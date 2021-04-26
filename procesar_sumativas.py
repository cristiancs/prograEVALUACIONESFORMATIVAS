

import pandas as pd
import glob
import sys
from pathlib import Path
# Archivo Base
# Descarga desde https://aula.usm.cl/grade/export/txt/index.php?id=107441

fields = [2, 6]


curso = sys.argv[1]
archivo = sys.argv[2]


print("Reading input")


li = []
df = pd.read_csv("ENTRADA/"+archivo, index_col=None, header=0,
                    skipinitialspace=True, dtype=str)
columnas_originales = df.columns
li.append(df)


try:
    df = pd.concat(li, axis=0, ignore_index=True)
    i = 0

    for x in columnas_originales:
        if i in [0, 1,  3, 4, 5, len(columnas_originales)-1]:
            df.drop([x], axis=1, inplace=True)
        i += 1
    df.rename(columns={"Número de ID": "rut"}, inplace=True)
    df["rut"] = df["rut"].str.upper()
except ValueError as e:
    print("No hay archivos en la carpeta ENTRADA")
    exit(1)

# Convertimos a 0 / 1 / 100
cant_evaluaciones = len(df.columns[1:])


i = 0
columnas_aux = []
columnas_originales = df.columns[1:]


for x in columnas_originales:
    df.loc[df[x] == '-', x] = 0
    df = df.astype({x: "float32"})
    df[x] = round(df[x] * 10, 0)
    i += 1

df.drop(columnas_aux, axis=1, inplace=True)


df.to_excel("SALIDA/SUMATIVAS/" +
            archivo.split("/")[-1].split(".")[0]+".xls", index=False)
