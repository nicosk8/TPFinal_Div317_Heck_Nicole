import pygame as pg
import modules.variables as var
import modules.load_data as load_data
import random as rd
import modules.carta as carta
import modules.participante as participante

def inicializar_stage(jugador: dict, pantalla: pg.Surface, nro_stage: int):
    """ Inicializa el nivel/stage.
    :params: 
        jugador -> datos del jugador 
        nro_stage -> numero del nivel actual     
    """
    stage_data = {}
    stage_data['nro_stage'] = nro_stage
    stage_data['configs'] = {}                      # configuaracion general del juego
    stage_data['cartas_mazo_inicial'] = []
    stage_data['cartas_mazo_preparadas'] = []       # cartas listas que utiliza el proceso del juego
 
    stage_data['ruta_mazo'] = ''
    stage_data['screen'] = pantalla

    stage_data['jugador'] = jugador
    stage_data['coordenada_inicial_mazo_jugador'] = (0,0)
    stage_data['coordenada_final_mazo_jugador'] = (0,0)

    stage_data['coordenada_inicial_mazo_enemigo'] = (0,0)
    stage_data['coordenada_final_mazo_enemigo'] = (0,0)

    stage_data['cantidad_cartas_jugadores'] = 0

    stage_data['enemigo'] = participante.inicializar_participante(stage_data.get('screen'), nombre='Enemigo')
    participante.setear_stat_participante(stage_data.get('enemigo'), stat='pos_deck_inicial', valor=stage_data.get('coordenada_inicial_mazo_enemigo'))
    participante.setear_stat_participante(stage_data.get('enemigo'), stat='pos_deck_jugado', valor=stage_data.get('coordenada_final_mazo_enemigo'))

    participante.setear_stat_participante(stage_data.get('jugador'), stat='pos_deck_inicial', valor=stage_data.get('coordenada_inicial_mazo_jugador'))
    participante.setear_stat_participante(stage_data.get('jugador'), stat='pos_deck_jugado', valor=stage_data.get('coordenada_final_mazo_jugador'))

    stage_data['juego_finalizado'] = False
    stage_data['puntaje_guardado'] = False
    stage_data['stage_timer'] = var.STAGE_TIMER     # indicador de tiempo restante de partida
    stage_data['ganador'] = None                    # info del ganador final

    stage_data['puntaje_stage'] = 0
    stage_data['data_cargada'] = False              # indicador de datos cargados

    return stage_data

def asignar_cartas_stage(stage_data: dict, participante: dict):
    """ Asigan las cartas a los participantes"""
    # mezclo las cartas y las asigno
    rd.shuffle(stage_data.get('cartas_mazo_preparadas'))
    cantidad_cartas = stage_data.get('cantidad_cartas_jugadores')
    cartas_participante = rd.sample(stage_data.get('cartas_mazo_preparadas'), cantidad_cartas)
    participante['cartas_iniciales'] = cartas_participante

def generar_mazo(stage_data: dict):
    """ Genera el mazo de cartas de los participantes.
    :params:
        stage_data -> datos del juego 
        participante -> datos del participante 
    """  
    for card in stage_data.get('cartas_mazo_inicial'):
        carta_power = carta.inicializar_carta(card, (0,0) ) 
        stage_data.get('cartas_mazo_preparadas').append(carta_power)

        
def barajar_mazos_stage(stage_data: dict): 
    """ Si la partida esta en curso, asigna cartas a los participantes y
    establece los stats iniciales (hp,atk y def).
    :params:
        stage_data -> datos del juego  
    """  
    if not stage_data.get('stage_finalizado'):
        asignar_cartas_stage(stage_data, stage_data.get('jugador'))
        asignar_cartas_stage(stage_data, stage_data.get('enemigo'))
        participante.asignar_stats_iniciales_participante(stage_data.get('jugador'))
        participante.asignar_stats_iniciales_participante(stage_data.get('enemigo'))
        stage_data['data_cargada'] = True


def restart_stage(stage_data: dict, jugador: dict, pantalla: pg.Surface, nro_stage: int):
    """ Restablece el nivel. Devuelve el seteo de las configuraciones a como estaban al inicio 
    :params:  """
    stage_data = inicializar_stage(jugador, pantalla, nro_stage)
    participante.set_score_participante(jugador, 0)
    participante.reiniciar_datos_participante(jugador)
    inicializar_data_stage(stage_data)

def draw_jugadores(stage_data: dict):
    """ Dibuja en pantalla las cartas del jugador y oponente """
    participante.draw_participante(stage_data.get('jugador'))
    participante.draw_participante(stage_data.get('enemigo'))

def inicializar_data_stage(stage_data: dict):
    """ Proceso prncipal del modulo stage: 
        1 - lee la config del juego desde un archivo 
        2 - lee un directorio especifico y empieza  a cargar una lista de dict con los datos de las cartas 
        3 - Genera los mazos de cartas 
        4 - Mezcla las cartas y las asigna a los participantes
    :params:
        stage_data -> datos del juego 
    """
    print('Cargando los datos del stage...')
    load_data.cargar_configs_stage(stage_data) # lee la config del juego desde un archivo 
    load_data.cargar_bd_data(stage_data) # lee un directorio especifico y empieza  a cargar una lista de dict con los datos de las cartas
    generar_mazo(stage_data)
    barajar_mazos_stage(stage_data)