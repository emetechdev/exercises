def colisiona(coordPunto, coordenadasCuadrado):
    menorValorX=coordenadasCuadrado[0][0]
    mayorValorX=coordenadasCuadrado[0][0]
    menorValorY=coordenadasCuadrado[0][1]
    mayorValorY=coordenadasCuadrado[0][1]
    
    # Valores Maximos y minimos
    for i in coordenadasCuadrado:
        if i[0] < menorValorX:
            menorValorX=i[0]
        if i[0] > mayorValorX:
            mayorValorX=i[0]
            
        if i[1] < menorValorY:
            menorValorY=i[1]
        if i[1] > mayorValorY:
            mayorValorY=i[1]
    
    estaFueraDeRangoX=False
    estaFueraDeRangoY=False
    if coordPunto[0] < menorValorX or coordPunto[0] > mayorValorX:
        estaFueraDeRangoX=True

    if coordPunto[1] < menorValorY or coordPunto[1] > mayorValorY:
        estaFueraDeRangoY=True
        
    if estaFueraDeRangoX or estaFueraDeRangoY:
        print(f'\033[17;70H====> NO hubo colision')
    else:
        print(f'\033[17;70H====> SI hubo colision')
        # Compara contacto con los bordes
        if coordPunto[0] == menorValorX or coordPunto[0] == mayorValorX or coordPunto[1] == menorValorY or coordPunto[1] == mayorValorY:
            print(f'\033[18;70H====> Y tocó uno de los bordes')
            
    
   
        
    
    
    
    
    
    return True