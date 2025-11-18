import modules.variables as var
import json
import os

def mapear_valores(matriz: list[list], columna_a_mapear: int, callback):

    for indice_fila in range(len(matriz)):
        valor  = matriz[indice_fila][columna_a_mapear] 
        matriz[indice_fila][columna_a_mapear] = callback(valor)

def parsear_valor(valor: str):
    """ Convierte un valor a entero o flotante segun sea el caso
    :params: valor -> dato sting """
    if valor.isdigit(): 
        return int(valor)
    
    elif "." in valor: 
        return float(valor)
    
    return valor


def cargar_ranking(file_path: str, top: int = 7) -> list:
    """ Carga datos a una matriz desde una rchivo csv:
        1 - Apertura , lectura y cierra de archivo 
        2 - Adiciona linea por linea a la lista 
        3 - Convierte los valores numericos segun la columna indicada 
        4 - Ordena la lista DES segun el puntaje mas alto

    :params: 
        top -> numero que indica la cantidad de reg a devolver
    :returns:
         ranking[:top] -> lista de los 7 maximos valores
    """
    
    ranking = []
    with open(file_path,'r', encoding='utf-8') as file:
        
        texto = file.read()

        for linea in texto.split('\n'):
            if linea: 
                lista_datos_linea = linea.split(';')
                ranking.append(lista_datos_linea)

    mapear_valores(ranking, columna_a_mapear= 1, callback= parsear_valor) # parseo de datos

    ranking = ranking[1:] # ignora el encabezado y empieza desde las 2da linea
    ranking.sort(key=lambda fila: fila[1], reverse=True) # ordena DES por puntaje numerico

    return ranking[:top] # Devuelve los primeros 7 valores 

def cargar_configs(file_path: str) -> dict:
    """ Carga un dict de datos desde la lectura de un archivo configs.json
    :params:   
        file_path -> ruta del archivo
    :returns:
        data -> dict de datos
     """
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def cargar_configs_stage(stage_data: dict):
    """ Si la partida sigue en curso y los datos no estan cargados, los carga desde 
    la lectura de un archivo
    :params: 
        stage_data -> datos del stage
     """
    if not stage_data.get('juego_finalizado') and not stage_data.get('data_cargada'):

        configs_globales = cargar_configs(var.JSON_CONFIGS_FILE) 
        stage_data['configs'] = configs_globales.get('nivel_1')
        stage_data['ruta_mazo'] = stage_data.get('configs').get('ruta_mazo')
        

def leer_bd_cartas(path_mazo: str) -> dict:
    """ Realiza la carga de datos tecnicos de las cartas y arma un diccionario 
    :params:
        path_mazo -> ruta de carpeta de imagenes de las cartas con sus datos (nombre)
    :returns:
        cartas_dict -> dict de datos
        """
    cartas_dict = {
        "cartas": []
    }

    for root, dir, files in os.walk(path_mazo):
        reverse_path = ''
        deck_cards = []

        for carta in files:
            card_path = os.path.join(root, carta)
            
            if 'reverse' in card_path:
                reverse_path = card_path.replace('\\','/')
            else:
                card_path = card_path.replace('\\','/') 
                filename = carta

                filename = filename.replace('.png','')
                datos_crudo = filename.split('_')
            

                datos_card = { # '0.0.1 HP 9999 ATK 30000 DEF 9999 7 ', '1.0_HP_8000_ATK_20000_DEF_8000_7.png'
                    'id'  : datos_crudo[0],
                    'hp' : int(datos_crudo[2]),
                    'atk' : int(datos_crudo[4]),
                    'def' : int(datos_crudo[6]),
                    'ruta_frente' : card_path,
                    'ruta_reverso' : ''
                }
                deck_cards.append(datos_card)

        for index_carta in range(len(deck_cards)):
            deck_cards[index_carta]['ruta_reverso'] = reverse_path # cargo la ruta de la img reverso
        
        cartas_dict['cartas'] = deck_cards # cargo los datos de la carta en el dict
        return cartas_dict
            
def guardar_info_cartas(ruta_archivo: str, dict_cards: dict):
    """ Graba info tecnica de las cartas en un archivo json """
    with open(ruta_archivo, 'w', encoding='utf-8') as file:
        json.dump(dict_cards, file, indent=4)


def cargar_bd_data(stage_data: dict):
    """ Realiza la carga de los datos de las cartas cuando la partida està en curso
    :params:
        stage_data -> datos del stage
    """
    if not stage_data.get('juego_finalizado'):

        if os.path.exists(var.JSON_INFO_CARDS_FILE) and os.path.isfile(var.JSON_INFO_CARDS_FILE): 
            print(' >>>>>>>>>>>>>>>>>>>  CARGANDO BD CARTAS DESDE FILE  <<<<<<<<<<<<<<<<<<<<')
            stage_data['cartas_mazo_inicial'] = cargar_configs(var.JSON_INFO_CARDS_FILE)
        else:
            print(' >>>>>>>>>>>>>>>>>>>  CARGANDO BD CARTAS DESDE DIR   <<<<<<<<<<<<<<<<<<<<')
            stage_data['cartas_mazo_inicial'] = leer_bd_cartas(stage_data.get('ruta_mazo'))

def reducir(callback, iterable: list):
    suma = 0
    for elemento in iterable:
        suma += callback(elemento)
    return suma

if __name__ == '__main__':
    #print(cargar_ranking('C:/Repositorio UTN/2025/PROG I/TPFinal_Div317_Heck_Nicole/puntajes.csv', top=7))
    cartas = leer_bd_cartas("modules/assets/decks/platinum_deck_expansion_1")

    #for clave, valor in cartas.items():
    #    print(f'{clave} : {valor}')
    #    print()
    
    guardar_info_cartas('./info_cartas.json', cartas)
    print(cartas.get('cartas')[:2])
    