import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as mp

# Extraccion de datos
# Transformar los datos. (Porque pueden tener fuentes diferentes, o no ser homogeneos. Por eso hay que depurarlos en ésta instancia)
# Cargar/Procesar los datos.

# Leemos los datos del archivo para convertirlos en un dataframe.
df = pd.read_csv('./Numpy/canasta-basica.csv') # con ésta linea ya se convierten
# Si el archivo tiene un separador distinto a la coma ',' se puede agregar en la apertura del archivo
# el separador que se está usando para distinguir las columnas. Ej: sep=';'
df = pd.read_csv('./Numpy/ejemplo2.csv', sep=';') # Usando separador
df2 = pd.read_csv('./Numpy/ejemplo2.csv') # Sin usar separador

print(df)
print(df2)

# Es como un 'group by' de un 'select', agrupa los datos.
# "size()" me indica el tamaño y me genera una columna más con la cantidad agrupada, pero por defecto no tiene nombre
# por eso se agrega "reset_index(name='Total')", ésto es para nombrar la columna con "Total"
df1 = df.groupby(['01/12/2020']).size().reset_index(name='Total') # Se puede agrupar por más de una columna
df2 = df.groupby(['01/12/2021']).size().reset_index(name='Total') # Se puede agrupar por más de una columna

# Se pueden renombrar las columnas del df2 para poder compararlas
df2 = df2.rename(columns={'noreste':'pa alla'})
df_full = pd.merge(df1, df2, on='01/12/2020') # on es la columna en comun que los combina


print(df1)
print(df2)
print(df_full) # Revisar bien como es

# "value_counts()" devuelve una serie con la primera columna con el "nombre de indice" y una 
# segunda columna indicando cuantas veces se repite. Todo ésto devuelve una estructura que no 
# es una lista. Así que lo convertimos a lista con el método "list()"
x = list(df_full.value_counts()) 
y=[0,0,0,0,0]

# Recorre la estructura, usa el largo de "df_full"
for i in range(len(df_full)):
    if(df_full.iloc[i]['nombre_columna'] == x[i]):
        # le suma al vector "y" los valores
        y[i] += df_full.iloc[i]['Total_x'] + df_full.iloc[i]['Total_y']


print(len(x)) # devuelve los nodos que tiene