import pygame as pg
import modules.variables as var

def create_base_form(dict_form_data: dict) -> dict:
    """ Crea la estructura base , comùn, a todos los formularios de las pantallas
    :params:
        dict_form_data -> claves elementales del formulario
    :returns:  form -> esqueleto del formulario """

    form = {}
    form['name'] = dict_form_data.get('name') # nombre del form -> "menu_form" | "ranking_form" | ...
    form['screen'] = dict_form_data.get('screen')
    form['active'] = dict_form_data.get('active') # es el que tengo que dijuar cuando esta activo
    form['x_coord'] = dict_form_data.get('coord')[0] # en que punto de la coordenada X tengo que dibujarlo
    form['y_coord'] = dict_form_data.get('coord')[1] # en que punto de la coordenada Y tengo que dibujarlo
    form['music_path'] = dict_form_data.get('music_path') # ruta del archivo de musica
    
    form['surface'] = pg.image.load(dict_form_data.get('background')).convert_alpha() # ruta de la imagen de fondo que tiene que cargar
    form['surface'] = pg.transform.scale(form.get('surface'), var.DIMENSION_PANTALLA) # <- ajusto la img al tamago de la pantalla 
    form['rect'] = form.get('surface').get_rect() # aca seteo la superficie rectangulo 

    form['rect'].x = dict_form_data.get('coord')[0] # seteo desde donde quiero que se empiece a dibujar
    form['rect'].y = dict_form_data.get('coord')[1]

    return form

def draw_widgets(form_data: dict):
    """ Dibuja en la pantalla los widgets (formularios) correspondientes 
    :params: form_data -> diccionario de formularios """

    for widget in form_data.get('widgets_list'):
        widget.draw()

def update_widgets(form_data: dict):
    """ Actualiza en la pantalla el estado de los widgets 
    :params: form_data -> diccionario de formularios """

    for widget in form_data.get('widgets_list'):
        widget.update()


def update(form_data: dict):
    """ Actualiza en la pantalla el estado de los widgets 
    :params: form_data -> diccionario de formularios """

    update_widgets(form_data)


def draw(form_data: dict):
    """ Fusiona en pantalla principal la superficie y los widgets que se veran en pantalla
    :params: form_data -> diccionario de formularios """

    form_data['screen']. blit(form_data.get('surface'), form_data.get('rect'))

