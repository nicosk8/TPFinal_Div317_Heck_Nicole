import pygame as pg
import modules.variables as var
import modules.load_data as load_data
import random as rd
import modules.carta as carta
import modules.participante as participante_juego

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

    stage_data['heal_available'] = True
    stage_data['jackpot_available'] = True
    
    stage_data['enemigo'] = participante_juego.inicializar_participante(stage_data.get('screen'), nombre='Enemigo')

    participante_juego.setear_stat_participante(stage_data.get('enemigo'), stat='pos_deck_inicial', valor=stage_data.get('coordenada_inicial_mazo_enemigo'))
    participante_juego.setear_stat_participante(stage_data.get('enemigo'), stat='pos_deck_jugado', valor=stage_data.get('coordenada_final_mazo_enemigo'))

    participante_juego.setear_stat_participante(stage_data.get('jugador'), stat='pos_deck_inicial', valor=stage_data.get('coordenada_inicial_mazo_jugador'))
    participante_juego.setear_stat_participante(stage_data.get('jugador'), stat='pos_deck_jugado', valor=stage_data.get('coordenada_final_mazo_jugador'))

    stage_data['juego_finalizado'] = False
    stage_data['puntaje_guardado'] = False
    stage_data['stage_timer'] = var.STAGE_TIMER     # indicador de tiempo restante de partida
    stage_data['last_timer'] = pg.time.get_ticks()
    stage_data['ganador'] = None                    # info del ganador final
    stage_data['data_cargada'] = False              # indicador de datos cargados

    return stage_data

def modificar_estado_bonus(stage_data: dict, bonus: str):
    stage_data[f'{bonus}_available'] = False

def timer_update(stage_data: dict):
    """ Actualiza el tiempo restante de partida """

    if stage_data.get('stage_timer') > 0:

        tiempo_actual = pg.time.get_ticks() # capturo el tiempo actual en milisegs
        

        if (tiempo_actual - stage_data.get('last_timer')) > 1000:
            stage_data['stage_timer'] -= 1
            stage_data['last_timer'] = tiempo_actual

def obtener_tiempo(stage_data: dict):
    return stage_data.get('stage_timer')

def asignar_cartas_stage(stage_data: dict, participante: dict):
    """ Mezcla las cartas y las asigna a los participantes"""

    cantidad_cartas = stage_data.get('cantidad_cartas_jugadores')
    if participante_juego.get_nombre_participante(participante) != 'Enemigo':
        rd.shuffle(stage_data.get('cartas_mazo_preparadas_p'))
        cartas_participante = stage_data.get('cartas_mazo_preparadas_p')[:cantidad_cartas]
    else: 
        rd.shuffle(stage_data.get('cartas_mazo_preparadas_e'))
        cartas_participante = stage_data.get('cartas_mazo_preparadas_e')[:cantidad_cartas]

    participante_juego.set_cartas_participante(participante, cartas_participante)

def generar_mazo(stage_data: dict):
    """ Genera el mazo de cartas de los participantes.
    :params:
        stage_data -> datos del juego 
        participante -> datos del participante 
    """  
    for carta_inicial_e, carta_inicial_p in zip(
        stage_data.get('cartas_mazo_inicial_e'),
        stage_data.get('cartas_mazo_inicial_p')
    ):
        carta_power_e = carta.inicializar_carta(carta_inicial_e, (0,0))
        carta_power_p = carta.inicializar_carta(carta_inicial_p, (0,0))
        stage_data.get('cartas_mazo_preparadas_e').append(carta_power_e)
        stage_data.get('cartas_mazo_preparadas_p').append(carta_power_p)
         
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
        participante_juego.asignar_stats_iniciales_participante(stage_data.get('jugador'))
        participante_juego.asignar_stats_iniciales_participante(stage_data.get('enemigo'))
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

def hay_jugadores_con_cartas(stage_data: dict) -> bool:

    jugador_con_cartas = participante_juego.get_cartas_restantes_participante(stage_data.get('jugador'))
    enemigo_con_cartas = participante_juego.get_cartas_restantes_participante(stage_data.get('enemigo'))
    return jugador_con_cartas or enemigo_con_cartas

