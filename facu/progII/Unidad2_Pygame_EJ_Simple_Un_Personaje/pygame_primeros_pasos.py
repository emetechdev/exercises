import pygame
import os, sys, time

""" Imagenes: Las animaciones son imágenes que se superponenen y se repiten en un ciclo
o en un bucle para generar un efecto de movimiento. Para ésto se usan los 'Sprites'
"""

BLANCO=(255,255,255)
NEGRO=(0,0,0)



class Persona(pygame.sprite.Sprite):
    _lista_Animaciones=[] # Lista que contiene todas las animaciones de la personita
    _pos_animacion=0 # Posicion de la imagen que se quiere mostrar
    
    def __init__(self):
        # Se ejecuta el constructor de la clase 'Sprite'
        super().__init__()
        # Primero se crea la superficie de la linea
        self.image=pygame.Surface([46,47])
        # Despues el cuadro que ocupa (el rectangulo al rededor que permite detectar colisiones, etc)
        self.rect=self.image.get_rect()
        # Se le da una posicion x, Y a la imagen
        self.rect.x=10
        self.rect.y=300
        # Se completa la lista de animaciones con las animaciones que se quieren caragar
        self._lista_Animaciones.append(pygame.image.load("./10.png"))
        # Se indica la imagen que se utiliza. Se toma por defecto la primera de la lista
        self.image=self._lista_Animaciones[self._pos_animacion] 
        # Se agrega la imagen 2
        self._lista_Animaciones.append(pygame.image.load("./11.png"))
        # Se le agrega el color de fondo
        self.image.set_colorkey((BLANCO))

    # Se hace una funcion para sobreescribir el método update() para que cada vez que actualice
    # le sume 1 a la posición de la imágen
    def update(self):
        self._pos_animacion+=1
        # Pregunto si la posicion de la imagen es mayor a uno
        if self._pos_animacion > 1:
            self._pos_animacion=0 
        # Luego se actualiza la imagen en la posicion
        self.image=self._lista_Animaciones[self._pos_animacion]


def main():
    pygame.init()
    pantalla=pygame.display.set_mode((360,450))
    pygame.display.set_caption("Mi Primer Juego")
    reloj=pygame.time.Clock()
    fuente=pygame.font.SysFont("Arial",20) # Fuente que se usa para el programa
    
    ejemploMensaje=fuente.render("Ejemplo de un Mensaje", True, NEGRO)
    
    # Se instancia el objeto
    persona=Persona()
    # Se crea una coleccion de sprites para despues recorrerla
    _lista_sprite=pygame.sprite.Group()
    # A la lista se le agrega el objeto persona para que lo dibuje
    _lista_sprite.add(persona)
    
    
    
    
    # Loop del Juego
    salir=False
    while not salir:
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                salir=True
        pantalla.fill(BLANCO) # Rellena con color blanco la pantalla
        
        # Se dibuja. Primero se actualiza. Esto recorre todos los elementos dentro de la lista
        _lista_sprite.update()
        # Despues de actualizar, se pide que dibuje y que lo lleve a la pantalla
        _lista_sprite.draw(pantalla)
        
        reloj.tick(20) # Velocidad con la que se refresca la ventana
        
        pantalla.blit(ejemploMensaje, [10,10]) # Ejemplo de como renderizar un mensaje en pantalla
        pygame.display.flip() # Actualiza la ventana
    
    # Se cierra la librería y se cierra la ventana
    pygame.quit()
    sys.exit()

if __name__=='__main__':
    main()
