import pygame as pg
import modules.forms.menu_form as menu_form
import modules.variables as var
import modules.forms.ranking_form as ranking_form

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
    controller['enemy'] = None

# aca contengo todos los formularios que usa mi juego, y que contienen: Botones, rutas a sonidos, superficies, textos, etc...
    controller['forms_list'] = [
        menu_form.create_form_menu( # aca agrego el formulario de "Menu principal"
        {
            "name" : 'form_menu',
            "screen" : controller.get('main_screen'),
            "active" : True,
            "coord" : (0,0),
            "music_path" : '...',
            "background" : var.FONDO_MENU_IMG,
            "screen_dimensions" : var.DIMENSION_PANTALLA
        }),

        ranking_form.create_form_ranking(
        {
            "name" : 'form_ranking',
            "screen" : controller.get('main_screen'),
            "active" : False,
            "coord" : (0,0),
            "music_path" : '...',
            "background" : var.FONDO_RANKING_IMG,
            "screen_dimensions" : var.DIMENSION_PANTALLA
        })
    ] 
    return controller

def forms_update(form_controller: dict):
    """ Valida cual formulario està activo, lo actualiza y lo muestra en pantalla 
    :params: form_controller -> diccionario de formularios """

    lista_formularios = form_controller.get('forms_list')

    # Form "MENU"
    if lista_formularios[0].get('active'): # aca pregunto si el formulario de menu_form esta activo y lo llamo
        
        form_menu = lista_formularios[0]
        menu_form.update(form_menu) # <- lo actualizo
        menu_form.draw(form_menu) # <- y lo dibujo en pantalla
    
    # Form "RANKING"
    elif lista_formularios[1].get('active'): # aca pregunto si el formulario raking_form esta activo y lo llamo

        form_ranking = lista_formularios[1]
        ranking_form.update(form_ranking) # <- lo actualizo
        ranking_form.draw(form_ranking) # <- y lo dibujo en pantalla

def update(form_controller: dict):
    """ Valida cual formulario està activo, lo actualiza y lo muestra en pantalla 
    :params: form_controller -> diccionario de formularios """

    forms_update(form_controller)
