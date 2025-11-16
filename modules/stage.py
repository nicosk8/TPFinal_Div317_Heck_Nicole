import pygame as pg
import modules.variables as var
import modules.load_data as load_data

def inicializar_stage(jugador: dict, pantalla: pg.Surface, nro_stage: int):
    """ Inicializa el nivel/stage.
    :params: 
        jugador -> datos del jugador 
        nro_stage -> numero del nivel actual     
    """
    stage_data = {}
    stage_data['nro_stage'] = nro_stage
    stage_data['configs'] = {}               # configuaracion general del juego
    stage_data['cartas_mazo_inicial'] = []
    stage_data['cartas_mazo_preparadas'] = [] # cartas listas que utiliza el proceso del juego
 
    stage_data['ruta_mazo'] = ''
    stage_data['screen'] = pantalla
    stage_data['jugador'] = jugador

    stage_data['juego_finalizado'] = False
    stage_data['puntaje_guardado'] = False
    stage_data['stage_timer'] = var.STAGE_TIMER
    stage_data['ganador'] = None                    # info del ganador final

    stage_data['puntaje_stage'] = 0
    stage_data['data_cargada'] = False

    return stage_data

def generar_mazo(stage_data: dict):
    cantidad_cartas = stage_data.get('cantidad_cartas_jugadores')

def inicializar_data_stage(stage_data: dict):
    print('Cargando los datos del stage...')
    load_data.cargar_configs_stage(stage_data) # lee la config del juego desde un archivo 
    load_data.cargar_bd_data(stage_data) # lee un directorio especifico y empieza  a cargar una lista de dict con los datos de las cartas
    generar_mazo(stage_data)

