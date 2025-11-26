import pygame as pg
import modules.variables as var
import modules.forms.base_form as base_form
import modules.load_data as load_data
import modules.forms.stage_form as stage_form
import modules.participante as participante_juego
from utn_fra.pygame_widgets import (
    Label , Button, TextBox
)

def create_form_name(dict_form_data: dict) -> dict:
    """ """

    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = dict_form_data.get('jugador')
    form['info_submitida'] = False
    form['lbl_titulo'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , 
        y= 100,
        text= '',
        screen= form.get('screen'), 
        font_path= var.FONT_ALAGARD,
        font_size= 35,
        color= pg.Color('green'),
    )

    form['lbl_subtitulo'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , 
        y= 150,
        text= 'Escriba su nombre:',
        screen= form.get('screen'), 
        font_path= var.FONT_ALAGARD,
        font_size= 35,
        color= pg.Color('red'),
    )

    form['lbl_score'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , 
        y= 210,
        text= f'{participante_juego.get_score_participante(form.get('jugador'))}',
        screen= form.get('screen'), 
        font_path= var.FONT_ALAGARD,
        font_size= 35,
        color= pg.Color('red'),
    )

    form['lbl_nombre_texto'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , 
        y= 270,
        text= '',
        screen= form.get('screen'), 
        font_path= var.FONT_ALAGARD,
        font_size= 35,
        color= pg.Color('blue'),
    )

    form['text_box'] = TextBox(
        x= var.DIMENSION_PANTALLA[0] // 2 , y= 280,
        text=f'_____________________________________', screen=form.get('screen'),
        font_path= var.FONT_ALAGARD, font_size= 25, color= pg.Color('blue')
    )   

    form['btn_submit'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2 ,
        y= 370, 
        text='CONFIRMAR NOMBRE',
        screen= form.get('screen'), 
        font_path= var.FONT_ALAGARD,
        align= 'top-left', 
        font_size= 30,
        on_click= submit_name, 
        on_click_param= form 
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('lbl_score'),
        form.get('lbl_nombre_texto'),
        form.get('btn_submit')         
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def update_background_victory_defeat(form_data: dict, win_status: bool):
    """ Actualiza el background segùn el jugador haya ganado o perdido la partida """

    if win_status:
        form_data['background'] = var.FONDO_VICTORY_IMG 
    else:
        form_data['background'] = var.FONDO_DEFEAT_IMG

    form_data['surface'] = pg.image.load(form_data.get('background')).convert_alpha() # ruta de la imagen de fondo que tiene que cargar
    form_data['surface'] = pg.transform.scale(form_data.get('surface'), var.DIMENSION_PANTALLA) # <- ajusto la img al tamago de la pantalla 
    form_data['rect'] = form_data.get('surface').get_rect() # aca seteo la superficie rectangulo 

#    form_data['rect'].x = form_data.get('coord')[0] # seteo desde donde quiero que se empiece a dibujar
#    form_data['rect'].y = form_data.get('coord')[1]



def update_texto_victoria(form_data: dict, win_status: bool):
    """ Actualiza el titulo segun el jugador haya ganado o perdido la partida """
   
    if win_status:
        mensaje = 'VICTORIA!'
        color_texto = pg.Color('green')

    else: 
        mensaje = 'DERROTA'
        color_texto = pg.Color('red')

    form_data.get('widgets_list')[0].update_text(text=mensaje, color=color_texto)

def clear_text(form_data: dict):
    """ """
    form_data['text_box'].writing = ''

def submit_name(form_data: dict):
    """ Captura el texto ingresado por el usuario y redirreciona a la pantalla de ranking.
        1 - Setea el nombre
        2 - Captura el puntaje del jugador
        3 - Guarda datos en un archivo .csv
        4 - Activa el formulario ranking """
    nombre_jugador = form_data.get('lbl_nombre_texto').text
    participante_juego.set_nombre_participante(form_data.get('jugador'), nombre_jugador)

    nombre_jugador_seteado = participante_juego.get_nombre_participante(form_data.get('jugador'))
    puntaje_jugador = participante_juego.get_score_participante(form_data.get('jugador'))
    print(f'NOMBRE JUGADOR: {nombre_jugador_seteado} - {puntaje_jugador}')
    data_to_csv = participante_juego.info_to_csv(form_data.get('jugador'))
    load_data.guardar_info_csv(data_to_csv)

    form_data['info_submitida'] = True
    clear_text(form_data)
    base_form.set_active('form_ranking')

def update(form_dict_data: dict, event_list: list[pg.event.Event]):

#    update_background_victory_defeat(form_dict_data) # falta completar esta parte 
    form_dict_data['score'] = participante_juego.get_score_participante(form_dict_data.get('jugador'))

    form_dict_data.get('widgets_list')[2].update_text(text=f'SCORE: {form_dict_data.get("score")}', color=pg.Color('red'))
    form_dict_data.get('widgets_list')[3].update_text(text=f'{form_dict_data.get('text_box').writing.upper()}', color=pg.Color('blue'))

    form_dict_data.get('text_box').update(event_list)
    base_form.update(form_dict_data)

def draw(form_data: dict):
    base_form.draw(form_data)
    base_form.draw_widgets(form_data)
    form_data.get('text_box').draw()