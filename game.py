import pygame
import constants
from ship import Ship
import sys

def run_game(screen, clock):
    ship = Ship(screen.get_width() / 2, screen.get_height() / 2)
    running = True
    while running:
        dt = clock.tick(constants.FPS) / 1000.0  # seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
        keys = pygame.key.get_pressed()

        w, h = screen.get_size()
        ship.update(dt, keys, w, h)

        screen.fill(constants.BLACK)
        ship.draw(screen)
        pygame.display.flip()