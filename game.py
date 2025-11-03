import pygame as pg
import sys
import time
import random as rd
import pantallas 
from variables import (
    ASPECT_RATIO, CENTER_SCREEN, PATH_ICON_IMG,
    FUENTE_ALAGARD, POS_FONDO_MENU_IMG
)

from funciones import(
    set_main_game_configs, manejador_de_eventos, cerrar_juego, 
)

def run_game(game_name: str, heroes: list[dict]):

    pg.init()
    configs = set_main_game_configs(game_name)
    
    while configs.get('running_state'):
        
        

        manejador_de_eventos(configs, heroes)
        pantallas.armar_background_menu(configs)

        if configs.get('selected_hero_info') != None:
            
            pass
            

        pg.display.update()

    cerrar_juego()
    