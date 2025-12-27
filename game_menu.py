import pygame
import sys
import constants
import os

def show_menu(screen, font, clock):
    pygame.display.set_caption("Space Goose Menu")
    menu_font = pygame.font.Font("./fonts/Vaseline Extra.ttf", 60)
    title_font = pygame.font.Font("./fonts/Championship.ttf", 100)
    menu_options = ["Start Game", "Settings", "Quit"]
    selected_option = 0
    menu_active = True
    

    def draw_menu():
        screen.fill(constants.BLACK)
        # Title        
        title_text = title_font.render("SPACE GOOSE", True, "gold")
        title_rect = title_text.get_rect(center=(constants.SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        for i, option in enumerate(menu_options):
            if i == selected_option:
                display_text = f"> {option} <"
                colour = constants.WHITE
            else: 
                display_text = option
                colour = constants.GRAY
            text = menu_font.render(display_text, True, colour)
            text_rect = text.get_rect(center=(constants.SCREEN_WIDTH // 2,
                                              constants.SCREEN_HEIGHT // 2 + i * 100))
            screen.blit(text, text_rect)
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_option] == "Start Game":
                        menu_active = False
                    elif menu_options[selected_option] ==  "Settings":
                        pass
                    elif menu_options[selected_option] == "Quit":
                        pygame.quit()
                        sys.exit()           
        draw_menu()
        pygame.display.flip()
        clock.tick(constants.FPS)
    return

