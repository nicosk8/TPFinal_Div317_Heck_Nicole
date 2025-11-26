import pygame as pg
import sys
import modules.variables as var
import modules.assets
import modules.forms.base_form as base_form
import modules.load_data as load_data
from utn_fra.pygame_widgets import (
    Label , # <- class
    Button, # <- boton simple
)

def create_form_ranking(dict_form_data: dict) -> dict:
    """ Crea el formulario "ranking" de totales 
        1 - Levanta los del archivo ranking y carga una lista
        2 - Ordena e itera a lista
        3 - Dibuja los formularios """
    form = base_form.create_base_form(dict_form_data)

    
    form['lista_ranking_file'] = [] # <- lista con los datos de trabajo
    form['lista_ranking_GUI'] = [] # <- lista con los labels : [posicion , nombre, puntaje]

    form['lbl_titulo'] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2,
        y=50,
        text= 'DBZ Playing Cards',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 70
    )


    form['lbl_subtitulo'] = Label( # <- sub titulo : "TOP SCORE RANKING"
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 130,
        text= 'TOP 7 RANKING SCORE',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 50
    ) 


    form['btn_volver'] = Button( # <- volver a la pantalla del menu principal
        x= var.DIMENSION_PANTALLA[0] // 2,
        y= 550,
        text= 'VOLVER',
        screen= form.get('screen'),
        font_path= var.FONT_ALAGARD,
        font_size= 30,
        on_click= cambiar_pantalla , on_click_param= (form, 'form_menu') # <- tupla de parms con datos del form y nombre del formulario "MENU" = 'menu_form.py'
    )  

    form['data_loaded'] = False

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_volver')  
    ]
    var.dict_forms_status[form.get('name')] = form 
    return form 

def cambiar_pantalla(param_list : tuple):
    """ Vacìa los datos del formulario Ranking para su salida, para cuando se vuelva a ingresar
    pueda reiniciarse. Por ultimo, recibe el nombre de un formulario y lo ejecuta.
        1 - Muestra un mensaje de salida
        2 - Vacìa la lista de widgets
        3 - Establece en False la carga de datos
        4 - LLamado a funcion de cambio de pantalla
    :params: 
        form_ranking -> datos del formulario
        form_name -> nombre del formualrio """
    
    form_ranking, form_name = param_list # <- desempaqueto los datos

    print('Saliendo del formulario -> "RANKING" ...')
    form_ranking['lista_ranking_GUI'] = []
    form_ranking['lista_ranking_file'] = []
    form_ranking['data_loaded'] = False
    base_form.cambiar_pantalla(form_name)

def armar_encabezado_top_ranking():
    """ Arma e imprime por consola el encabezado de top ranking """
    print(' ________________________________________')
    print('|                                        |')
    print('|    RANKING  TOP 7 MEJORES PUNTAJES     |')
    print('|________________________________________|')
    print('|____  NOMBRE  ____|____  PUNTAJE  ______|')
    

def init_ranking_data(form_dict_data: dict):
    """
    Arma la siguiente pantalla con los datos obtenidos del archivo puntajes.csv
    POSICION        NOMBRE          PUNTAJE
    POSICION        NOMBRE          PUNTAJE
    POSICION        NOMBRE          PUNTAJE
    POSICION        NOMBRE          PUNTAJE
    POSICION        NOMBRE          PUNTAJE

    """
    form_dict_data['lista_ranking_GUI'] = []
    matriz = form_dict_data.get('lista_ranking_file')
    y_coord_inicial = 190 # establezco la posicion para el primer registro
    color_texto = (255,255,255) # blanco
    armar_encabezado_top_ranking()
    for indice_fila in range(len(matriz)):
        fila = matriz[indice_fila]
        nombre_jugador = fila[0]
        puntaje_jugador = fila[1]
        mensaje = f'       {nombre_jugador:15}    {puntaje_jugador}'
        
        print(mensaje)


        # me tengo que crear un label por cada dato
        posicion = Label(
            x= var.DIMENSION_PANTALLA[0] // 2 - 220,
            y= y_coord_inicial ,
            text= f'{indice_fila + 1}', # <- convierto a string : "1" ... "1" ... "1"
            screen= form_dict_data.get('screen'),
            font_size=40,
            font_path= var.FONT_ALAGARD, color=color_texto
        )
        nombre = Label(
            x= var.DIMENSION_PANTALLA[0] // 2 ,
            y= y_coord_inicial,
            text= nombre_jugador, # <- nombre del jugador
            screen= form_dict_data.get('screen'),
            font_size=40,
            font_path= var.FONT_ALAGARD, color=color_texto       
        )
        puntaje = Label(
            x= var.DIMENSION_PANTALLA[0] // 2 + 220,
            y= y_coord_inicial,
            text= f'{puntaje_jugador}', # <- puntaje del jugador
            screen= form_dict_data.get('screen'),
            font_size=40,
            font_path= var.FONT_ALAGARD, color=color_texto
        )

        y_coord_inicial += 50 # actualizo la posision para el siguiente registro

        form_dict_data['lista_ranking_GUI'].append(posicion)
        form_dict_data['lista_ranking_GUI'].append(nombre)
        form_dict_data['lista_ranking_GUI'].append(puntaje)

        if indice_fila == 0:
            color_texto = (255,0,0)


def inicializar_ranking_archivo(form_dict_data: dict):
    """ Carga la lista de ranking con toda su informacion 
        con los datos obtenidos desde el archivo de entrada puntajes.csv"""
    
    if not form_dict_data.get('data_loaded'):
        form_dict_data['lista_ranking_file'] = load_data.cargar_ranking(file_path= var.RANKING_CSV_FILE, top=7)
        init_ranking_data(form_dict_data) # llamado a funcion que agarra la matriz y se encarga de dibujar todo lo necesario en el form
        form_dict_data['data_loaded'] = True
    lista_ranking_file = form_dict_data['lista_ranking_file']

def draw(form_dict_data: dict):
    """ Dibuja la pantalla del formulario RANKING y sus widgets 
    :params: form_dict_data -> datos del formulario"""
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)
    
    # dibujo los widgets lbl del ranking
    for widget in form_dict_data.get('lista_ranking_GUI'):
        widget.draw()
    

def update(form_dict_data: dict):
    """ Carga los datos, los actualiza y los muestra en pantalla """

    if not form_dict_data.get('data_loaded'):
        inicializar_ranking_archivo(form_dict_data)
    base_form.update(form_dict_data)
