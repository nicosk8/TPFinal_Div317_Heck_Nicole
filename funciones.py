import pygame as pg
import sys
import time
import random as rd
import pantallas as sc 
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
        'fondo_menu_img' : FONDO_MENU_IMG,
        'menu_img_size': (50,150),
        'running_state': True,
        'selected_card_info': None
    }

    pg.display.set_caption(game_name) 
    pg.display.set_icon(configs.get('icono_surface'))
    
    return configs

def manejador_de_eventos(configs: dict, heroes: list[dict]):

    for event in pg.event.get():

        if event.type == pg.QUIT:
            configs['running_state'] = False
        
        if event.type == pg.MOUSEBUTTONDOWN:

            position = (event.pos)
            print(event)
            if event.button == 1:

                print('Click boton derecho')
                
                

                # aca tengo que validar evento click en alguna de las opciones del menu ?
                

                pass
                
def cerrar_juego():
    print('\n|---------------------------------------------------|')
    print('|  cerrando el juego... ¡Muchas gracias por jugar!  |')
    print('|---------------------------------------------------|\n')
    pg.quit()
    sys.exit()

