import pygame as pg
import modules.variables as var
import modules.assets
import modules.forms.base_form as base_form
from utn_fra.pygame_widgets import (
    Label , # <- class
    Button, # <- boton simple
)

def create_form_menu(dict_form_data: dict) -> dict:
    """ Crea el formulario de la pantalla "Menu" con los datos del juego.
     1 - ejecuta funcion que crea la plantilla -> create_base_form(dict_form_data) [traido desde modules.forms.base_form] 
      para crear el formulario "form" y asignarle los valores obtenidos en el parm dict_form_data: dict 
    2 - En el formulario que creo, arma claves que seran los widgets que se dibujaran en pantalla y
      accionaran las funcionalidades correspondientes al menu de inicio.
      
    :params: dict_form_data -> datos del juego 
    :returns: form -> """

    form = base_form.create_base_form(dict_form_data)

    form['lbl_titulo'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , # <- lo ubico en la mitad de la pantalla en el eje x 
        y= 100,
        text= 'Menu principal',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        font_size= 35,
        color= pg.Color('red'),
    )

    # Aca voy a crear el boton "JUGAR"
    form['btn_play'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2 ,
        y= 150, # <- lo ubico 50 pixeles por debajo del texto "Menu principal"
        text='JUGAR',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        font_size= 30,
        on_click= None, 
        on_click_param= None # <- llamado a la funcion que ejecuta la logica principal del juego
    )

    # Lista de widgets a dibujar en pantalla
    form['widgets_list'] = [
        form.get('lbl_titulo'), # <- Titulo
        form.get('btn_play') # <- Boton "JUGAR"
    ]

    # ahora, agrego el formulario para controlar cual form estoy activando y cual no.
    var.dict_forms_status[form.get('name')] = form  # <- el nombre del formulario activo en el momento + sus valores
    return form

def draw(dict_form_data: dict):
    """ Dibuja en pantalla el fondo y los widgets """
    base_form.draw(dict_form_data) # <- dibuja la imagen de fondo
    base_form.draw_widgets(dict_form_data) # <- dibuja los botones y labels (widgets)

def update(dict_form_data: dict):
    """ Actualiza en pantalla el fondo y los widgets """
    base_form.update(dict_form_data)

