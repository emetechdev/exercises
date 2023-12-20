import pygame, sys, time
import libs.colores as COLOR


""""Clase Dino - Es una clase se va a comportar como si fuera un 'Sprite'"""
class Dino(pygame.sprite.Sprite): # Hereda de "Sprite"
    # "_lista_Animaciones=[]" ayuda a crear una lista de dibujos o "Sprites" que cuando se la recorre se crea la animacion
    # por esa sensacion de movimiento. Y cada vez que se actualiza, cambia a la imagen siguiente
    _lista_Animaciones=[]
    _pos_animacion=0 # posición en la "_lista_Animaciones"
    
    # Se crea el constructor
    def __init__(self):  # 'self' hace referencia a sí mismo
        # Consigna 1
        
        # Como necesito implementar cierto comportamiento de la "Clase Base", le digo que ejecute el constructor de la "Clase Base"
        super().__init__() # Ejecuta el constructor de la clase base y se inicializan todos los valores que estan ya programados en la clase "Sprite"
        self.image=pygame.Surface([46,47]) # Se le asigna la superficie a la imagen
        
        # "self.rect" se crea un rectangulo que represente la superficie de la imagen. Y sirve para mover la imagen
        # o para detectar colisiones
        self.rect=self.image.get_rect() # Dice que genere un rectangulo a partir de la línea anterior (con la misma superficie)
        
        # Marco la posicion del rectángulo usando coordenadas. Estos son los que se modifican para que el bicho se mueva
        self.rect.x=100 # ubicacion en eje 'X' del objeto
        self.rect.y=540 # ubicacion en eje 'Y' del objeto

        # "pygame.image.load" carga o levanta la imgen que se va a usar y "self._lista_Animaciones.append" carga o mete
        # la imagen a la lista de animaciones
        self._lista_Animaciones.append(pygame.image.load("./actividad_clase_9/sprites/dino1.png"))
        self._lista_Animaciones.append(pygame.image.load("./actividad_clase_9/sprites/dino2.png"))
        
        # "self.image" ésta es la imágen que queremos que cargue y el dibujo que le decimos que muestre va a ser el que obtenga de 
        # "_lista_Animaciones" en la posición indicada
        self.image=self._lista_Animaciones[self._pos_animacion]
        self.image.set_colorkey((COLOR.BLANCO)) # Aca todo lo que tenga blanco la imagen se supone que lo va a pasar a transparente
    
    # Se sobreescribe el método "update()" de la "Clase Spite". Este lo que hace es actualizar la imagen, acá es donde se hace la magia.
    # Entonces lo que le digo es que cada vez que se actualice, se mueva a la imágen siguiente.
    def update(self):
        # Si queremos que el personaje se mueva adelante/atras, modificamos el eje de las "X"
        # Si queremos que el personaje se mueva arriba/abajo, modificamos el eje de las "Y"
        self._pos_animacion += 1 # A la posición actual le suma 1
        if self._pos_animacion > 1: # Para evitar un "overflow", si llega al final de la lista, le decimos que vuelva a empezar
            self._pos_animacion = 0 # vuelve a la posicion 0 de la lista de animaciones
            
        time.sleep(0.2)
        self.image=self._lista_Animaciones[self._pos_animacion]
    
    # Metodo para darle movimiento al objeto
    def mover(self, velocidad):
        # Se le suma unos enteros para que se desplace el bicho en los ejes de coordenadas
        self.rect.x += velocidad 

        
# Consigna 4
class Planta(pygame.sprite.Sprite):
    _piso=[pygame.image.load("./actividad_clase_9/sprites/planta.png")]
    
    def __init__(self):
        # Consigna 1
        super().__init__() 
        self.image=pygame.Surface([15,20])
        self.rect=self.image.get_rect()
        self.rect.x=500
        self.rect.y=520 # ubicacion en eje 'Y' del objeto
        self.image=self._piso[0]
        self.image.set_colorkey((COLOR.BLANCO))

