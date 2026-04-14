import sys
from pygame import mixer
import pygame

from Button import ImageButton

pygame.init()
mixer.init()

pygame.mixer.set_num_channels(10)

effect1 = pygame.mixer.Sound('sounds/fridge_sound.mp3')
effect2 = pygame.mixer.Sound('sounds/watch_tick.mp3')
effect3 = pygame.mixer.Sound('sounds/main_menu_ambient.mp3')
effect4 = pygame.mixer.Sound('sounds/firefly.mp3')


# -------------DISPLAY_SETTINGS---------------------------

WIDTH, HEIGHT = 1920, 1080

pygame.display.set_caption("HORROR")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(pygame.image.load('images/icon.png'))
main_background = pygame.image.load('images/BGs/background.png')
kitchenbg = pygame.image.load('images/BGs/kitchen/kitchen.png')

cursor = pygame.image.load('images/cursor.png')
cursor = pygame.transform.scale(cursor, (35, 35))
pygame.mouse.set_visible(False)

effect3.set_volume(0.2)
effect3.play(loops=-1, fade_ms=5000)


#--------------------------AUDIOSLIDER----------------------------------

# Глобальная переменная для хранения громкости эффектов
effects_volume = 0.5

class Slider:
    def __init__(self, x, y, width, height, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_value
        self.knob_rect = pygame.Rect(x + width * initial_value - height // 2, y, height, height)
        self.dragging = False

    def draw(self, surface):
        # Рисуем ползунок
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.knob_rect)

    def handle_event(self, event):
        global effects_volume
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x_pos = event.pos[0] - self.rect.x
            self.value = max(0, min(1, x_pos / self.rect.width))
            self.knob_rect.x = self.rect.x + self.value * self.rect.width - self.knob_rect.width // 2
            effects_volume = self.value
            mixer.music.set_volume(self.value)  # Устанавливаем громкость музыки
            # Устанавливаем громкость всех звуковых эффектов
            effect1.set_volume(effects_volume)
            effect2.set_volume(effects_volume)
            effect3.set_volume(effects_volume)
            effect4.set_volume(effects_volume)


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

    volume_slider = Slider(WIDTH/2 - 200, 250, 400, 20)
    slider_visible = False

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (200, + 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == audio_button:
                slider_visible = True

            elif event.type == pygame.USEREVENT and event.button == back_button:
                running = False

            volume_slider.handle_event(event) if slider_visible else None


            for btn in [audio_button, video_button, back_button]:
                btn.handle_event(event)

        for btn in [audio_button, video_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        if slider_visible:
            volume_slider.draw(screen)

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

    effect3.stop()
    effect1.set_volume(0.2)
    effect2.set_volume(0.2)
    effect1.play(loops=-1, fade_ms=2000)
    effect2.play(loops=-1, fade_ms=2000)

    # Кнопка выхода в меню (левый верхний угол, 80x50)
    exit_button = ImageButton(10, 10, 80, 50, 'esc', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(kitchenbg, (200, + 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Проверка нажатия на кнопку ESC или клик по кнопке выхода
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                show_confirm_dialog()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                show_confirm_dialog()

            exit_button.handle_event(event)

        exit_button.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 10, y))

        pygame.display.flip()


def show_confirm_dialog():
    """Показывает окно подтверждения выхода в главное меню"""
    dialog_width, dialog_height = 600, 400
    dialog_x = WIDTH // 2 - dialog_width // 2
    dialog_y = HEIGHT // 2 - dialog_height // 2

    # Создаём кнопки Да и Нет
    yes_button = ImageButton(dialog_x + 50, dialog_y + 250, 200, 74, 'yes', 'images/buttons/button.png',
                             'images/buttons/h_button.png', 'sounds/click.mp3')
    no_button = ImageButton(dialog_x + 350, dialog_y + 250, 200, 74, 'no', 'images/buttons/button.png',
                            'images/buttons/h_button.png', 'sounds/click.mp3')

    dialog_running = True
    while dialog_running:
        # Рисуем полупрозрачный фон поверх игры
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Рисуем окно подтверждения
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, (50, 50, 50), dialog_rect)
        pygame.draw.rect(screen, (200, 200, 200), dialog_rect, 3)

        # Текст вопроса
        font = pygame.font.Font(None, 48)
        text = font.render("Вы хотите выйти в главное меню?", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, dialog_y + 100))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == yes_button:
                dialog_running = False
                # Прерываем new_game и запускаем main_menu
                main_menu()
                return

            if event.type == pygame.USEREVENT and event.button == no_button:
                dialog_running = False
                return

            yes_button.handle_event(event)
            no_button.handle_event(event)

        yes_button.check_hover(pygame.mouse.get_pos())
        no_button.check_hover(pygame.mouse.get_pos())
        yes_button.draw(screen)
        no_button.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 10, y))

        pygame.display.flip()


# ------------------GAME PROCESS-------------------------
main_menu()
