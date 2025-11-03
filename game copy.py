import pygame as pg
import sys
from variables import (
    ASPECT_RATIO, CENTER_SCREEN, PATH_ESFERA_IMG,
    FUENTE_ALAGARD
)
import random as rd

def set_main_game_configs(game_name: str) -> dict:
    configs = {
#        'icono_surface': pg.image.load(PATH_ESFERA_IMG),
        # main_display: pg.display.set_mode(ASPECT_RATIO, pg.RESIZABLE)
        'main_display': pg.display.set_mode(ASPECT_RATIO),
        'color_fondo': pg.Color('pink'),
        'running_state': True,
        'selected_hero_info': None
    }

    pg.display.set_caption(game_name)
#    pg.display.set_icon(configs.get('icono_surface'))

    return configs

def manejador_de_eventos(configs: dict, heroes: list[dict]):

    for event in pg.event.get():

        if event.type == pg.QUIT:
            configs['running_state'] = False
        
        if event.type == pg.MOUSEBUTTONDOWN:
            print(event)
            if event.button == 1:
                random_index_list = rd.randint(0, len(heroes) - 1)
                background_color_name = rd.choice(['cyan', 'red', 'blue', 'pink'])
                color_random_name = rd.choice(['black', 'white'])

                configs['color_fondo'] = pg.Color(background_color_name)
                configs['color_texto'] = pg.Color(color_random_name)

                configs['selected_hero_info'] = heroes[random_index_list]

def cerrar_juego():
    print('Cerrando el juego')
    pg.quit()
    sys.exit()

def crear_superficie_texto(size: int, text: str, color: pg.Color, pos: tuple):
    # texto = pg.font.SysFont('Arial', size)
    texto = pg.font.Font(FUENTE_ALAGARD, size)
    texto_render = texto.render(
        text,
        True,
        color
    )
    rectangulo_texto = texto_render.get_rect()
    rectangulo_texto.center = pos
    return (texto_render, rectangulo_texto)

def fusionar_texto(configs: dict, size: int, text: str, color: pg.Color, pos: tuple):
    texto_sup, texto_rect = crear_superficie_texto(
        size, 
        text,
        color,
        pos)

    configs.get('main_display').blit(texto_sup, texto_rect)

def dibujar_tarjeta_heroe(configs: dict, font_size: int):
    
    alto_minimo = [
        CENTER_SCREEN[1], 
        CENTER_SCREEN[1] + (font_size + 1) * 3 + font_size
    ]

    altura_pixeles = alto_minimo[1] - alto_minimo[0]

    padding = font_size // 2
    coordenadas_tarjeta = [CENTER_SCREEN[0] - 230, CENTER_SCREEN[1] - padding]
    dimensiones_tarjeta = [460, altura_pixeles + padding * 2] # ancho x alto
    
    dimensiones_rectangulo_tarj = coordenadas_tarjeta + dimensiones_tarjeta

    rect_tarjeta = pg.draw.rect(
        configs.get('main_display'), 
        pg.Color('grey'),
        dimensiones_rectangulo_tarj
    )

    fusionar_texto(
        configs, font_size, 
        f"Nombre: {configs.get('selected_hero_info').get('nombre')[:20]}",
        configs.get('color_texto'),
        CENTER_SCREEN)

    fusionar_texto(
        configs, font_size, 
        f"Alias: {configs.get('selected_hero_info').get('alias')[:20]}",
        configs.get('color_texto'),
        (CENTER_SCREEN[0], CENTER_SCREEN[1] + (font_size + 1)))
    
    fusionar_texto(
        configs, font_size, 
        f'Genero: {configs.get('selected_hero_info').get('genero')[:20]}',
        configs.get('color_texto'),
        (CENTER_SCREEN[0], CENTER_SCREEN[1] + (font_size + 1) * 2))
    
    fusionar_texto(
        configs, font_size, 
        f'Raza: {configs.get('selected_hero_info').get('raza')[:20]}',
        configs.get('color_texto'),
        (CENTER_SCREEN[0], CENTER_SCREEN[1] + (font_size + 1) * 3))

def run_game(game_name: str, heroes: list[dict]):

    pg.init()
    configs = set_main_game_configs(game_name)
    
    while configs.get('running_state'):

        manejador_de_eventos(configs, heroes)
        
        configs.get('main_display').fill(configs.get('color_fondo'))

        if configs.get('selected_hero_info') != None:
            

            # dibujar la tarjeta
            dibujar_tarjeta_heroe(configs, 20)

        pg.display.update()

    cerrar_juego()
    