def restart_stage(stage_data: dict, jugador: dict, pantalla: pg.Surface, nro_stage: int):
    """ Restablece el nivel. Devuelve el seteo de las configuraciones a como estaban al inicio 
    :params:  """
    stage_data = inicializar_stage(jugador, pantalla, nro_stage)
    participante_juego.reiniciar_datos_participante(jugador)
    inicializar_data_stage(stage_data)
    return stage_data

def jugar_mano_stage(stage_data: dict):
    """ Juega la carta actual de los participantes """
    participante_juego.jugar_carta(stage_data.get('jugador'))
    participante_juego.jugar_carta(stage_data.get('enemigo'))

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
    carta_jugador = participante_juego.get_carta_actual_participante(jugador)
    carta_enemigo = participante_juego.get_carta_actual_participante(enemigo)

    if carta_enemigo and carta_jugador:
        critical = es_golpe_critico()
        atk_jugador = carta.get_atk_carta(carta_jugador)
        atk_enemigo = carta.get_atk_carta(carta_enemigo)
        
        if atk_enemigo > atk_jugador:
            ganador_mano = 'PC'
            participante_juego.restar_stats_participante(jugador, carta_enemigo, critical)
        else:
            score = atk_jugador - carta.get_def_carta(carta_enemigo)
            ganador_mano = 'PLAYER'
            participante_juego.restar_stats_participante(enemigo, carta_jugador, critical)
            participante_juego.add_score_participante(jugador, score)
    return ganador_mano

def setear_ganador(stage_data: dict, participante: dict):
    """ Setea al ganador de la ronda """
    stage_data['ganador'] = participante
    stage_data['juego_finalizado'] = True

def chequear_ganador(stage_data: dict):
    """ Si el jugador llegò a 0 de vida o la vida del jugador es menor que la del enemigo,
     y ,ademàs, el enemigo ya no tiene cartas para jugar, establece como ganador al enemigo. 
    Caso contrario, misma logica a la inversa. Ademas, si el jugador pierde la mano, 
    el jugador pierde la mitad de su puntaje actual """
    jugador = stage_data.get('jugador')
    enemigo = stage_data.get('enemigo')

    if (participante_juego.get_hp_participante(jugador) <= 0 or\
        (participante_juego.get_hp_participante(jugador) < participante_juego.get_hp_participante(enemigo)) and\
        (len(participante_juego.get_cartas_restantes_participante(enemigo)) == 0)):
            
            setear_ganador(stage_data, enemigo)            
            puntaje_jugador_actual = participante_juego.get_score_participante(jugador) // 2
            participante_juego.set_score_participante(jugador, puntaje_jugador_actual)

    elif (participante_juego.get_hp_participante(enemigo) <= 0 or\
          (participante_juego.get_hp_participante(enemigo) < participante_juego.get_hp_participante(jugador)) and\
         (len(participante_juego.get_cartas_restantes_participante(jugador)) == 0)):
            
            setear_ganador(stage_data, jugador)

def esta_finalizado(stage_data: dict) -> bool:
    return stage_data.get('juego_finalizado')

def obtener_ganador(stage_data: dict):
    return stage_data.get('ganador')

def jugar_mano(stage_data: dict) -> str:
    """ Ejecuta la jugada de cartas, compara daños, resta stats a los participantes, verifica el ganador de la ronda y lo retorna """
    if not stage_data.get('juego_finalizado'):
        jugar_mano_stage(stage_data)
        ganador_mano = comparar_damage(stage_data)
        chequear_ganador(stage_data)
        return ganador_mano
    else:
        print(' ¡ JUEGO FINALIZADO !')    
        return None

def draw_jugadores(stage_data: dict):
    """ Dibuja en pantalla las cartas del jugador y oponente """

    participante_juego.draw_participante(stage_data.get('jugador'), stage_data.get('screen'))
    participante_juego.draw_participante(stage_data.get('enemigo'), stage_data.get('screen'))

def update(stage_data: dict):
    """ Actualiza el stage """
    timer_update(stage_data)
    chequear_ganador(stage_data)