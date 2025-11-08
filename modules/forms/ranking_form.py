import pygame as pg
import sys
import modules.variables as var
import modules.assets
import modules.forms.base_form as base_form
import modules.load_data as load_data
from utn_fra.pygame_widgets import (
    Label , # <- class
    Button, # <- boton simple
)

def create_form_ranking(dict_form_data: dict) -> dict:
    """ Crea el formulario "ranking" de totales 
        1 - Levanta los del archivo ranking y carga una lista
        2 - Ordena e itera a lista
        3 - Dibuja los formularios """
    form = base_form.create_base_form(dict_form_data)

    
    form['lista_ranking_file'] = [] # <- lista con los datos de trabajo
    form['lista_ranking_GUI'] = [] # <- lista con los labels : [posicion , nombre, puntaje]

    form['lbl_titulo'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y=50,
        text= 'DBZ Playing Cards',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 70
    )


    form['lbl_subtitulo'] = Label( # <- sub titulo : "TOP SCORE RANKING"
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 130,
        text= 'TOP 10 RANKING SCORE',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 50
    ) 


    form['btn_volver'] = Button( # <- volver a la pantalla del menu principal
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 550,
        text= 'VOLVER',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30,
        on_click= cambiar_pantalla , on_click_param= (form, 'form_menu') # <- tupla de parms con datos del form y nombre del formulario "MENU" = 'menu_form.py'
    )  

    form['data_loaded'] = False

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_volver')  
    ]
    var.dict_forms_status[form.get('name')] = form 
    return form 

def cambiar_pantalla(param_list : tuple):
    """ Recibe el nombre de un formulario y lo ejecuta.
        1 - Muestra un mensaje de salida
        2 - Establece en False la carga de datos
        3 - LLamado a funcion de cambio de pantalla
    :params: 
        form_ranking -> datos del formulario
        form_name -> nombre del formualrio """

    form_ranking, form_name = param_list # <- desempaqueto los datos

    print('Saliendo del formulario -> "RANKING" ...')
    form_ranking['data_loaded'] = False

    base_form.cambiar_pantalla(form_name)

def draw(form_dict_data: dict):
    """ Dibuja la pantalla del formulario RANKING y sus widgets 
    :params: form_dict_data -> datos del formulario"""
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)
    

def update(form_dict_data: dict):

    if form_dict_data.get('data_loaded'):
        pass
    base_form.update(form_dict_data)
