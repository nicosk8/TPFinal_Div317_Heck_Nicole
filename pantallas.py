import pygame as pg
import sys
import time
import random as rd
from variables import (
    ASPECT_RATIO, CENTER_SCREEN, PATH_ICON_IMG,
    FUENTE_ALAGARD, COLORES, FONDO_MENU_IMG, POS_FONDO_MENU_IMG
)
   

def crear_superficie_texto(texto: str, size: int, color: dict, configs: dict, position : tuple) -> tuple:
    """ Arma una superficie con texto  """

    texto = pg.font.SysFont('Arial', size)
#    texto_render = texto.render(texto, True, color.get('negro'))
    texto_render = texto.render('Dragon Ball Z - Playing cards', True, color.get('negro'))
    rectangulo_texto = texto_render.get_rect()
    rectangulo_texto.center = position
    return (texto_render, rectangulo_texto)

def armar_background_menu(configs: dict):
    """ Rellena el fondo principal y le carga una imagen de fondo 
    :params: config -> configuraciones """
    
    configs.get('main_display').fill(configs.get('color_fondo'))
    fondo_menu_img = pg.image.load(configs.get('fondo_menu_img'))
    rect_fondo_menu_img = fondo_menu_img.get_rect()
    configs.get('main_display').blit(source=fondo_menu_img,dest=POS_FONDO_MENU_IMG, area=rect_fondo_menu_img)
    fondo_menu_img = pg.transform.scale(surface=fondo_menu_img, size= configs.get('menu_img_size'))
    #fondo_menu_img = pg.transform.scale_by(fondo_menu_img, 0.1)

    # Armo el rect + titulo
    texto_superficie, texto_rect = crear_superficie_texto('Dragon Ball Z - Playing cards',
                                                           40, COLORES, configs, (CENTER_SCREEN[0],CENTER_SCREEN[1] - 150))
    configs.get('main_display').blit(texto_superficie, texto_rect)

    texto = pg.font.SysFont('Arial', 35)
#    texto_render = texto.render(texto, True, color.get('negro'))
    texto_render = texto.render('Main menu', True, COLORES.get('negro'))
    rectangulo_texto = texto_render.get_rect()
#    rectangulo_texto.center = (387, 360)
    rectangulo_texto.center = (CENTER_SCREEN[0],CENTER_SCREEN[1] - 80)
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    texto = pg.font.SysFont('Arial', 25)
#    texto_render = texto.render(texto, True, color.get('negro'))
    texto_render = texto.render('START', True, COLORES.get('negro'))
    rectangulo_texto = texto_render.get_rect()
#    rectangulo_texto.center = (387, 360)
    rectangulo_texto.center = CENTER_SCREEN
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    texto = pg.font.SysFont('Arial', 25)
#    texto_render = texto.render(texto, True, color.get('negro'))
    texto_render = texto.render('OPTIONS', True, COLORES.get('negro'))
    rectangulo_texto = texto_render.get_rect()
#    rectangulo_texto.center = (387, 406)
    rectangulo_texto.center = (CENTER_SCREEN[0],CENTER_SCREEN[1] + 60)
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    texto = pg.font.SysFont('Arial', 25)
#    texto_render = texto.render(texto, True, color.get('negro'))
    texto_render = texto.render('RANKING', True, COLORES.get('negro'))
    rectangulo_texto = texto_render.get_rect()
#    rectangulo_texto.center = (387, 446)
    rectangulo_texto.center = (CENTER_SCREEN[0],CENTER_SCREEN[1] + 120)
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    texto = pg.font.SysFont('Arial', 25)
#    texto_render = texto.render(texto, True, color.get('negro'))
    texto_render = texto.render('EXIT', True, COLORES.get('negro'))
    rectangulo_texto = texto_render.get_rect()
#    rectangulo_texto.center = (387, 484)
    rectangulo_texto.center = (CENTER_SCREEN[0],CENTER_SCREEN[1] + 235)
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    
    

def menu_opciones():

    armar_background_menu