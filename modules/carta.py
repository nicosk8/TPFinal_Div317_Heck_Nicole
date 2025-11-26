import pygame as pg
import modules.load_data as load_data

def inicializar_carta(dict_card: dict, coords: list) -> dict:
    """ 
        'id'  : datos_crudo[0],
        'hp' : int(datos_crudo[2]),
        'atk' : int(datos_crudo[4]),
        'def' : int(datos_crudo[6]),
        'ruta_frente' : card_path,
        'ruta_reverso' : ''    
        
    """
    card = dict_card
    card['visible'] = False
    card['coordenadas'] = coords

    card['imagen'] = None
    card['rect'] = None

    return card

def esta_visible(dict_card: dict) -> bool:
    """ Devuelve True si esta visible, False si no esta visible """
    return dict_card.get('visible')

def cambiar_visibilidad(dict_card: dict):
    """ Cambia la visibilidad de la carta actual.
        Valor True -> para dibujar superficie frente
        Valor False -> para dibujar superficie reverso  """
    dict_card['visible'] = not dict_card.get('visible')

def get_hp_carta(dict_card: dict) -> int:
    """ Devuelve el contenido de la clave "hp" """
    return dict_card.get('hp')

def get_atk_carta(dict_card: dict) -> int:
    """ Devuelve el contenido de la clave "atk" """
    return dict_card.get('atk')

def get_def_carta(dict_card: dict) -> int:
    """ Devuelve el contenido de la clave "def" """
    return dict_card.get('def')

def asignar_coordenadas_carta(dict_card: dict, coordenadas: list[int]):
    """ Asigna coordenadas a la clave 'coordenadas' """
    dict_card['coordenadas'] = coordenadas

def redimensionar_imagen(ruta_img: str, porcentaje_a_ajustar: int):
    """ Redimensiona una imagen 
    :params:
        ruta_img -> ruta de la img
        porcentaje_a_ajustar -> porcentaje a ajustar 
    :returns:
        imagen_final -> imagen redimensionada """
    imagen_raw = pg.image.load(ruta_img)
    ancho, alto = imagen_raw.get_size() # devuelve (w,h)

    nuevo_alto = int(alto * float(f'0.{porcentaje_a_ajustar}'))
    nuevo_ancho = int(ancho * float(f'0.{porcentaje_a_ajustar}'))

    imagen_final = pg.transform.scale(imagen_raw, (nuevo_ancho, nuevo_alto))
    return imagen_final

def draw_carta(dict_card: dict, screen: pg.Surface):
    """ Dibuja la superficie de la carta, si 'visible' = True, dibuja la portada,
    caso contrario, si 'visible' = False dibuja la img del reverso """
    
    visible_resultado = dict_card.get('visible')
    img_frente = dict_card.get('ruta_frente')
    img_reverso = dict_card.get('ruta_reverso')
    
#    if dict_card.get('visible'):
    if visible_resultado:

        dict_card['imagen'] = redimensionar_imagen(img_frente, 35)
#        print(f'CARTA.PY -> DRAW_CARTA() -> VISIBILIDAD: {dict_card.get('visible')}')
#        print(f'CARTA.PY -> DRAW_CARTA() -> IMAGEN A DIBUJAR: {img_frente}')
#        print(f'CARTA.PY -> DRAW_CARTA() -> COORDENADAS DEL RECT A DIBUJAR: {dict_card.get('coordenadas')}\n')
    else:
        dict_card['imagen'] = redimensionar_imagen(img_reverso, 35)
#        print(f'CARTA.PY -> DRAW_CARTA() -> VISIBILIDAD: {dict_card.get('visible')}')
#        print(f'CARTA.PY -> DRAW_CARTA() -> IMAGEN A DIBUJAR: {img_reverso}')
#        print(f'CARTA.PY -> DRAW_CARTA() -> COORDENADAS DEL RECT A DIBUJAR: {dict_card.get('coordenadas')}\n')

    dict_card['rect'] = dict_card.get('imagen').get_rect()
    dict_card['rect'].topleft = dict_card.get('coordenadas')
    superficie_dibujada = screen.blit(dict_card.get('imagen'), dict_card.get('rect'))
#    print(f'CARTA.PY -> DRAW_CARTA() -> SUPERFICIE DIBUJADA: {superficie_dibujada}')


