import pygame, sys
import Librerias.Colores as COLOR
import Librerias.Clases as Asset
import Librerias.Constantes as Const
import Librerias.Funciones as fun



def main():
    #inicializar la lireria pygame
    pygame.init()
    pygame.mixer.init() #inicializar sonido
    #pantalla
    pantalla=pygame.display.set_mode((640,360))
    pygame.display.set_caption("Dino")
    
    reloj=pygame.time.Clock()
    
    #seleccionar la fuente para el texto
    fuente=pygame.font.SysFont("Gloucester MT",48)
    '''
        sonidio
    '''
    _audio_salto=pygame.mixer.Sound(".\\audio\\jump.wav")
    _audio_colision=pygame.mixer.Sound(".\\audio\\die.wav")
    '''
        Instanciar todos los Objetos
    '''
    dino=Asset.Dino(100,Const._limite_piso-29)
    piso1= Asset.Piso(0,Const._limite_piso)
    piso2= Asset.Piso(piso1.rect.width,Const._limite_piso)
    planta=Asset.Planta(650,Const._limite_piso -40)
    _lista_elementos=pygame.sprite.Group()
    _lista_planta=pygame.sprite.Group()
    _lista_elementos.add(dino)
    _lista_elementos.add(piso1)
    _lista_elementos.add(piso2)
    _lista_elementos.add(planta)
    _lista_planta.add(planta)
    
    
    
    
    #loop
    salir=False
    while not salir:
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                salir=True
            if evento.type==pygame.KEYDOWN:
                if evento.key==pygame.K_SPACE:
                    _audio_salto.play()
                    dino.saltar()
                    
        
        pantalla.fill(COLOR.BLANCO) #color de fondo
        reloj.tick(20) #Definir la cantidad de FPS
        _lista_elementos.update()
        _lista_elementos.draw(pantalla)
        colision=pygame.sprite.spritecollide(dino,_lista_planta,False)
        if colision:
            #game over
            mensaje=fuente.render("GAME OVER",40,COLOR.NEGRO)
            pantalla.blit(mensaje,[150,150])
            _audio_colision.play()
            pygame.display.flip() #actualizar pantalla
            salir=fun.pausa()
            
        pygame.display.flip() #actualizar pantalla
        

    #cerrar la librería pygame y la ventana
    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()