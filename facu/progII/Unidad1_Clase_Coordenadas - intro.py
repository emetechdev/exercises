

import os
# from colorama import Fore
os.system('cls')

""" Coordenadas. El cero empieza en la parte superior izquierda"""
# Posiciono el cursor en una coorddenada:  El formato es print("\033[fila,colH]")
# print("\033[5;10H*")

""" Dibujo de ejes de coordenadas X/Y """
# Trazo el eje 'y'
for i in range(30):
    print('\033[' + str(i) + ';4H|')

# Pinto la 'y'
print('\033[2;3HY')

# Trazo el eje 'x'
for i in range(30):
    print('\033[20;' + str(i) + 'H-')

# Pinto la 'x'
print('\033[21;28HX')


# Pruebas 
print('Inicio prueba')
print('\033[1;1H]')
print('Fin prueba')

""" Ejercicio con coordenadas"""
# Punto 'P'
des_y=4
px=25
py=10

# Coordenadas del cuadrado
ax=8
ay=10
bx=20
by=10
cx=20
cy=2
dx=8
dy=2



# Trazo el eje 'y'
for i in range(20):
    print('\033[' + str(i) + ';4H|')

# Pinto la 'y'
print('\033[2;3HY')

# Trazo el eje 'x'
for i in range(30):
    print('\033[20;' + str(i) + 'H-')

# Pinto la 'x'
print('\033[21;28HX')



input()