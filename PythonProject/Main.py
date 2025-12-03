import sys

import pygame

from Button import ImageButton

pygame.init()

# -------------DISPLAY_SETTINGS---------------------------

WIDTH, HEIGHT = 1920, 1080

pygame.display.set_caption("HORROR")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(pygame.image.load('images/icon.png'))
main_background = pygame.image.load('images/BGs/background.png')
kitchenbg = pygame.image.load('images/BGs/kitchen.png')

cursor = pygame.image.load('images/cursor.png')
cursor = pygame.transform.scale(cursor, (35, 35))
pygame.mouse.set_visible(False)


# ------------------MENU--------------------------------

def main_menu():
    start_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, 'new game', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')
    load_game_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, 'load game', 'images/buttons/button.png',
                                   'images/buttons/h_button.png', 'sounds/click.mp3')
    quit_button = ImageButton(WIDTH / 2 - (252 / 2), 950, 252, 74, 'quit', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')
    settings_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, 'settings', 'images/buttons/button.png',
                                  'images/buttons/h_button.png', 'sounds/click.mp3')

    running = True
    while running:

        screen.fill((0, 0, 0))
        screen.blit(main_background, (200, + 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == quit_button:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                print("settings")
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == start_button:
                print("start")
                new_game()

            if event.type == pygame.USEREVENT and event.button == load_game_button:
                print("load data")
                load_game()

        for btn in [start_button, load_game_button, quit_button, settings_button]:
            btn.handle_event(event)

        for btn in [start_button, load_game_button, quit_button, settings_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 10, y ))
        pygame.display.flip()


def settings_menu():
    audio_button = ImageButton(WIDTH / 2 - (252 / 2), 50, 252, 74, 'audio', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')
    video_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, 'video', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, 'back', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (200, + 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False

            for btn in [audio_button, video_button, back_button]:
                btn.handle_event(event)

        for btn in [audio_button, video_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 10, y ))

        pygame.display.flip()


def load_game():
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, 'back', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (200, + 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False

            for btn in [back_button]:
                btn.handle_event(event)

        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 10, y ))

        pygame.display.flip()

def new_game():

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(kitchenbg, (200, + 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()


        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 10, y))

        pygame.display.flip()


# ------------------GAME PROCESS-------------------------
main_menu()

