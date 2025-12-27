import pygame
import sys
import constants
import random

from audio import apply_volume

def show_menu(screen, clock):
    pygame.display.set_caption("Space Goose Menu")

    menu_options = ["Start Game", "Settings", "Quit"]
    selected_option = 0
    menu_active = True

    # Settings dict
    settings = {
        "volume": 50,
        "resolution": (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    }

    move_sound = pygame.mixer.Sound("./sounds/menu_move.wav")
    select_sound = pygame.mixer.Sound("./sounds/menu_select.wav")
    apply_volume(settings, (move_sound, select_sound))
    menu_font = pygame.font.Font("./fonts/Vaseline Extra.ttf", 60)
    title_font = pygame.font.Font("./fonts/Championship.ttf", 100)



    # Snowflake initialization
    screen_width, screen_height = screen.get_size()
    NUM_SNOWFLAKES = 100
    snowflakes = []
    for _ in range(NUM_SNOWFLAKES):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        speed_y = random.uniform(0.3, 1.5)
        drift_x = random.uniform(0.3, 1)
        size = random.randint(2, 4)
        snowflakes.append([x, y, speed_y, drift_x, size])

    # Draw snowflakes dynamically
    def draw_snowflakes():
        screen_width, screen_height = screen.get_size()
        for flake in snowflakes:
            flake[0] += flake[3]
            flake[1] += flake[2]

            # Wrap vertically
            if flake[1] > screen_height:
                flake[1] = 0
                flake[0] = random.randint(0, screen_width)

            # Wrap horizontally
            if flake[0] < 0:
                flake[0] = screen_width
            elif flake[0] > screen_width:
                flake[0] = 0

            pygame.draw.circle(screen, constants.WHITE, (int(flake[0]), int(flake[1])), flake[4])

    # Draw main menu
    def draw_menu():
        screen.fill(constants.BLACK)
        draw_snowflakes()

        screen_width, screen_height = screen.get_size()

        # Title
        title_text = title_font.render("SPACE GOOSE", True, "gold")
        title_rect = title_text.get_rect(center=(screen_width // 2, 150))
        screen.blit(title_text, title_rect)

        # Menu options
        for i, option in enumerate(menu_options):
            display_text = f"> {option} <" if i == selected_option else option
            colour = constants.WHITE if i == selected_option else constants.GRAY
            text = menu_font.render(display_text, True, colour)
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 100))
            screen.blit(text, text_rect)

    # Main menu loop
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_option = (selected_option - 1) % len(menu_options)
                    move_sound.play()
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_option = (selected_option + 1) % len(menu_options)
                    move_sound.play()
                elif event.key == pygame.K_RETURN:
                    select_sound.play()
                    choice = menu_options[selected_option]
                    if choice == "Start Game":
                        menu_active = False
                    elif choice == "Settings":
                        # Open settings menu and update screen if resolution changes
                        screen = show_settings_menu(screen, clock, settings, menu_font, move_sound, select_sound)
                    elif choice == "Quit":
                        pygame.quit()
                        sys.exit()

        draw_menu()
        pygame.display.flip()
        clock.tick(constants.FPS)

    return

def show_settings_menu(screen, clock, settings, menu_font, move_sound, select_sound):
    title_font = pygame.font.Font("./fonts/Vaseline Extra.ttf", 100)
    menu_options = [
        "Volume",
        "Screen Size",
        "Player Options (ph)",
        "Back"
    ]
    resolutions = [
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1920, 1080)
    ]
    selected_option = 0
    menu_active = True

    def draw_settings_menu():
        screen.fill(constants.BLACK)
        screen_width, screen_height = screen.get_size()

        # Title
        title_text = title_font.render("Settings", True, "gold")
        title_rect = title_text.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_text, title_rect)

        # Options
        for i, option in enumerate(menu_options):
            display = option
            if option == "Volume":
                display = f"Volume: {settings['volume']}%"
            elif option == "Screen Size":
                w, h = settings["resolution"]
                display = f"Screen Size: {w}x{h}"

            if i == selected_option:
                display = f"> {display} <"
                colour = constants.WHITE
            else:
                colour = constants.GRAY

            text = menu_font.render(display, True, colour)
            text_rect = text.get_rect(center=(screen_width // 2, 260 + i * 80))
            screen.blit(text, text_rect)

    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_option = (selected_option - 1) % len(menu_options)
                    move_sound.play()
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_option = (selected_option + 1) % len(menu_options)
                    move_sound.play()
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    if menu_options[selected_option] == "Volume":
                        settings["volume"] = min(100, settings["volume"] + 5)
                        apply_volume(settings, (move_sound, select_sound))
                        move_sound.play()
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    if menu_options[selected_option] == "Volume":
                        settings["volume"] = max(0, settings["volume"] - 5)
                        apply_volume(settings, (move_sound, select_sound))
                        move_sound.play()
                elif event.key == pygame.K_RETURN:
                    current = menu_options[selected_option]
                    select_sound.play()
                    if current == "Screen Size":
                        idx = resolutions.index(settings["resolution"])
                        settings["resolution"] = resolutions[(idx + 1) % len(resolutions)]
                        screen = pygame.display.set_mode(settings["resolution"])
                    elif current == "Back":
                        menu_active = False

        draw_settings_menu()
        pygame.display.flip()
        clock.tick(constants.FPS)

    return screen
