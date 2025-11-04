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
    texto_render = texto.render('Dragon Ball Z - Playing cards', True, color.get('negro'))

    #print(f'Tipo de texto -> {type(texto)}') # Tipo de texto -> <class 'pygame.font.Font'>

    #texto_render = texto.render(texto, True, color.get('negro')) # <- OJO ESTOY IMPRIENDO SIN FORMATO

    rectangulo_texto = texto_render.get_rect()
    rectangulo_texto.center = position
    return (texto_render, rectangulo_texto)

def fusionar_texto(configs: dict, texto_superficie, rectangulo_texto):  
    """ Fusiona el texto con la superficie de la pantalla 
    :params: 
        configs -> configuraciones
        texto_superficie -> texto 
        rectangulo_texto -> rectangulo invisible que contiene al texto """
    configs.get('main_display').blit(texto_superficie, rectangulo_texto) 

def armar_background(configs: dict, color_fondo: str, imagen: str):
    """ Rellena el fondo principal y le carga una imagen de fondo 
    :params: config -> configuraciones """
    
    configs.get('main_display').fill(configs.get(color_fondo))
    fondo_menu_img = pg.image.load(configs.get(imagen))
    rect_fondo_menu_img = fondo_menu_img.get_rect()
    configs.get('main_display').blit(source=fondo_menu_img,
                                     dest=POS_FONDO_MENU_IMG, 
                                     area=rect_fondo_menu_img)
    
    fondo_menu_img = pg.transform.scale(surface=fondo_menu_img, size= configs.get('menu_img_size'))
    #fondo_menu_img = pg.transform.scale_by(fondo_menu_img, 0.1) # <- no me toma el escalado a la img

def armar_tarjeta_rectangulo(configs: dict, colores: dict, color_tarjeta: str, pos: tuple, ancho: int, alto: int):

    coordenadas_tarjeta = [pos[0] - 230 , pos[1] - 30] # coordenada (-230, -30)
    dimensiones_tarjeta = [ancho,alto] # 300 , 170
    dimensiones_rect_tarjeta = coordenadas_tarjeta + dimensiones_tarjeta

    rectangulo_tarjeta = pg.draw.rect(
                                configs.get('main_display'),
                                colores.get(color_tarjeta),
                                dimensiones_rect_tarjeta)
    return rectangulo_tarjeta
# _______________________________________________________________________________________________

def armar_pantalla_menu_principal(configs: dict):
    """ Arma la pantalla del menu principal 
    :params: configs -> configuraciones"""

    # armo el fondo con la imagen y el color
    armar_background(configs,
                     color_fondo='color_fondo',
                     imagen='fondo_menu_img' )
    
    
    

    # Armo el menu principal : texto + superficie de texto + posicion en la pantalla

    texto = 'Dragon Ball Z - Playing cards' # <- OJO ESTO NO ESTA FUNCIONANDO, ESTA VALOR ESTA HARDCODED DENTRO EN LA FUNCION
    texto_superficie, texto_rect = crear_superficie_texto(texto, 40,
                                                        COLORES, configs,
                                                        (CENTER_SCREEN[0],CENTER_SCREEN[1] - 150))
    fusionar_texto(configs, texto_superficie, texto_rect)

    # REPITO ESTE CODIGO PORQUE LA FUNCION "crear_superficie_texto(texto, ....)" rompe cuando con ese parm
    texto = pg.font.SysFont('Arial', 35)
    texto_render = texto.render('Main menu', True, COLORES.get('negro'))
    rectangulo_texto = texto_render.get_rect()
    rectangulo_texto.center = (CENTER_SCREEN[0],CENTER_SCREEN[1] - 80)
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    
    texto = pg.font.SysFont('Arial', 25)
    texto_render = texto.render('START', True, COLORES.get('negro'))
    rectangulo_texto = texto_render.get_rect()
    rectangulo_texto.center = CENTER_SCREEN
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    texto = pg.font.SysFont('Arial', 25)
    texto_render = texto.render('OPTIONS', True, COLORES.get('negro')) # coordenadas_tarjeta = [center_screen[0] - 50 , center_screen[1] + 40]
    rectangulo_texto = texto_render.get_rect()
    rectangulo_texto.center = (CENTER_SCREEN[0],CENTER_SCREEN[1] + 60)
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    texto = pg.font.SysFont('Arial', 25)
    texto_render = texto.render('RANKING', True, COLORES.get('negro'))
    rectangulo_texto = texto_render.get_rect()
    rectangulo_texto.center = (CENTER_SCREEN[0],CENTER_SCREEN[1] + 120)
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    texto = pg.font.SysFont('Arial', 25)
    texto_render = texto.render('EXIT', True, COLORES.get('negro'))
    rectangulo_texto = texto_render.get_rect()
    rectangulo_texto.center = (CENTER_SCREEN[0],CENTER_SCREEN[1] + 235)
    configs.get('main_display').blit(texto_render, rectangulo_texto)

    #armar_tarjeta_rectangulo(configs, COLORES, color_tarjeta='amarillo',pos=CENTER_SCREEN, ancho= 300, alto=170)

