import pygame as pg
import sys
import time
import random as rd
from variables import (
    ASPECT_RATIO, CENTER_SCREEN, PATH_ICON_IMG,
    FUENTE_ALAGARD, COLORES, FONDO_MENU_IMG, POS_FONDO_MENU_IMG
)


def set_main_game_configs(game_name: str) -> dict:
    """ Configuraciones de inicio: 
            Arma la superficie (ventana) principal de la aplicacion
    :params: 
        game_name -> titulo string que se visualiza al lado del icono de joystick
    :returns: 
        configs -> dict de configuraciones  """

    configs = {
       'icono_surface': pg.image.load(PATH_ICON_IMG),
#        'main_display': pg.display.set_mode(ASPECT_RATIO, pg.RESIZABLE),
        'main_display': pg.display.set_mode(ASPECT_RATIO),
        'color_fondo': COLORES.get('rosa'),
        'fondo_menu_img' : FONDO_MENU_IMG, #<- fondo donde voy a escribir el menu
        'menu_img_size': (50,150),
        'running_state': True,
        'selected_card_info': None
    }

    pg.display.set_caption(game_name) 
    pg.display.set_icon(configs.get('icono_surface'))
    

    return configs

def armar_background_menu(configs: dict):
    """ Rellena el fondo principal y le carga una imagen de fondo 
    :params: config -> configuraciones """
    
    configs.get('main_display').fill(configs.get('color_fondo'))
    fondo_menu_img = pg.image.load(configs.get('fondo_menu_img'))
    rect_fondo_menu_img = fondo_menu_img.get_rect()
    configs.get('main_display').blit(source=fondo_menu_img,dest=POS_FONDO_MENU_IMG, area=rect_fondo_menu_img)
    fondo_menu_img = pg.transform.scale(surface=fondo_menu_img, size= configs.get('menu_img_size'))
    #fondo_menu_img = pg.transform.scale_by(fondo_menu_img, 0.1)

    armar_menu_titulo_texto()

def armar_menu_titulo_texto():   

    texto = pg.font.SysFont('Arial',35)
    texto_render = texto.render('Dragon Ball Z cards - Menu principal', True ,pg.Color('black'))
    rectangulo_texto = texto_render.get_rect()
    rectangulo_texto.center = CENTER_SCREEN 

def manejador_de_eventos(configs: dict, heroes: list[dict]):

    for event in pg.event.get():

        if event.type == pg.QUIT:
            configs['running_state'] = False
        
        if event.type == pg.MOUSEBUTTONDOWN:
            print(event)
            if event.button == 1:

                random_index_list = rd.randint(0, len(heroes) - 1)
#                background_color_name = rd.choice(['cyan', 'red', 'blue', 'pink'])
                background_color_name = 'pink'
                color_random_name = 'black'

                configs['color_fondo'] = pg.Color(background_color_name)
                configs['color_texto'] = pg.Color(color_random_name)

                configs['selected_hero_info'] = heroes[random_index_list]
                

def cerrar_juego():
    print('\n|---------------------------------------------------|')
    print('|  cerrando el juego... ¡Muchas gracias por jugar!  |')
    print('|---------------------------------------------------|\n')
    pg.quit()
    sys.exit()

