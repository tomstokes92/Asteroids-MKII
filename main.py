import os
# set audio device
os.environ["SDL_AUDIODRIVER"] = "pulseaudio"
import pygame
import sys
import constants
import game_menu
import settings_manager
import game


# audio crash protection
def init_audio():
    try:
        pygame.mixer.init()
        print("Audio initialised")
    except pygame.error:
        print("Audio unavailable, continuing without sound")
def main():
    # initialise game engines
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
    pygame.init()
    init_audio()
    settings = settings_manager.load_settings()
    # set parameter variables for pygame
    screen = pygame.display.set_mode(tuple(settings["resolution"]))
    pygame.display.set_caption("Space Goose")
    clock = pygame.time.Clock()

    running = True
    while running:
        menu_result = game_menu.show_menu(screen, clock, settings)
        if menu_result == "start":
            game.run_game(screen, clock)
        else:
            running = False
    pygame.quit()

if __name__ == "__main__":
    main()
