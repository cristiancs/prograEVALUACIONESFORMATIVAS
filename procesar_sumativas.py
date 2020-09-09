

import pandas as pd
import glob
import sys
from pathlib import Path
# Archivo Base
# Descarga desde https://aula.usm.cl/grade/export/txt/index.php?id=107441

fields = [2, 6]


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
    #df.loc[df[x] != '-', x] = 1
    df.loc[df[x] == '-', x] = 0
    df.rename(columns={x: "cont_"+str(i)}, inplace=True)
    df = df.astype({"cont_"+str(i): "float64"})
    columnas_aux.append("cont_"+str(i))
    i += 1


df["nota"] = df.sum(axis=1)
df["nota"] = df["nota"] * 10
df.drop(columnas_aux, axis=1, inplace=True)


# df.loc[df.nota == cant_evaluaciones, "nota"] = 100
# Valor temporal para que no les de un 1 cuando es un 0
# df.loc[df.nota == 0, "nota"] = cant_evaluaciones+5
# df.loc[df.nota < cant_evaluaciones, "nota"] = 100
# df.loc[df.nota == cant_evaluaciones+5, "nota"] = 0


df.to_excel("SALIDA/SUMATIVAS/" +
            all_files[0].split("/")[-1].split(".")[0]+".xls", index=False)

# Las pasamos a la lista de cada curso

# all_files = glob.glob("LISTAS/"+curso+"/*.xls")


# Path("./SALIDA/"+curso).mkdir(parents=False, exist_ok=True)
# for filename in all_files:
#    paralelo = filename.split("_")[2]
#    print("\nPARALELO: " + paralelo)
#    lista_curso = pd.read_excel(filename, skiprows=8, dtype=str)
#    lista_curso["rut"] = lista_curso["RUT"] + "-" + lista_curso["DV.1"]
#    lista_curso = lista_curso.merge(
#        df, left_on='rut', right_on='rut', how='left')

#    lista_curso.to_excel("SALIDA/"+curso+"/"+paralelo+".xls")
# print(lista_curso['nota'].to_string(index=False))
# print(lista_curso.nota.isnull().sum())