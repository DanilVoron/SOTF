import sys
from pygame import mixer
import pygame
import random

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
    global effects_volume
    start_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, 'new game', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')
    load_game_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, 'load game', 'images/buttons/button.png',
                                   'images/buttons/h_button.png', 'sounds/click.mp3')
    quit_button = ImageButton(WIDTH / 2 - (252 / 2), 950, 252, 74, 'quit', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')
    settings_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, 'settings', 'images/buttons/button.png',
                                  'images/buttons/h_button.png', 'sounds/click.mp3')

    # Настройка звука для главного меню: только эффект 3
    effect1.stop()
    effect2.stop()
    effect3.set_volume(effects_volume)
    effect3.play(loops=-1, fade_ms=5000)

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
                settings_menu('main')

            if event.type == pygame.USEREVENT and event.button == start_button:
                print("start")
                new_game()
                # После возврата из игры снова включаем музыку меню с сохранённой громкостью
                effect1.stop()
                effect2.stop()
                effect3.set_volume(effects_volume)
                effect3.play(loops=-1, fade_ms=5000)

            if event.type == pygame.USEREVENT and event.button == load_game_button:
                print("load data")
                load_game()
                # После возврата из загрузки снова включаем музыку меню с сохранённой громкостью
                effect1.stop()
                effect2.stop()
                effect3.set_volume(effects_volume)
                effect3.play(loops=-1, fade_ms=5000)

        for btn in [start_button, load_game_button, quit_button, settings_button]:
            btn.handle_event(event)

        for btn in [start_button, load_game_button, quit_button, settings_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 10, y ))
        pygame.display.flip()


def settings_menu(location='main', bg_image=None, light_x=0, light_y=0, light_r=0):
    global effects_volume
    audio_button = ImageButton(WIDTH / 2 - (252 / 2), 50, 252, 74, 'audio', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')
    video_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, 'video', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, 'back', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')

    volume_slider = Slider(WIDTH/2 - 200, 250, 400, 20)
    slider_visible = False

    # Определяем фон в зависимости от локации
    if location == 'game' and bg_image:
        current_bg = bg_image
        has_lighting = True
    else:
        current_bg = main_background
        has_lighting = False

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 0))
        screen.blit(current_bg, (200, + 30))

        # Если вызвано из игры, добавляем освещение и затемнение как в окне подтверждения
        if has_lighting:
            # Создаем поверхность для освещения
            light_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            light_surf.fill((0, 0, 0, 0))

            # Рисуем свет с теми же параметрами, что были в игре
            for i in range(20, 0, -1):
                r = int(light_r * (i / 20))
                circle_alpha = int(200 * (1 - (i / 20)))
                pygame.draw.circle(light_surf, (0, 0, 0, circle_alpha), (light_x, light_y), r)

            screen.blit(light_surf, (0, 0))

            # Добавляем полупрозрачный затемняющий слой поверх всего
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

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
        clock.tick(60)


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
    effect1.set_volume(effects_volume)
    effect2.set_volume(effects_volume)
    effect1.play(loops=-1, fade_ms=2000)
    effect2.play(loops=-1, fade_ms=2000)

    # Координаты лампы на кухне (центр сверху)
    light_center_x = WIDTH // 2
    light_center_y = 150

    # Параметры освещения - уменьшенный радиус и светло-оранжевый цвет
    base_light_radius = 300  # Уменьшенный базовый радиус
    current_light_radius = base_light_radius
    light_color = (255, 200, 100)  # Светло-оранжевый цвет

    flicker_timer = 0
    is_flickering = False  # Флаг затухания

    # Кнопка выхода в меню (левый верхний угол, 80x50)
    exit_button = ImageButton(10, 10, 80, 50, 'esc', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')

    # Кнопка настроек под кнопкой выхода (10, 70, 80x50)
    settings_btn = ImageButton(10, 70, 80, 50, 'set', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 0))
        screen.blit(kitchenbg, (200, 30))

        # --- Логика мерцания света ---
        if is_flickering:
            # Быстрое затухание - фон становится темнее
            current_light_radius -= 15
            if current_light_radius < 50:
                is_flickering = False
        else:
            # Плавное возвращение к нормальному размеру
            if current_light_radius < base_light_radius:
                current_light_radius += 5
            else:
                # Небольшие случайные колебания вокруг базового радиуса
                current_light_radius = base_light_radius + random.randint(-10, 10)

            # Шанс на начало затухания (2% каждый кадр)
            if random.random() < 0.02:
                is_flickering = True

        # --- Отрисовка освещения (светло-оранжевое с градиентом) ---
        light_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Рисуем несколько кругов для мягкого градиента от центра к краям
        for i in range(10, 0, -1):
            alpha = int(80 * (i / 10))  # Прозрачность уменьшается к краям
            radius = int(current_light_radius * (i / 10))
            if radius > 0:
                color_with_alpha = (*light_color, alpha)
                pygame.draw.circle(light_surface, color_with_alpha, (light_center_x, light_center_y), radius)

        screen.blit(light_surface, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Проверка нажатия на кнопку ESC или клик по кнопке выхода
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if show_confirm_dialog(kitchenbg, light_center_x, light_center_y, current_light_radius, light_color):
                    return  # Выход из new_game и возврат в main_menu

            if event.type == pygame.USEREVENT and event.button == exit_button:
                if show_confirm_dialog(kitchenbg, light_center_x, light_center_y, current_light_radius, light_color):
                    return  # Выход из new_game и возврат в main_menu

            if event.type == pygame.USEREVENT and event.button == settings_btn:
                settings_menu('game', kitchenbg, light_center_x, light_center_y, current_light_radius, light_color)
                # После возврата из настроек продолжаем игру с той же музыкой и громкостью
                effect1.set_volume(effects_volume)
                effect2.set_volume(effects_volume)

            exit_button.handle_event(event)
            settings_btn.handle_event(event)

        exit_button.check_hover(pygame.mouse.get_pos())
        settings_btn.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen)
        settings_btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 10, y))

        pygame.display.flip()
        clock.tick(60)


