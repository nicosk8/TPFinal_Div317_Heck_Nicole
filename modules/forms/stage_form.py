import pygame as pg
import sys
import modules.forms.base_form as base_form
from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var
import modules.forms.pause_form as pause_form
import modules.stage as stage_juego

def create_form_stage(dict_form_data: dict) -> dict:
    """ Crea el formulario stage_form: puntajes, imagenes, posicion, musica, contador """

    form = base_form.create_base_form(dict_form_data)

    form['stage_restart'] = False # bandera para saber si debe reiniciar el juego o no
    form['time_finished'] = False # indicador de finalizacion de tiempo de juego
    form['actual_level'] = 1
    form['stage_timer'] = var.STAGE_TIMER # cantidad de seg desde donde arranca el juego
    form['last_timer'] = pg.time.get_ticks()
    form['bonus_shield_available'] = True
    form['bonus_heal_available'] = True
    form['bonus_shield_applied'] = False
    form['jugador'] = dict_form_data.get('jugador')
   
    form['stage'] = stage_juego.inicializar_stage(jugador=form.get('jugador'), pantalla=form.get('screen'),
                                                  nro_stage=form.get('actual_level')) 
    form['clock'] = pg.time.Clock() # 

    form['lbl_timer'] = Label(
        x=50, y=15,
        text=f'{form.get('stage_timer')}',
        screen= form.get('screen'),
        align= 'top-left',
        font_path= var.FONT_ALAGARD,
        font_size=30, color= pg.Color('white')
    )

    form['lbl_score'] = Label(
        x= 450, y=50,
        text=f'1500',
        screen= form.get('screen'),
        align= 'top-left',
        font_path= var.FONT_ALAGARD,
        font_size=30, color= pg.Color('white')
    )
    
    form['btn_play'] = Button( 
        x= var.DIMENSION_PANTALLA[0] // 2 + 175,
        y= var.DIMENSION_PANTALLA[0] // 2,
        text= 'JUGAR',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30,
        on_click= jugar_mano, on_click_param= form
    ) 

    form['widgets_list'] = [
        form.get('lbl_timer'),
        form.get('lbl_score'),
        form.get('btn_play')
    ]

    var.dict_forms_status[form.get('name')] = form 
    return form

def jugar_mano(form_dict_data: dict):
    """ Ejecuta la logica principal del juego:
            1 - Ejecuta la jugada de cartas 
            2 - compara daños 
            3 - Resta stats a los participantes 
            4 - Verifica el ganador de la ronda
            5 - Imprime el ganador de la ronda """
    stage = form_dict_data.get('stage')
    ganador_mano = stage_juego.jugar_mano(stage)
    print(f'El ganador de la mano es : {ganador_mano}')

def iniciar_nueva_partida(form_dict_data: dict):
    """ Funcion que setea las configs para una nueva partida """
    stage = form_dict_data.get('stage')
    jugador = form_dict_data.get('jugador')
    pantalla = form_dict_data.get('screen')
    nro_stage = stage.get('nro_stage')
    form_dict_data['stage'] = stage_juego.restart_stage(stage, jugador, pantalla, nro_stage)

def timer_update(dict_form_data: dict):
    """ Actualiza el tiempo restante de partida """

    if dict_form_data.get('stage_timer') > 0:

        tiempo_actual = pg.time.get_ticks() # capturo el tiempo actual en milisegs

        if (tiempo_actual - dict_form_data.get('last_timer')) > 1000:
            dict_form_data['stage_timer'] -= 1
            dict_form_data['last_timer'] = tiempo_actual

def events_handler(events: list[pg.event.Event]):
    """ Manejador de eventos del stage  """
    for event in events:

        if event.type == pg.KEYDOWN:
             if event.key == pg.K_ESCAPE:

                base_form.set_active('form_pause')

                # cuando se activa el form de pausa, le baja el sonido al minimo
                form_pause = var.dict_forms_status.get('form_pause')
                pause_form.save_last_volume(form_pause)
                 
def draw(form_dict_data: dict):
    """ Dibuja los widgets del formulario"""
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)
    stage_juego.draw_jugadores(form_dict_data.get('stage'))

def update(form_dict_data: dict, eventos: list[pg.event.Event]):
    """ Actualiza los widgets del formulario"""
    form_dict_data['lbl_timer'].update_text(f'{form_dict_data.get('stage_timer')}', pg.Color('white'))
    base_form.update(form_dict_data)
    events_handler(eventos)
    timer_update(form_dict_data)
    