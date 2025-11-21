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
    """ Devuelve el contenido de la clave 'visible' """
    return dict_card.get('visible')

def cambiar_visibilidad(dict_card: dict):
    """ Niega el contenido de la clave 'visible' """
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
    """ Dibuja la superficie de la carta, si està visible dibuja la portada,
    caso contrario dibuja el reverso de la misma"""
    
    if dict_card.get('visible'):
        dict_card['imagen'] = redimensionar_imagen(dict_card.get('ruta_frente'), 40)
    else:
        dict_card['imagen'] = redimensionar_imagen(dict_card.get('ruta_reverso'), 40)

    dict_card['rect'] = dict_card.get('imagen').get_rect()
    dict_card['rect'].topleft = dict_card.get('coordenadas')

    screen.blit(dict_card.get('imagen'), dict_card.get('rect'))


