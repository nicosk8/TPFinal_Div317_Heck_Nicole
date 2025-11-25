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

def create_form_options(dict_form_data: dict) -> dict:
    """ Crea el formulario "OPTIONS" desde donde se puede controlar 
    el volumen de la musica 
        1 - Levanta los del archivo ranking y carga una lista
        2 - Ordena e itera a lista
        3 - Dibuja los formularios """
    form = base_form.create_base_form(dict_form_data)
    

    form['lbl_titulo'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , # <- lo ubico en la mitad de la pantalla en el eje x 
        y= 115,
        text= 'OPCIONES',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        font_size= 75,
        color= pg.Color('red'),
    )

    # Aca voy a crear el boton "MUSIC ON"
    form['btn_music_on'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2 ,
        y= 270, # <- lo ubico 200 pixeles por debajo del texto "Menu principal"
        text='MUSIC ON',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD, 
        align= 'top-left', # <- punto superior izq desde donde se empieza a dibujar la superficie del boton
        font_size= 30,
        on_click= activar_musica, # <- llamado a la funcion que ejecuta la logica principal del juego
        on_click_param= form # <- transfiere parametros a la funcion
    )

    # Aca voy a crear el boton "MUSIC OFF"
    form['btn_music_off'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2 ,
        y= 300, # <- lo ubico 260 pixeles por debajo del texto "Menu principal"
        text='MUSIC OFF', 
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        align= 'top-left', # <- punto superior izq desde donde se empieza a dibujar la superficie del boton
        font_size= 30,
        on_click= desactivar_musica, # <- llamado a la funcion que ejecuta la logica principal del juego
        on_click_param= form # <- transfiere parametros a la funcion
    )

    form['btn_vol_down'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2 - 150,
        y= 335, # <- lo ubico 360 pixeles por debajo del texto "Menu principal"
        text='<', 
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        align= 'top-left', # <- punto superior izq desde donde se empieza a dibujar la superficie del boton
        font_size= 60,
        color= pg.Color('red'),
        on_click= modificar_volumen, 
        on_click_param=(-10) 
    )
    form['btn_vol_up'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2 + 150 ,
        y= 335, # <- lo ubico 360 pixeles por debajo del texto "Menu principal"
        text='>', 
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        align= 'top-left', # <- punto superior izq desde donde se empieza a dibujar la superficie del boton
        font_size= 60,
        color= pg.Color('red'),
        on_click= modificar_volumen, 
        on_click_param=10
    )

    form['lbl_vol'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , # <- lo ubico en la mitad de la pantalla en el eje x 
        y= 335, # <- lo ubico 360 pixeles por debajo del texto "Menu principal"
        text= f'{sonido.get_actual_volume()}',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        font_size= 35,
        color= pg.Color('blue'),
    )
    
    form['btn_volver'] = Button( # <- volver a la pantalla del menu principal
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 500,
        text= 'VOLVER',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30,
        on_click= cambiar_pantalla, on_click_param= 'form_menu' # <- tupla de parms con datos del form y nombre del formulario "MENU" = 'menu_form.py'
    )  

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_music_on'),
        form.get('btn_music_off'),
        form.get('btn_vol_down'),
        form.get('btn_vol_up'),
        form.get('lbl_vol'),
        form.get('btn_volver')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def modificar_volumen(volumen: int):
    """ Realiza calculo para aumentar o disminuir el volumen """

    vol_actual = sonido.get_actual_volume()

    print(f'\nMusica volumen actual -> {vol_actual}')
    print(f'>>> Valor del volumen a agregar/disminuir -> {volumen}')

    if  vol_actual > 0 and volumen < 0 or\
        vol_actual < 100 and volumen > 0:

        vol_actual += volumen # ej : 90 + 10 = 100 | 90 + (-10) = 80
        sonido.set_volume(vol_actual)

        if volumen > 0:
            print(f'Volumen aumentado -> {volumen}')
        else:
            print(f'Volumen disminuido -> {volumen}')
            


def activar_musica(form_dict_data : dict):
    """ Accede a la configuracion de la musica, y la enciende sin verificar, para todos los formularios"""
    form_dict_data['music_config']['music_on'] = True
    base_form.music_on(form_dict_data)

def desactivar_musica(form_dict_data: dict):
    """ Accede a la configuracion de la musica, y la apaga sin verificar, para todos los formularios """
    form_dict_data['music_config']['music_on'] = False
    sonido.stop_music()


def cambiar_pantalla(form_name: str):
    """ Realiza el cambio de pantalla del panel de opciones al menu principal 
    :params: form_name -> nombre del formulario : form_menu """
    base_form.set_active(form_name)

def draw(form_dict_data: dict):
    """ Dibuja en pantalla el formulario "OPTIONS" junto a sus widgets"""
    base_form.draw(form_dict_data) # fondo 
    base_form.draw_widgets(form_dict_data) # widgets

def update(form_dict_data: dict):
    """ Actualiza el formulario """
    lbl_vol: Label = form_dict_data.get('widgets_list')[5] # get('lbl_vol')
    lbl_vol.update_text(text=f'{sonido.get_actual_volume()}', color=pg.Color('white'))
    base_form.update(form_dict_data)