import pandas as pd
import matplotlib.pyplot as mp
import os


# Se puede trabajar con archivos externos --> .csv
# fuente: https://datos.gob.ar/dataset/sspm-canasta-basica-alimentaria-regiones-pais
df=pd.read_csv('./Numpy/canasta-basica.csv')
df.plot(kind='bar',x='indice_tiempo',xlabel='Valores en Pesos', ylabel='Referencia en Pesos', title='Grafico')
mp.show()

# Hacer un grafico tomando la libreria de matplot pero metiendole datos
file=df.iloc[1]
# Le digo que me traiga de esta fila, todos los indices (osea los nombres de las columnas).
# Y a esto lo voy a convertir en una lista. y despues hago lo mismo con los valores
indices=['a','b']
valores=[1,2]
mp.bar(indices,valores,color='green')
mp.xlabel='Prov'
mp.ylabel='Valores'
mp.title('Grafico')
mp.show()

print(indices)
print(valores)

# Rutas relativas
os.system('cls')
path=os.path.abspath('clasePandas.py')
path=os.path.dirname(path)
print(path)
