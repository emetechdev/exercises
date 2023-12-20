import pygame
import time
import lib.var as VAR
import lib.core as CLASS
import lib.config as Config
import lib.color as COLOR
import lib.helpers as Funcion


def main():
    # Inicio y Configuracion de Pantalla
    Config.configGame()
    VAR.RELOJ.tick(20)

# -----------------------------------------------------
    # Lista de animaciones
    _lista_animaciones = pygame.sprite.Group()
    _lista_fin_juego = pygame.sprite.Group()
    _lista_recompensas = pygame.sprite.Group()
    _lista_recompensas2 = pygame.sprite.Group()
    _lista_obstaculos = pygame.sprite.Group()
    _lista_obstaculos2 = pygame.sprite.Group()

    # Objetos
    _jugador = CLASS.Jugador(True)
    _jugador_fin = CLASS.Jugador(False)
    _piso = CLASS.Piso(0, 0, VAR.VELOCIDAD_INICIAL)
    _piso2 = CLASS.Piso(1000, 0, VAR.VELOCIDAD_INICIAL)
    _vida = CLASS.Vida(VAR.VIDA100)

    _lista_animaciones.add(_piso)
    _lista_animaciones.add(_piso2)
    _lista_animaciones.add(_jugador)
    _lista_animaciones.add(_vida)
    _lista_fin_juego.add(_jugador_fin)

    Funcion.lista_de_animaciones(
        'comida', VAR.VELOCIDAD_INICIAL, _lista_recompensas)
    Funcion.lista_de_animaciones(
        'enemigo', VAR.VELOCIDAD_INICIAL, _lista_obstaculos)
    Funcion.lista_de_animaciones(
        'comida', VAR.VELOCIDAD_DIFICULTAD_2, _lista_recompensas2)
    Funcion.lista_de_animaciones(
        'enemigo', VAR.VELOCIDAD_DIFICULTAD_2, _lista_obstaculos2)

    inicio_tiempo = time.time()


# -----------------------------------------------------
    # Intro:
    Funcion.mostrar_intro_juego()

# -----------------------------------------------------
    _total_vida = VAR.VIDA_INICIAL
    _cantidad_mordidas = VAR.MORDIDA_INICIAL
    _cronometro_mordida = time.time()
    _contador = 0
# -----------------------------------------------------

    # Loop
    salir = False
    while not salir:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir = True
            if evento.type == pygame.KEYDOWN:
                Funcion.teclado_accion(evento.key, _jugador)

        VAR.SCREEN.fill((255, 255, 255))
        tiempo_transcurrido = Funcion.tiempo(inicio_tiempo, time.time())

        if _total_vida > 1:
            Funcion.mostrar_animaciones(_lista_animaciones)
            if _total_vida <= 50 or tiempo_transcurrido > 30:
                Funcion.mostrar_animaciones(_lista_recompensas2)
                Funcion.mostrar_animaciones(_lista_obstaculos2)
            else:
                Funcion.mostrar_animaciones(_lista_recompensas)
                Funcion.mostrar_animaciones(_lista_obstaculos)

        # Colisiones
        col_comida = Funcion.detectar_colision(_jugador, _lista_recompensas)
        col_comida2 = Funcion.detectar_colision(_jugador, _lista_recompensas2)
        col_zombie = Funcion.detectar_colision(_jugador, _lista_obstaculos)
        col_zombie2 = Funcion.detectar_colision(_jugador, _lista_obstaculos2)

        _tiempo = Funcion.mostrar_tiempo('Tiempo', tiempo_transcurrido)
        VAR.SCREEN.blit(_tiempo, [700, 10])

        mordidas = Funcion.mostrar_tiempo('Mordidas', _cantidad_mordidas)
        VAR.SCREEN.blit(mordidas, [300, 10])

        _tiempo_zombificacion = 25*_cantidad_mordidas

        if _contador == 90:
            _cronometro_mordida = time.time()
            _total_vida -= _tiempo_zombificacion
            _contador = 0
        else:
            _contador += 1
            _seg = Funcion.tiempo(_cronometro_mordida, time.time())
            contrareloj = Funcion.mostrar_tiempo('Contrareloj', _seg)
            VAR.SCREEN.blit(contrareloj, [500, 10])

        if col_comida or col_comida2:
            VAR.AUDIO_COMER.play()
            if _total_vida < 100:
                _total_vida += 25
        elif col_zombie or col_zombie2:
            VAR.AUDIO_AUCH.play()
            _cantidad_mordidas += 1
        elif _total_vida < 1:
            VAR.AUDIO_MUERTE.play()
            VAR.SCREEN.fill(COLOR.NEGRO)
            _lista_animaciones.empty()
            _lista_obstaculos.empty()
            _lista_recompensas.empty()
            Funcion.finalizar_juego()
            Funcion.mostrar_animaciones(_lista_fin_juego)

        _vida = Funcion.actualizar_vidas(_total_vida)
        _lista_animaciones.add(_vida)

        pygame.display.flip()

    # Cierre de librería y ventana
    Config.closeGame()


if __name__ == "__main__":
    main()
