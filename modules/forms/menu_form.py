import pygame as pg
import sys
import modules.variables as var
import modules.forms.base_form as base_form
import modules.forms.stage_form as stage_form
from utn_fra.pygame_widgets import (
    Label , Button, ButtonSound, ButtonImageSound
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

    form['lbl_titulo_1'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , # <- lo ubico en la mitad de la pantalla en el eje x 
        y= 90,
        text= 'DBZ',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        font_size= 45,
        color= pg.Color('red'),
    )

    form['lbl_titulo_2'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , # <- lo ubico en la mitad de la pantalla en el eje x 
        y= 140,
        text= 'PLAYING CARDS',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        font_size= 45,
        color= pg.Color('red'),
    )

    form['lbl_menu'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 , # <- lo ubico en la mitad de la pantalla en el eje x 
        y= 300,
        text= 'MENU PRINCIPAL',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_path= var.FONT_ALAGARD,
        font_size= 35,
        color= pg.Color('red'),
    )

    # Aca voy a crear el boton "JUGAR"
    form['btn_play'] = ButtonImageSound(
        x= var.DIMENSION_PANTALLA[0] // 2 ,
        y= 350, # <- lo ubico 150 pixeles por debajo del texto "Menu principal"
        text='JUGAR',
        screen= form.get('screen'), # <- dimension de la pantalla
        align= 'top-left', # <- punto superior izq desde donde se empieza a dibujar la superficie del boton
        font_size= 30,
        sound_path=var.SONIDO_CLICK,image_path=var.IMG_BTN_PLAY, width=100,height=32,
        on_click= iniciar_stage, # <- llamado a la funcion que ejecuta la logica principal del juego
        on_click_param= 'form_stage' # <- transfiere parametros a la funcion
    )

    # Aca voy a crear el boton "RANKING"
    form['btn_ranking'] = ButtonImageSound(
        x= var.DIMENSION_PANTALLA[0] // 2 ,
        y= 390, # <- lo ubico 210 pixeles por debajo del texto "Menu principal"
        text='RANKING',
        screen= form.get('screen'), # <- dimension de la pantalla
        align= 'top-left', # <- punto superior izq desde donde se empieza a dibujar la superficie del boton
        font_size= 30, sound_path=var.SONIDO_CLICK,
        image_path=var.IMG_BTN_RANKING, width=100,height=32,
        on_click= base_form.cambiar_pantalla, # <- llamado a la funcion que ejecuta el cambio de pantalla a RANKING
        on_click_param= 'form_ranking' # <- transfiere parametros a la funcion
    )

    # Aca voy a crear el boton "OPCIONES"
    form['btn_options'] = ButtonImageSound(
        x= var.DIMENSION_PANTALLA[0] // 2 ,
        y= 430, # <- lo ubico 400 pixeles por debajo del texto "Menu principal"
        text='OPCIONES',
        screen= form.get('screen'), # <- dimension de la pantalla
        align= 'top-left', # <- punto superior izq desde donde se empieza a dibujar la superficie del boton
        font_size= 30, sound_path=var.SONIDO_CLICK,
        image_path=var.IMG_BTN_OPCIONES, width=100,height=32,
        on_click= base_form.cambiar_pantalla, # <- llamado a la funcion que ejecuta el cambio de pantalla a RANKING
        on_click_param= 'form_options'
    )

    # Aca voy a crear el boton "EXIT"
    form['btn_exit'] = ButtonImageSound(
        x= var.DIMENSION_PANTALLA[0] // 2 ,
        y= 495, # <- lo ubico 500 pixeles por debajo del texto "Menu principal"
        text='SALIR',
        screen= form.get('screen'), # <- dimension de la pantalla
        font_size= 30, sound_path=var.SONIDO_CLICK,
        image_path=var.IMG_BTN_SALIR, width=100,height=32,
        on_click= salir_juego, # <- llamado a la funcion que ejecuta la logica principal del juego
        on_click_param= '_' # <- transfiere parametros a la funcion
    )

    # Lista de widgets a dibujar en pantalla
    form['widgets_list'] = [
        form.get('lbl_titulo_1'),
        form.get('lbl_titulo_2'),
        form.get('lbl_menu'), # <- Titulo
        form.get('btn_play'), # <- Boton "JUGAR"
        form.get('btn_ranking'), # <- Boton "RANKING"
        form.get('btn_exit'),
        form.get('btn_options')
    ]

    # ahora, agrego el formulario para controlar cual form estoy activando y cual no.
    var.dict_forms_status[form.get('name')] = form  # <- el nombre del formulario activo en el momento + sus valores
    return form

def iniciar_stage(form_name: str):
    """ Boton de entrada al juego. """
    print(f'Ingresando al form -> {form_name}')
    print('Estamos presionando el boton "JUGAR"...')
    base_form.cambiar_pantalla(form_name)
    form_stage = var.dict_forms_status.get(form_name)
    stage_form.iniciar_nueva_partida(form_stage)



def salir_juego(_):
    """ Termina la ejecuciòn del juego """
    print('\n|---------------------------------------------------|')
    print('|  cerrando el juego... ¡Muchas gracias por jugar!  |')
    print('|---------------------------------------------------|\n')
    pg.quit()
    sys.exit()


def draw(dict_form_data: dict):
    """ Dibuja en pantalla el fondo y los widgets """
    base_form.draw(dict_form_data) # <- dibuja la imagen de fondo
    base_form.draw_widgets(dict_form_data) # <- dibuja los botones y labels (widgets)


def events_handler():
    """ Manejador de eventos del menu"""
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            salir_juego()
         

def update(dict_form_data: dict):
    """ Actualiza en pantalla el fondo y los widgets """
    events_handler()
    base_form.update(dict_form_data)
    if not dict_form_data.get('music_config').get('music_init'):
        base_form.music_on(dict_form_data)
        dict_form_data['music_config']['music_init'] = True
        