# Consigna 3
class Piso(pygame.sprite.Sprite):
    _piso=[pygame.image.load("./actividad_clase_9/sprites/piso.png")]
    
    def __init__(self):
        # Consigna 1
        super().__init__()
        self.image=pygame.Surface([15,20])
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=575
        self.image=self._piso[0]
        self.image.set_colorkey((COLOR.BLANCO))

# Consigna 2
class Ave(pygame.sprite.Sprite):
    _lista_Aves=[]
    _pos_ave=0
    
    def __init__(self):
        # Consigna 1
        super().__init__()
        self.image=pygame.Surface([15,20])
        self.rect=self.image.get_rect()
        self.rect.x=600
        self.rect.y=50
        self._lista_Aves.append(pygame.image.load("./actividad_clase_9/sprites/pajaro1.png"))
        self._lista_Aves.append(pygame.image.load("./actividad_clase_9/sprites/pajaro2.png"))
        self.image=self._lista_Aves[self._pos_ave]
        self.image.set_colorkey((COLOR.BLANCO))
        
    def update(self):
        self._pos_ave += 1
        if self._pos_ave > 1:
            self._pos_ave = 0
            
        time.sleep(0.2)
        self.image=self._lista_Aves[self._pos_ave]



def main():
    # Inicializacion
    pygame.init()

    # Configuracion de Pantalla
    pantalla=pygame.display.set_mode((800,640))
    pygame.display.set_caption("Dinoactividad")
    
    # La velocidad se mide en Fotogramas. El objeto "reloj" que es la instancia de "Clock()" se va a encargar de que el juego
    # vaya o mas rapido, o mas lento 
    # Se indica con qué velocidad python tiene que refrescar la pantalla
    reloj=pygame.time.Clock()
    reloj.tick(20)
    
    # Estilos
    fuente=pygame.font.SysFont("Arial",48)

    # Objetos: Dino y Ave
    dino=Dino()
    ave=Ave()
    piso=Piso()
    planta=Planta()
    
    # Lista de sprites: Estas son listas de elementos que me permite recorrer y mostrar elementos
    _lista_dino=pygame.sprite.Group()
    _lista_dino.add(dino)
    
    # Esta sería una lista de colision. 
    _lista_colision=pygame.sprite.Group()
    _lista_colision.add(dino)

    _lista_ave=pygame.sprite.Group()
    _lista_ave.add(ave)
    
    _piso=pygame.sprite.Group()
    _piso.add(piso)
    
    _planta=pygame.sprite.Group()
    _planta.add(planta)
    
    
    # Loop: Hace que se esté redibujando todo el tiempo
    salir=False
    while not salir:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir=True
            if evento.type == pygame.KEYDOWN: # Si presiona una tecla
            # Tratamos de atrapar un evento para poder determinar si el bicho se mueve
                if evento.key == pygame.K_RIGHT:
                # Si la tecla que se presiono es la de la derecha por ejemplo, uso el metodo de movimiento para desplazar al dino
                    dino.mover(5)
                
        pantalla.fill(COLOR.BLANCO)

        # Acá si dino choco con algo que esté en la lista de colición me avisa. El "False" es para decirle que si algo chocó, que no lo
        # borre de la lista. El "True" sería para que sí lo borre.
        colision = pygame.sprite.spritecollide(dino, _lista_colision, False) # Devuelve un booleano
        if colision:
            # Se define que se hace en caso de colisionar. En este caso se muestra un mensaje
            mensaje = fuente.render("Game Over", 40, (0, 0, 0))
            pantalla.blit(mensaje, [200, 200])

    
        # Consigna 1 : "update()" y "draw(pantalla)" Lo que hacen es actualizar y dibujar en cada iteración a una velocidad suficiente 
        # que nos da la sensación de movimiento
        _lista_dino.update()
        _lista_dino.draw(pantalla)
        
        # Consigna 2        
        _lista_ave.update()
        _lista_ave.draw(pantalla)
        
        # Consigna 3        
        _piso.update()
        _piso.draw(pantalla)
        
        # Consigna 4        
        _planta.update()
        _planta.draw(pantalla)
        
        
        
        pygame.display.flip() 
        

    # Cierre de librería y ventana
    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()