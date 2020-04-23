

import pandas as pd
import glob
import sys
from pathlib import Path
# Archivo Base
# Descarga desde https://aula.usm.cl/grade/export/txt/index.php?id=107441

fields = [2, 6]


print("Reading input")
all_files = glob.glob("ENTRADA/*.csv")

li = []

for filename in all_files:
    print(filename)
    df = pd.read_csv(filename, index_col=None, header=0,
                     skipinitialspace=True, usecols=fields, dtype=str)
    li.append(df)

try:
    df = pd.concat(li, axis=0, ignore_index=True)
    df.rename(columns={df.columns[0]: "rut",
                       df.columns[1]: "nota"}, inplace=True)
    df["rut"] = df["rut"].str.upper()
except ValueError as e:
    print("No hay archivos en la carpeta ENTRADA")
    exit(1)

# Convertimos a 0 / 100

df.nota[df.nota != '-'] = 100
df.nota[df.nota == '-'] = 0

# Las pasamos a la lista de cada curso

if len(sys.argv) > 1:

    curso = sys.argv[1]
    all_files = glob.glob("LISTAS/"+curso+"/*.xls")

    Path("./SALIDA/"+curso).mkdir(parents=False, exist_ok=True)
    for filename in all_files:
        paralelo = filename.split("_")[2]
        print("\nPARALELO: " + paralelo)
        lista_curso = pd.read_excel(filename, skiprows=8, dtype=str)
        lista_curso["rut"] = lista_curso["RUT"] + "-" + lista_curso["DV.1"]
        lista_curso = lista_curso.merge(
            df, left_on='rut', right_on='rut', how='left')

        lista_curso.to_excel("SALIDA/"+curso+"/"+paralelo+".xls")
        print(lista_curso['nota'].to_string(index=False))


else:
    print(df.to_string(index=False))
