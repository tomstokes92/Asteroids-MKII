import pygame

def apply_volume(settings, sfx_sounds=()):
    vol = max(0, min(100, settings["volume"])) / 100.0
    for s in sfx_sounds:
        if s is not None:
            s.set_volume(vol)
    try:
        pygame.mixer.music.set_volume(vol)
    except pygame.error:
        pass

def play_music(path, settings, loop=True):
    try:
        pygame.mixer.music.load(path)
        apply_volume(settings)
        pygame.mixer.music.play(-1 if loop else 0)
    except pygame.error:
        pass
def stop_music():
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        pass