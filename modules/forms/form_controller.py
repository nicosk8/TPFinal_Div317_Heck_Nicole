import pygame as pg
import modules.forms.menu_form as menu_form
import modules.variables as var
import modules.forms.ranking_form as ranking_form
import modules.forms.options_form as options_form
import modules.forms.pause_form as pause_form
import modules.forms.stage_form as stage_form

def create_form_controller(screen: pg.Surface, datos_juego: dict):
    """ Funcion creadora de formularios 
    :params:
        screen -> donde se tiene que empezar a dibujar la pantalla 
        datos_juego -> los datos del juego (ej.: cantidad de vida del jugador, puntale inicial, etc...) 
                       Informacion basica para que arranque el juego 
    :returns: controller -> formulario """
    
    controller = {} # contiene botones, imagenes, niveles, etc...
    controller['main_screen'] = screen
    controller['current_stage'] = 1
    controller['game_started'] = False
    controller['player'] = datos_juego.get('player')
    controller['music_config'] = datos_juego.get('music_config')

# aca contengo todos los formularios que usa mi juego, y que contienen: Botones, rutas a sonidos, superficies, textos, etc...
    controller['forms_list'] = [
        menu_form.create_form_menu( # aca agrego el formulario de "Menu principal"
        {
            "name" : 'form_menu',
            "screen" : controller.get('main_screen'),
            "active" : True,
            "coord" : (0,0),
            "music_path" : var.MUSICA_MENU,
            "background" : var.FONDO_MENU_IMG,
            "screen_dimensions" : var.DIMENSION_PANTALLA,
            "music_config" : controller.get('music_config')
        }),

        ranking_form.create_form_ranking(
        {
            "name" : 'form_ranking',
            "screen" : controller.get('main_screen'),
            "active" : False,
            "coord" : (0,0),
            "music_path" : var.MUSICA_RANKING,
            "background" : var.FONDO_RANKING_IMG,
            "screen_dimensions" : var.DIMENSION_PANTALLA,
            "music_config" : controller.get('music_config')
        }),

        options_form.create_form_options(
        {
            "name" : 'form_options',
            "screen" : controller.get('main_screen'),
            "active" : False,
            "coord" : (0,0),
            "music_path" : var.MUSICA_OPTIONS,
            "background" : var.FONDO_OPCIONES_IMG,
            "screen_dimensions" : var.DIMENSION_PANTALLA,
            "music_config" : controller.get('music_config')
        }),

        pause_form.create_form_pause(
        {
            "name" : 'form_pause',
            "screen" : controller.get('main_screen'),
            "active" : False,
            "coord" : (0,0),
            "music_path" : var.MUSICA_PAUSA,
            "background" : var.FONDO_PAUSA_IMG,
            "screen_dimensions" : var.DIMENSION_PANTALLA,
            "music_config" : controller.get('music_config')
        }
        ),
        stage_form.create_form_stage(
        {
            "name" : 'form_stage',
            "screen" : controller.get('main_screen'),
            "active" : False,
            "coord" : (0,0),
            "music_path" : var.MUSICA_STAGE,
            "background" : var.FONDO_STAGE_IMG,
            "screen_dimensions" : var.DIMENSION_PANTALLA,
            "music_config" : controller.get('music_config'),
            "jugador" :  controller.get('player')
        }
        )

    ] 
    return controller

def forms_update(form_controller: dict, eventos: list[pg.event.Event]):
    """ ESTE ES EL CORE DEL MANEJO DE EJECUION DE LOS FORMULARIOS.
    Valida cual formulario està activo, lo actualiza y lo muestra en pantalla 
    :params: form_controller -> diccionario de formularios """

    lista_formularios = form_controller.get('forms_list')
        
    for form in lista_formularios:
        if form.get('active'):
            match form.get('name'):
                case 'form_menu':
                    form_menu = lista_formularios[0]
                    menu_form.update(form_menu)
                    menu_form.draw(form_menu)
                case 'form_ranking':
                    form_ranking = lista_formularios[1]
                    ranking_form.update(form_ranking)
                    ranking_form.draw(form_ranking)
                case 'form_options':
                    form_options = lista_formularios[2]
                    options_form.update(form_options)
                    options_form.draw(form_options)
                case 'form_pause':
                    form_pause = lista_formularios[3]
                    pause_form.update(form_pause)
                    pause_form.draw(form_pause)
                case 'form_stage':
                    form_stage = lista_formularios[4]
                    stage_form.update(form_stage, eventos)
                    pause_form.draw(form_stage)
                    stage_form.draw(form_stage)
                    


def update(form_controller: dict, eventos: list[pg.event.Event]):
    """ Valida cual formulario està activo, lo actualiza y lo muestra en pantalla 
    :params: form_controller -> diccionario de formularios """

    forms_update(form_controller, eventos)
