

import pandas as pd
import glob
import sys
from pathlib import Path
# Archivo Base
# IWI
# https://aula.usm.cl/grade/export/txt/index.php?id=12105
# INF130
# https://aula.usm.cl/grade/export/txt/index.php?id=12092


if(len(sys.argv) < 2):
    raise Exception("Missing params")
curso = sys.argv[1]
archivo = sys.argv[2]

li = []
df = pd.read_csv("ENTRADA/"+archivo, index_col=None, header=0,
                 skipinitialspace=True, dtype=str)
columnas_originales = df.columns
li.append(df)

try:
    df = pd.concat(li, axis=0, ignore_index=True)
    i = 0

    for x in columnas_originales:
        if i in [0, 1, 2, 3, 4, len(columnas_originales)-1]:
            df.drop([x], axis=1, inplace=True)
        i += 1
    df.rename(columns={"Dirección de correo": "correo"}, inplace=True)
except ValueError as e:
    print("No hay archivos en la carpeta ENTRADA")
    exit(1)


i = 0
columnas_aux = []
columnas_originales = df.columns[1:]


for x in columnas_originales:
    df.loc[df[x] != '-', x] = df[x]
    df.loc[df[x] == '-', x] = 0
    df.rename(columns={x: "cont_"+str(i)}, inplace=True)
    df = df.astype({"cont_"+str(i): "float32"})
    columnas_aux.append("cont_"+str(i))
    i += 1


df["nota"] = df.mean(axis=1)
if df["nota"].max() == 10:
    df["nota"] = df["nota"]*10
df = df.astype({"nota": "int64"})
df.drop(columnas_aux, axis=1, inplace=True)


all_files = glob.glob("LISTAS/"+curso+"/*.xls")
all_files.sort()

listas_alumnos = pd.read_excel(all_files[0], skiprows=8, dtype=str)
listas_alumnos["full_rut"] = listas_alumnos["RUT"] + \
    "-" + listas_alumnos["DV.1"]


for file in all_files[1:]:
    temp_df = pd.read_excel(file, skiprows=8, dtype=str)
    temp_df["full_rut"] = temp_df["RUT"] + "-" + temp_df["DV.1"]

    listas_alumnos = listas_alumnos.append(
        temp_df)

listas_alumnos = listas_alumnos.merge(
    df, left_on='Correo', right_on='correo', how='left')
listas_alumnos = listas_alumnos.drop(
    listas_alumnos.columns[list(range(11))], axis=1)

print(listas_alumnos)

listas_alumnos.to_excel("SALIDA/FORMATIVAS/" +
                        archivo.split("/")[-1].split(".")[0]+".xls", index=False)
