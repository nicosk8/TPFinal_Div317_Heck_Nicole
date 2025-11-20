import pygame as pg
import modules.carta as carta
import modules.variables as var
import modules.load_data as load_data
from functools import reduce

def inicializar_participante(pantalla: pg.Surface, nombre: str = 'PC'):
    participante = {}
    participante['nombre'] = nombre
    participante['hp_actual'] = 1
    participante['hp_inicial'] = 1
    participante['atk'] = 1
    participante['def'] = 1
    participante['score'] = 0

    participante['mazo_asignado'] = []  # cartas iniciales
    participante['cartas_mazo'] = []    # cartas restantes
    participante['cartas_usadas'] = []  # cartas que ya fueron jugadas

    participante['screen'] = pantalla
    participante['pos_deck_inicial'] = (0,0)
    participante['pos_deck_jugado'] = (0,0)

    return participante

def get_hp_participante(participante: dict) -> int:
    """ Devuelve el contenido de la clave 'hp' """
    return participante.get('hp_actual')

def get_hp_inicial_participante(participante: dict) -> int:
    """ Devuelve el contenido de la clave 'hp_inicial' """
    return participante.get('hp_inicial')

def get_atk_participante(participante: dict) -> int:
    """ Devuelve el contenido de la clave 'atk' """
    return participante.get('atk')

def get_def_participante(participante: dict) -> int:
    """ Devuelve el contenido de la clave 'def' """
    return participante.get('def')

def get_nombre_participante(participante: dict) -> str:
    """ Devuelve el contenido de la clave 'nombre' """
    return participante.get('nombre')

def set_nombre_participante(participante: dict, nuevo_nombre: str):
    """ Asigna nuevo nombre en la clave 'nombre' """
    participante['nombre'] = nuevo_nombre

def get_cartas_iniciales_participante(participante: dict) -> list[dict]:
    """ Devuelve las cartas iniciales que tiene asignadas el participante """
    return participante.get('mazo_asignado')

def get_cartas_restantes_participante(participante: dict) -> list[dict]:
    """ Devuelve las cartas restantes del participante que estan en juego """
    return participante.get('cartas_mazo')

def get_cartas_jugadas_participante(participante: dict) -> list[dict]:
    """ Devuelve las cartas que ya fueron jugadas """
    return participante.get('cartas_usadas')

def get_coordenadas_mazo_inicial(participante: dict):
    """ Devuelve la posicion en pantalla inicial del mazo de cartas """
    return participante.get('pos_deck_inicial')

def get_coordenadas_mazo_jugado(participante: dict):
    """ Devuelve la posicion en pantalla del mazo de cartas que fue jugado """
    return participante.get('pos_deck_jugado')

def get_carta_actual_participante(participante: dict):
    """ Devuelve la ultima carta del mazo de cartas usadas/jugadas (dadas vuelta) """
    return participante.get('cartas_usadas')[-1]

def setear_stat_participante(participante: dict, stat: str, valor: int):
    """ """
    participante['stat'] = valor    

def set_cartas_participante(participante: dict, lista_cartas: list[dict]):
    """ Setea las cartas del participante:
            1 - Asigna las coordenadas - obtenidas por medio de una funcion - a todas las cartas del mazo 
            2 - Carga la lista de cartas en la clave 'mazo_asignado' donde las aloja inicialmente  
            3 - Genera una copia superficial del mazo de cartas y la guarda en la clave 'cartas_mazo' """
    for carta_base in lista_cartas:
        carta_base['coordenadas'] = get_coordenadas_mazo_inicial(participante)
    
    participante['mazo_asignado'] = lista_cartas      # cartas boca arriba
    participante['cartas_mazo'] = lista_cartas.copy() # cartas boca abajo

def set_score_participante(participante: dict, score: int):
    """ Guarda puntaje del participante en su clave """
    participante['score'] = score
 
def add_score_participante(participante: dict, score: int):
    """ Acumula el puntaje del participante a medida que incrementa los puntos durante la partida """
    participante['score'] += score
 
def get_score_participante(participante: dict) -> int: 
    return participante.get('score')

def asignar_stats_iniciales_participante(participante: dict):
    """ Calcula el total de hp, atk y defensa de todas las cartas del mazo y guarda los totales 
    en la estructura de claves del participante  """

    participante['hp_inicial'] = load_data.reducir(
        carta.get_hp_carta,
        participante.get('mazo_asignado') # iterable
    )

    participante['hp_actual'] = participante['hp_inicial']

    participante['atk'] = load_data.reducir(
        carta.get_atk_carta,
        participante.get('mazo_asignado') 
    )

    participante['def'] = load_data.reducir(
        carta.get_def_carta,
        participante.get('mazo_asignado') 
    )

def verficar_estado_negativo(stat: int):
    """ Valida stat de poder menor o superior a 0"""
    if stat < 0:
        return 0
    return stat

def restar_stats_participante(participante: dict, carta_g: dict, is_critic : bool):
    """ Calcula el daño generado por la carta del participante y lo resta a
    la vida, ataque y defensa actuales.
    :params:
        participante -> participante
        carta_g: dict -> carta del oponente
        is_critic -> indicador de golpe critico
    """
    daño_multiplicado = 1
    if is_critic:
        daño_multiplicado = 3
    
    carta_jugador = participante.get('cartas_usadas')[-1]
    damage = carta.get_atk_carta(carta_g) - carta.get_def_carta(carta_jugador)
    damage *= daño_multiplicado

    # si el daño a restar deja al oponente en puntos de vida en negativo, seteo la vida en 0
    participante['hp_actual'] = verficar_estado_negativo(participante.get('hp_actual') - damage) 
    
    participante['atk'] -= carta.get_atk_carta(carta_jugador)
    participante['def'] -= carta.get_def_carta(carta_jugador) 

def info_to_csv(participante: dict):
    return f'{get_nombre_participante(participante)},{participante.get('score')}\n'

def reiniciar_datos_participante(participante: dict):
    """ Restablece el puntaje en 0 y vacìa la lista mazo de cartas """
    set_score_participante(participante,0)
    set_cartas_participante(participante, list())
    participante['cartas_usadas'].clear()
    setear_stat_participante(participante, stat='hp_inicial', valor=0)
    setear_stat_participante(participante, stat='hp_actual', valor=0)
    setear_stat_participante(participante, stat='atk', valor=0)
    setear_stat_participante(participante, stat='def', valor=0)
    
def jugar_carta(participante: dict):
    """ Logica de jugado de una carta:
    Si hay cartas disponibles en el mazo:
        1 - Obtiene la ultima carta de la lista del mazo actual
        2 - Anexa esa ultima carta a la lista del mazo de cartas usadas """
        
    if participante.get('cartas_mazo'):
        print(f'El jugador {participante.get('nombre')} tiene {len(participante.get('cartas_mazo'))} cartas')
        carta_actual = participante.get('cartas_mazo').pop()
        carta.cambiar_visibilidad(carta_actual)
        carta.asignar_coordenadas_carta(carta_actual,  get_coordenadas_mazo_jugado(participante))
        participante.get('cartas_usadas').append(carta_actual)

    else:
        print(f'El jugador {participante.get('nombre')} no tiene cartas')

def draw_participante(participante: dict, screen: pg.Surface):
    """ Dibuja las cartas en pantalla del participante """
   
    if participante.get('cartas_mazo'):
        carta.draw_carta(participante.get('cartas_mazo')[-1], screen)
    
    if participante.get('cartas_usadas'):
        carta.draw_carta(participante.get('cartas_usadas')[-1], screen) 