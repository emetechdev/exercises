import pygame, sys, time
import Librerias.Colores as COLOR

class Dino(pygame.sprite.Sprite):
    _lista_Animaciones=[]
    _pos_animacion=0
    
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface([46,47])
        self.rect=self.image.get_rect()
        self.rect.x=100
        self.rect.y=540
        self._lista_Animaciones.append(pygame.image.load(".\\Sprites\\dino1.png"))
        self._lista_Animaciones.append(pygame.image.load(".\\Sprites\\dino2.png"))
        self.image=self._lista_Animaciones[self._pos_animacion]
        self.image.set_colorkey((255,255,255))
    
    
    def update(self):
        self._pos_animacion+=1
        if self._pos_animacion>1:
            self._pos_animacion=0
        time.sleep(0.2)
        self.image=self._lista_Animaciones[self._pos_animacion]

def main():
    #inicializar la lireria pygame
    pygame.init()

    #pantalla
    pantalla=pygame.display.set_mode((360,640))
    pygame.display.set_caption("Mi Juego")
    
    reloj=pygame.time.Clock()
    reloj.tick(20)
    #seleccionar la fuente para el texto
    fuente=pygame.font.SysFont("Gloucester MT",48)

    #Dino
    dino=Dino()
    #lista sprite
    _lista_personaje=pygame.sprite.Group()
    _lista_personaje.add(dino)
    
    
    #loop
    salir=False
    while not salir:
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                salir=True
        pantalla.fill(COLOR.BLANCO) #color de fondo
        _lista_personaje.update()
        _lista_personaje.draw(pantalla)
        pygame.display.flip() #actualizar pantalla
        

    #cerrar la librería pygame y la ventana
    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()