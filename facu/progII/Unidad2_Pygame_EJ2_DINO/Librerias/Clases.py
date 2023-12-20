import pygame, time
import Librerias.Colores as COLOR
import Librerias.Constantes as Const

class Dino(pygame.sprite.Sprite):
    _lista_animacion=[]
    _pos_animacion=0
    _estado="corriendo"
    _velocidad_salto=-20
    def __init__(self,paramX,paramY):
        super().__init__()
        self.image=pygame.Surface([46,47])
        self.rect=self.image.get_rect()
        self.rect.x=paramX
        self.rect.y=paramY
        self._lista_animacion.append(pygame.image.load(".\\Sprites\\dino1.png"))
        self._lista_animacion.append(pygame.image.load(".\\Sprites\\dino2.png"))
        self.image=self._lista_animacion[self._pos_animacion]
        #self.image.set_colorkey(COLOR.BLANCO)
    
    def saltar(self):
        if self._estado!="saltando":
            self._estado="saltando"
            self._velocidad_salto=-30
    def update (self):
        if self._estado=="corriendo":
            self._pos_animacion+=1
            if self._pos_animacion>1:
                self._pos_animacion=0
            self.image=self._lista_animacion[self._pos_animacion]
        elif self._estado=="saltando":
            self.rect.y +=self._velocidad_salto
            self._velocidad_salto+=1
            if self.rect.y<=210:
                self._velocidad_salto=1
                self._estado="bajando"
        elif self._estado=="bajando":
            self.rect.y +=self._velocidad_salto
            self._velocidad_salto+=1
            if self.rect.y>=271:
                self.rect.y=271
                self._estado="corriendo"
        #print (self.rect.y,self._velocidad_salto, self._estado )
class Planta(pygame.sprite.Sprite):
    def __init__(self, paramX,paramY):
        super().__init__()
        self.image=pygame.Surface([31,70])
        self.rect=self.image.get_rect()
        self.rect.x=paramX
        self.rect.y=paramY
        self.image=pygame.image.load(".\\Sprites\\planta.png")
        self.image.set_colorkey(COLOR.BLANCO)
        
    def update(self):
        self.rect.x -=Const._velocidad
        if self.rect.x + self.rect.width <=0:
            self.rect.x=650

class Piso(pygame.sprite.Sprite):
    def __init__(self, paramX,paramY):
        super().__init__()
        self.image=pygame.Surface([2403,25])
        self.rect=self.image.get_rect()
        self.rect.x=paramX
        self.rect.y=paramY
        self.image=pygame.image.load(".\\Sprites\\piso.png")
        self.image.set_colorkey(COLOR.BLANCO)
        
    def update(self):
        self.rect.x -=Const._velocidad
        if self.rect.x + self.rect.width <=0:
            self.rect.x=self.rect.width -10