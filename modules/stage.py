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

    stage_data['cartas_mazo_inicial_e'] = []    
    stage_data['cartas_mazo_inicial_p'] = []  

    stage_data['cartas_mazo_preparadas_e'] = []       
    stage_data['cartas_mazo_preparadas_p'] = []

    stage_data['cantidad_cartas_jugadores'] = 10

    stage_data['ruta_mazo'] = ''
    stage_data['screen'] = pantalla

    stage_data['jugador'] = jugador
    stage_data['coordenada_inicial_mazo_jugador'] = (20,360)
    stage_data['coordenada_final_mazo_jugador'] = (390,360)

    stage_data['coordenada_inicial_mazo_enemigo'] = (20,70)
    stage_data['coordenada_final_mazo_enemigo'] = (390,70)

    
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

def asignar_cartas_stage(stage_data: dict, player: dict):
    """ Asigan las cartas a los participantes"""
   
    # mezclo las cartas y las asigno
    rd.shuffle(stage_data.get('cartas_mazo_preparadas'))
    cantidad_cartas = stage_data.get('cantidad_cartas_jugadores')
    cartas_participante = rd.sample(stage_data.get('cartas_mazo_preparadas'), cantidad_cartas)
   
    #participante['cartas_iniciales'] = cartas_participante
    #participante['cartas_mazo_preparadas'] = cartas_participante
    participante.set_cartas_participante(player, cartas_participante)

def generar_mazo(stage_data: dict):
    """ Genera el mazo de cartas de los participantes.
    :params:
        stage_data -> datos del juego 
        participante -> datos del participante 
    """  
    
    print('stage.py -> generar_mazo()')

    for carta_inicial in stage_data.get('cartas_mazo_inicial'):
        carta_power = carta.inicializar_carta(carta_inicial, (0,0) ) 
        stage_data.get('cartas_mazo_preparadas').append(carta_power)
    print(f'         cartas_mazo_preparadas -> {stage_data.get('cartas_mazo_preparadas')} ')
       
def barajar_mazos_stage(stage_data: dict): 
    """ Si la partida esta en curso, asigna cartas a los participantes y
    establece los stats iniciales (hp,atk y def).
    :params:
        stage_data -> datos del juego  
    """  
    print('stage.py -> barajar_mazos_stage()')

    if not stage_data.get('stage_finalizado'):
        asignar_cartas_stage(stage_data, stage_data.get('jugador'))
        asignar_cartas_stage(stage_data, stage_data.get('enemigo'))
        participante.asignar_stats_iniciales_participante(stage_data.get('jugador'))
        participante.asignar_stats_iniciales_participante(stage_data.get('enemigo'))
        stage_data['data_cargada'] = True
        print(f' *** data cargada : {stage_data.get('data_cargada')}')

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
    print('\nstage.py -> inicializar_data_stage() -> INICIALIZACION FINALIZADA ')

def restart_stage(stage_data: dict, jugador: dict, pantalla: pg.Surface, nro_stage: int):
    """ Restablece el nivel. Devuelve el seteo de las configuraciones a como estaban al inicio 
    :params:  """
    stage_data = inicializar_stage(jugador, pantalla, nro_stage)
    participante.reiniciar_datos_participante(jugador)
    inicializar_data_stage(stage_data)
    return stage_data

def jugar_mano_stage(stage_data: dict):
    """ Juega la carta actual de los participantes """
    participante.jugar_carta(stage_data.get('jugador'))
    participante.jugar_carta(stage_data.get('enemigo'))

def es_golpe_critico() -> bool:
    """ Bandera de golpe critico : Setea una funcion para asignar True o False 
        y retorna ese resultado """
    critical = rd.choice([False, False, False, True]) # 25% de probabilidad de golpe critico
    return critical

def comparar_damage(stage_data: dict) -> str:
    """ 1 - Verifica cual fue la ultima carta jugada por los participantes.
        2 - Compara los ataques de estas cartas. Si ataque enemigo mayor al jugador,
            establece al enemigo como ganador de la partida y resta stats al jugador. 
            Caso contrario, misma logica a la inversa.
        :returns: 
            ganador_mano -> nombre del ganador """
    ganador_mano = None
    jugador = stage_data.get('jugador')
    enemigo = stage_data.get('enemigo')
    critical = False
    carta_jugador = participante.get_carta_actual_participante(jugador)
    carta_enemigo = participante.get_carta_actual_participante(enemigo)

    if carta_enemigo and carta_jugador:
        critical = es_golpe_critico()
        atk_jugador = carta.get_atk_carta(carta_jugador)
        atk_enemigo = carta.get_atk_carta(carta_enemigo)
        
        if atk_enemigo > atk_jugador:
            ganador_mano = 'PC'
            participante.restar_stats_participante(jugador, carta_enemigo, critical)
        else:
            score = atk_jugador - carta.get_def_carta(carta_enemigo)
            ganador_mano = 'PLAYER'
            participante.restar_stats_participante(enemigo, carta_jugador, critical)
            participante.add_score_participante(jugador, )
    return critical, ganador_mano

def chequear_ganador(stage_data: dict):
    """ Si el jugador llegò a 0 de vida o la vida del jugador es menor que la del enemigo,
     y ,ademàs, el enemigo ya no tiene cartas para jugar, establece como ganador al enemigo. 
    Caso contrario, misma logica a la inversa.  """
    jugador = stage_data.get('jugador')
    enemigo = stage_data.get('enemigo')

    if (participante.get_hp_participante(jugador) <= 0 or\
        participante.get_hp_participante(jugador) < participante.get_hp_participante(enemigo)) and\
        (len(participante.get_cartas_restantes_participante(enemigo)) == 0):
            stage_data['ganador'] = enemigo
            stage_data['juego_finalizado'] = True

    elif (participante.get_hp_participante(enemigo) <= 0 or\
          participante.get_hp_participante(enemigo) < participante.get_hp_participante(jugador)) and\
         (len(participante.get_cartas_restantes_participante(jugador)) == 0):
            stage_data['ganador'] = jugador
            stage_data['juego_finalizado'] = True

def jugar_mano(stage_data: dict) -> str:
    """ Ejecuta la jugada de cartas, compara daños, resta stats a los participantes, verifica el ganador de la ronda y lo retorna """
    if not stage_data.get('juego_finalizado'):
        jugar_mano_stage(stage_data)
        critical, ganador_mano = comparar_damage(stage_data)
        chequear_ganador(stage_data)
        return critical, ganador_mano
    
    return None

def draw_jugadores(stage_data: dict):
    """ Dibuja en pantalla las cartas del jugador y oponente """

    participante.draw_participante(stage_data.get('jugador'), stage_data.get('screen'))
    participante.draw_participante(stage_data.get('enemigo'), stage_data.get('screen'))