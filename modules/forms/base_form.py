import pygame as pg
import modules.variables as var
import modules.sonido as sonido


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
    form['music_config'] = dict_form_data.get('music_config')

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

def set_active(form_name: str):
    """ Activa un formulario 
    1 - Setea en False todos los formularios
    2 - Setea en True la clave del formulario que viene por parametro

    :params: 
        form_name -> nombre del formulario a activar """

    for form in var.dict_forms_status.values():
        form['active'] = False
    form_activo = var.dict_forms_status[form_name]
    form_activo['active'] = True
    music_off(form_activo) # freno una musica anterior, si habìa
    music_on(form_activo) # doy play a la musica propia del form activo

def music_on(form_dict_data: dict):
    """ Si no hay una musica activada, la configura y da play """
    
    if form_dict_data.get('music_config').get('music_on'):
        ruta_musica = form_dict_data.get('music_path')
        sonido.set_music_path(ruta_musica)
        sonido.play_music()

def music_off(form_dict_data: dict):
    """ Si hay una musica activada, la desactiva """

    if form_dict_data.get('music_config').get('music_off'):
        sonido.stop_music()

def cambiar_pantalla(form_name: str):
    """ Recibe el nombre de un formulario y lo ejecuta
    :params: form_name -> nombre del formualrio """
    
    print(f'Ingresando al formulario -> {form_name}')
    
    set_active(form_name)


def update(form_data: dict):
    """ Actualiza en la pantalla el estado de los widgets 
    :params: form_data -> diccionario de formularios """

    update_widgets(form_data)


def draw(form_data: dict):
    """ Fusiona en pantalla principal la superficie y los widgets que se veran en pantalla
    :params: form_data -> diccionario de formularios """

    form_data['screen']. blit(form_data.get('surface'), form_data.get('rect'))

