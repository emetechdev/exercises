import pygame
def pausa():
    salir=False
    while not salir:
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                salir=True
            if evento.type==pygame.KEYDOWN:
                if evento.key==pygame.K_SPACE:
                    salir=True
    return salir                