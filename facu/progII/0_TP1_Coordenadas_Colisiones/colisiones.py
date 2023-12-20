# Detectar colision entre dos elementos físicos que se desplazan en un espacio bidimensional
# Los elementos son un cuadrado y un punto
# Entrada: 1. coordenadas (x,y) del punto. 2. Entradas coordenadas (x,y) de cada uno de los 4 puntos del cuadrado

# El código generado, deberá informar cuando dos puntos colisionan con cualquier parte del cuadrado. 
# En caso de que los puntos colisionen con los bordes del cuadrado se aclare especialmente en este caso, que el 
# punto esta colisionando con los bordes de la figura. 
# Los elementos pueden cambiar de posición en el espacio, por lo que cada vez que se ejecute el código se deberán pedir 
# las coordenadas (x,y) de los 5 puntos mencionados. 
# Es muy importante, que la posición del punto se marque con líneas de puntos que indiquen cual es la posición x,y.
import os
#from colorama import Fore
import dibujo as dib
import entradas as inp
import validacion as val



def main():
    print('TP 1 - COLISIONES')
    os.system('cls')

    dib.dibujar_ejes()
    coordenadasCuadrado=inp.solicitar_coordenadas_del_cuadrado()
    print(f'Coordenadas ingresadas: {coordenadasCuadrado}')
    coordPunto=inp.solicitar_coordenadas_del_punto()
    #coordenadasCuadrado=[[8, 8], [24, 8], [8, 16], [24, 16]]
    #coordPunto=[16,12]
    dib.cls()

    # dibujo cuadrado
    for i in coordenadasCuadrado:
        dib.dibujar_punto(i[0], i[1], f'C{i}') #(x,y, dibujo)

    # dibujo punto ==> Recbe: (x,y, dibujo)
    dib.dibujar_punto(coordPunto[0], coordPunto[1], f'PO{coordPunto}')
    dib.trazo(coordPunto[0], coordPunto[1])

    dib.dibujar_ejes()
    dib.dibujar_datos(coordPunto, coordenadasCuadrado)
    val.colisiona(coordPunto, coordenadasCuadrado)

    input()




if __name__=='__main__':
    main()