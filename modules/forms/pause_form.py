import pygame as pg
import sys
import modules.variables as var
import modules.assets
import modules.forms.base_form as base_form
import modules.load_data as load_data
import modules.sonido as sonido
from utn_fra.pygame_widgets import (
    Label , # <- class
    Button, # <- boton simple
)

def create_form_pause(dict_form_data: dict) -> dict:
    """ Crea el formulario "OPTIONS" desde donde se puede controlar 
    el volumen de la musica 
        1 - Levanta los del archivo ranking y carga una lista
        2 - Ordena e itera a lista
        3 - Dibuja los formularios """
    form = base_form.create_base_form(dict_form_data)

    form['lbl_titulo'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , # <- lo ubico en la mitad de la pantalla en el eje x 
        y= 100,
        text= var.TITULO_JUEGO,
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        font_size= 40,
        color= pg.Color('red'),
    )

    form['lbl_subtitulo'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , # <- lo ubico en la mitad de la pantalla en el eje x 
        y= 160,
        text= 'PAUSE',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        font_size= 35,
        color= pg.Color('red'),
    )

    form['btn_resume'] = Button( 
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 210,
        text= 'RESUME',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30,
        on_click= base_form.cambiar_pantalla, on_click_param= 'form_menu')

    form['btn_restart'] = Button( 
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 270,
        text= 'RESTART STAGE',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30,
        on_click= None, on_click_param= None)
     
    form['btn_back_menu'] = Button( 
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 550,
        text= 'BACK TO MENU',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30,
        on_click= base_form.cambiar_pantalla, on_click_param= 'form_menu') 
    
    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_resume'),
        form.get('btn_restart'),
        form.get('btn_back_menu')
    ]

    var.dict_forms_status[form.get('name')] = form
    return form 

def draw(form_dict_data: dict):
    """ Dibuja la superficie y widgets de las funcionalidades de pausa """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict):
    """ Actualiza widgets de las funcionalidades de pausa """
    base_form.update(form_dict_data)

# logica funciones de los btn



