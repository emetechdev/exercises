def solicitar_coordenadas_del_cuadrado():
    print('\n\n\n\nIngrese las coordenadas del cuadrado')
    coordenadas=[]
    
    for i in range(4):
        
        cooX=int(input(f'Ingrese coordenada X del punto {i+1}: '))
        cooY=int(input(f'Ingrese coordenada Y del punto {i+1}: '))
        
        coordenadas.append([cooX,cooY])
    
                
    return coordenadas

def solicitar_coordenadas_del_punto():
    print('\n\n\nIngrese las coordenadas del punto')
    cooX=int(input(f'Ingrese coordenada X: '))
    cooY=int(input(f'Ingrese coordenada Y: '))
    
    return [cooX,cooY]