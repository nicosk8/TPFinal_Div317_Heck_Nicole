import pygame as pg
import sys
import modules.variables as var
import modules.assets
import modules.forms.base_form as base_form
import modules.forms.stage_form as form_stage
import modules.load_data as load_data
import modules.sonido as sonido
from utn_fra.pygame_widgets import (
    Label , Button, ButtonSound
)

def create_form_pause(dict_form_data: dict) -> dict:

    """ Cuando el usuario presiona la tecla ESCAPE, se crea el formulario "PAUSE",
        si hay musica, el volumen de lo setea al minimo. Y muestra la siguientes 
        opciones disponibles:
            1 - Resume : resumir la partida
            2 - Restart : reiniciar la partida
    """

    form = base_form.create_base_form(dict_form_data)
    form['last_volume'] = None
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
        font_size= 30,
        color= pg.Color('red'),
    )

    form['btn_resume'] = ButtonSound( 
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 210,
        text= 'RESUME',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30, sound_path=var.SONIDO_CLICK,
        on_click= cambiar_pantalla, on_click_param= {'form': form, 'form_name': 'form_stage'} )

    form['btn_restart'] = ButtonSound( 
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 270,
        text= 'RESTART STAGE',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30, sound_path=var.SONIDO_CLICK,
        on_click= restart_stage, on_click_param= {'form': form,'form_name': 'form_stage'})
     
    form['btn_back_menu'] = ButtonSound( 
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 495,
        text= 'BACK TO MENU',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30, sound_path=var.SONIDO_CLICK,
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

def cambiar_pantalla(params: dict):
    """ Cuando el user oprime la tecla de pausa, el volumen se establece al minimo
    y se ejecuta el cambio de pantalla al panel de pausa """

    last_vol = params.get('form').get('last_volume')
    base_form.cambiar_pantalla(params.get('form_name'))
    set_last_volume(last_vol)

def restart_stage(params: dict):
    """ Reinicia la partida """
    stage_form = var.dict_forms_status.get(params.get('form_name'))
    cambiar_pantalla(params)
    form_stage.iniciar_nueva_partida(stage_form)
    form_stage.clear_lbls_card_info(stage_form)



def set_last_volume(vol: int):
    """ Establece el nivel de volumen en 10 """
    sonido.set_volume(vol)

def save_last_volume(form_dict_data: dict):
    """ Establece el nivel de volumen en 10 y lo guarda """
    form_dict_data['last_volume'] = sonido.get_actual_volume()
    set_last_volume(10)

def draw(form_dict_data: dict):
    """ Dibuja la superficie y widgets de las funcionalidades de pausa """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict):
    """ Actualiza widgets de las funcionalidades de pausa """
    base_form.update(form_dict_data)