def show_confirm_dialog(background_image, light_x=0, light_y=0, light_r=0, light_color=(255, 255, 255)):
    """Показывает окно подтверждения выхода в главное меню.
    Возвращает True, если нужно выйти в меню.
    background_image - изображение текущей локации для затемнения.
    light_x, light_y, light_r - параметры освещения для реалистичного отображения.
    light_color - цвет освещения."""
    dialog_width, dialog_height = 600, 400
    dialog_x = WIDTH // 2 - dialog_width // 2
    dialog_y = HEIGHT // 2 - dialog_height // 2

    # Создаём кнопки Да и Нет
    yes_button = ImageButton(dialog_x + 50, dialog_y + 250, 200, 74, 'yes', 'images/buttons/button.png',
                             'images/buttons/h_button.png', 'sounds/click.mp3')
    no_button = ImageButton(dialog_x + 350, dialog_y + 250, 200, 74, 'no', 'images/buttons/button.png',
                            'images/buttons/h_button.png', 'sounds/click.mp3')

    dialog_running = True
    result = False  # Флаг для возврата результата

    # Проверяем, переданы ли параметры освещения (значит вызов из игры)
    has_lighting = light_r > 0

    while dialog_running:
        # Рисуем текущую локацию
        screen.fill((0, 0, 0))
        screen.blit(background_image, (200, 30))

        # Если есть освещение, рисуем его
        if has_lighting:
            light_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

            # Рисуем светло-оранжевое освещение с градиентом
            for i in range(10, 0, -1):
                alpha = int(80 * (i / 10))
                radius = int(light_r * (i / 10))
                if radius > 0:
                    color_with_alpha = (*light_color, alpha)
                    pygame.draw.circle(light_surf, color_with_alpha, (light_x, light_y), radius)

            screen.blit(light_surf, (0, 0))

        # Рисуем полупрозрачный затемняющий слой поверх локации
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
                result = True  # Пользователь согласился выйти
                break

            if event.type == pygame.USEREVENT and event.button == no_button:
                dialog_running = False
                result = False  # Пользователь отказался
                break

            yes_button.handle_event(event)
            no_button.handle_event(event)

        yes_button.check_hover(pygame.mouse.get_pos())
        no_button.check_hover(pygame.mouse.get_pos())
        yes_button.draw(screen)
        no_button.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 10, y))

        pygame.display.flip()

    return result


# ------------------GAME PROCESS-------------------------
main_menu()
