
def mapear_valores(matriz: list[list], columna_a_mapear: int, callback):

    for indice_fila in range(len(matriz)):
        valor  = matriz[indice_fila][columna_a_mapear] 
        matriz[indice_fila][columna_a_mapear] = callback(valor)

def parsear_valor(valor: str):
    """ Convierte un valor a entero o flotante segun sea el caso
    :params: valor -> dato sting """
    if valor.isdigit(): 
        int(valor)
    
    elif "." in valor: 
        float(valor)
    
    return valor


def cargar_ranking(top: int = 7) -> list:
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
    with open('','r', encoding='utf-8') as file:
        
        texto = file.read()

        for linea in texto.split('\n'):
            if linea: 
                lista_datos_linea = linea.split(';')
                ranking.append(lista_datos_linea)
    mapear_valores(ranking, columna_a_mapear= 1, callback= parsear_valor) # parseo de datos

    ranking.sort(key= lambda fila: fila[1], reverse=True) # ordena DES por puntaje numerico

    return ranking[:top] # Devuelve los primeros 7 valores 
     