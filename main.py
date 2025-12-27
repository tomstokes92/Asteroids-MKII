import pygame
import sys
import constants
import game_menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Goose")
    font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    # Pass screen and font to menu
    game_menu.show_menu(screen, font, clock)

    # Start game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(constants.BLACK)
        pygame.display.flip()
        clock.tick(constants.FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
