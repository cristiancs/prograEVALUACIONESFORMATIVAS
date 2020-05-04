# Evaluador tareas formativas

## Descarga de listas

    Puede descargar las listas de notas desde https://aula.usm.cl/grade/export/txt/index.php?id=[id]

    Siendo id el id del curso.

## Uso

    python3 procesar.py CURSO

Si se desea que se compare contra las listas del curso debe ingresar la carpeta en la cual se encuentran los archivos dentro de la carpeta LISTAS, en caso contrario, solo se indicaran las notas según rut, extraidas desde ENTRADA/\*.csv

## Dependencias

    pip3 install pandas xlrd xlwt
