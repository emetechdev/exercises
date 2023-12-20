import pygame, sys
import Librerias.Colores as COLOR

""" Imagenes: Las animaciones son imágenes que se superponenen y se repiten en un ciclo
o en un bucle para generar un efecto de movimiento. Para ésto se usan los 'Sprites'
"""



def main():
    # Inicializar la lireria pygame. Con ésto se activa el inicio
    pygame.init()

    # Pantalla: "set_mode((360,640)" define el tamaño que va a tener la ventana del juego
    pantalla=pygame.display.set_mode((360,640)) # Se instancia un objeto "pantall"
    pygame.display.set_caption("Mi Juego") # Se setea el nombre de la ventana
    
    reloj=pygame.time.Clock() # Se instancia un objeto "reloj" que nos va a manejar la velocidad del juego
    
    #seleccionar la fuente para el texto
    fuente=pygame.font.SysFont("Gloucester MT",48)

    # Loop: éste es el ciclo del flujo del juego. Es una rutina que se repite y mientras se repita, el juego va a estar activo
    # y cuando queramos salir del juego, vamos a tener que salir de la rutina
    salir=False
    while not salir:
        """"En la rutina se van escuchando los eventos. Los eventos consisten en una 'Cola de Eventos' que se recorre para poder determinar
        que eventos se dispararon. Entonces, se recorre la cola de eventos que es 'pygame.event.get()' y luego aplicamos condicionales para determinar 
        cual fue."""
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                salir=True
        
        pantalla.fill(COLOR.BLANCO) # Se define color de fondo de la pantalla
        #pantalla.blit("Hola",[200,200]) # Esta sentencia se usa para mostrar un mensaje en pantalla
        reloj.tick(20) # Se define la cantidad de FPS (Fotogramas (o Frames) Por Segundo)
        pygame.display.flip() # "flip()" Actualiza la pantalla. Esto es necesario para poder ver los cambios realizados
        

    # Cerrar la librería pygame y la ventana
    pygame.quit() # Cierra la librería
    sys.exit() # El sistema cierra la ventana


if __name__=="__main__":
    main()