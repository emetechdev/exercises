import os

def dibujar_ejes():
    for i in range(21):
        # En la fila 'i', col 4, pinta un '+'
        print('\033[' + str(i) + ';8H+')
        if i%2==0:
            print(f'\033[{str(i)};2H{str(i)}')
        if i==10:
            print(f'\033[10;2H10 --')
        
    # Pinta Y
    print('\033[18;5HY')

    desplazamientoX=6
    for i in range(51):
        print('\033[19;' + str(i + desplazamientoX) + 'H+')
        if i%4==0:
            print(f'\033[21;{str(i + desplazamientoX)}H{str(i)}')
    
    # Pinta X
    print('\033[20;50HX')
    
    
def dibujar_punto(x, y, dibujo):
    correccionX=x + 6
    print(f'\033[{y};{correccionX}H{dibujo}')
    
    
def trazo(x, y):
    correccionX=x + 6
    inicioY=y+1
    rangoDeLinea=y
    if y == 0:
        rangoDeLinea=20
        inicioY=2
    elif y < 2:
        rangoDeLinea=y*20
    elif y < 3:
        rangoDeLinea=y*8
    elif y < 4:
        rangoDeLinea=y*6
    elif y < 6:
        rangoDeLinea=y*4
    elif y < 10:
        rangoDeLinea=y*2
    elif y > 10:
        rangoDeLinea=y-6
    
        
    for i in range(rangoDeLinea):
        print(f'\033[{str(inicioY)};{str(correccionX)}H.')
        inicioY +=1
    
    
    for i in range(x):
        print(f'\033[{str(y)};{str(i+6)}H.')
        
    


def dibujar_datos(coordPunto, coordenadasCuadrado):
    print(f'\033[6;80HCOORDENADAS')
    
    coordenadasPunto=f'Punto(x,y): {str(coordPunto)}'
    print(f'\033[7;70H{coordenadasPunto}')
    
    print(f'\033[10;70HPUNTOS DEL CUADRADO')
    fila=12
    punto=1
    for i in coordenadasCuadrado:
        print(f'\033[{str(fila)};70HPunto {str(punto)}(x,y): {str(i)}')
        fila +=1
        punto +=1
        
    
def cls():
    os.system('cls')
    
    
    