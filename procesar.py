

import pandas as pd
import glob
import sys
from pathlib import Path
# Archivo Base
# IWI
# https://aula.usm.cl/grade/export/txt/index.php?id=1493
# INF130
# https://aula.usm.cl/grade/export/txt/index.php?id=4101


curso = sys.argv[1]


print("Reading input")
all_files = glob.glob("ENTRADA/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0,
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


df["nota"] = df.mean(axis=1) * 10
df = df.astype({"nota": "int64"})
df.drop(columnas_aux, axis=1, inplace=True)


# Las pasamos a la lista de cada curso

archivo_salida = "SALIDA/"+curso+"/" + \
    all_files[0].split("/")[-1].split(".")[0]+".xls"

all_files = glob.glob("LISTAS/"+curso+"/*.xls")
all_files.sort()

Path("./SALIDA/"+curso).mkdir(parents=False, exist_ok=True)

writer = pd.ExcelWriter(archivo_salida)


for filename in all_files:
    paralelo = filename.split("_")[2]
    print("\nPARALELO: " + paralelo)
    lista_curso = pd.read_excel(filename, skiprows=8, dtype=str)

    lista_curso = lista_curso.merge(
        df, left_on='Correo', right_on='correo', how='left')

    lista_curso.to_excel(writer, sheet_name=paralelo)
    # print(lista_curso['nota'].to_string(index=False))
    # print(lista_curso.nota.isnull().sum())
writer.save()
