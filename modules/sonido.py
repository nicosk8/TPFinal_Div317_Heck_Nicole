import pygame.mixer as mixer

music_configs = {
    "actual_music_path" : ''
}

def set_music_path(music_path: str):
    """ Funcion encargada de establecer la ruta de la cancion a la que se le da play
    :params: 
        music_path -> ruta de la musica """
    music_configs['actual_music_path'] = music_path

def play_music():
    """ Funcion que se encarga de activar configurar la musica y activarla.
     Contempla si ya habìa una musica anterior sonando, por lo tanto la cambia a la musica que le corresponde al formulario """
    if music_configs.get('actual_music_path'):
        mixer.music.load(music_configs.get('actual_music_path'))
        mixer.music.set_volume(0.3) # 30%
        mixer.music.play(-1,0,2500) # (reproduccion en loop, inicio en el seg. 0 de la cancion, volumen inicial hasta un vol. alto [fade in])


def get_actual_volume() -> int:
    """ devuelve el volumen actual de la musica """
    actual_vol = mixer.music.get_volume() * 100 
    return actual_vol

def set_volume(volume: int):
    " Setea el valor actual del volumen  de la musica "
    actual_vol = volume / 100
    mixer.music.set_volume(actual_vol)
    print(f'Musica volumen actual -> {actual_vol}')
 

def stop_music():
    """ Si hay musica activada sonando y ,ademas, esta siendo reproducida, la desactiva """
    if music_configs.get('actual_music_path') and mixer.music.get_busy():
        mixer.music.fadeout(500) # fade out progresivo en 500 miliseg
