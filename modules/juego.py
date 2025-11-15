import pygame as pg
import modules.variables as var
import modules.forms.form_controller as form_controller
import sys

def dbz_playing_cards():
    """ Puerta de entrada al juego DBZ Playing Cards"""
    
    pg.init()

    pg.display.set_caption(var.TITULO_JUEGO)
    pantalla_juego = pg.display.set_mode(var.DIMENSION_PANTALLA)
    pg.image.load(var.ICON_IMG) # cargo el icono del juego

    corriendo = True
    reloj = pg.time.Clock() # seteo de FPS
    datos_juego = {
        "puntaje" : 0,
        "cantidad_vidas" : var.CANTIDAD_VIDAS,
        "player" : {},
        "music_config" : 
        {
            "music_volume" : var.vOLUMEN_INICIAL,
            "music_on": True,
            "music_init" : False
        }
    }

    form_control = form_controller.create_form_controller(pantalla_juego, datos_juego) # modulo controlador de formularios para eventos

    while corriendo:

        reloj.tick(var.FPS)
        eventos = pg.event.get()
        
        for evento in eventos:

            if evento.type == pg.QUIT:
                corriendo = False
            
        form_controller.update(form_control,eventos) # <- aca actualiza los eventos en pantalla
        pg.display.flip() # <- aca muestra al usuario los cambios en pantalla. fLIP() actualiza todos los widgets <> Update() actualiza cosas concretas por parametros


    