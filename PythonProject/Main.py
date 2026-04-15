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
kitchenlightoff = pygame.image.load('images/BGs/kitchen/kitchenlightoff.jpg')

cursor = pygame.image.load('images/cursor.png')
cursor = pygame.transform.scale(cursor, (35, 35))
pygame.mouse.set_visible(False)

# Глобальная переменная для хранения громкости эффектов
effects_volume = 0.5

# Переменная для состояния света на кухне (True = свет включен, False = выключен)
kitchen_light_on = True

# Параметры лампы
lamp_x = WIDTH // 2
lamp_y = 150
base_light_radius = 300
current_light_radius = base_light_radius
light_timer = 0
flicker_intensity = 40  # Насколько сильно меняется радиус
dim_duration = 0  # Таймер для состояния "темнее"


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
            # Устанавливаем громкость всех звуковых эффектов
            effect1.set_volume(effects_volume)
            effect2.set_volume(effects_volume)
            effect3.set_volume(effects_volume)
            effect4.set_volume(effects_volume)


def update_lamp_logic():
    """Обновляет логику мерцания лампы"""
    global current_light_radius, light_timer, dim_duration

    # Если свет выключен, не обновляем мерцание
    if not kitchen_light_on:
        return

    light_timer += 1

    # Если идет период затухания
    if dim_duration > 0:
        dim_duration -= 1
        # Плавно уменьшаем радиус до минимума
        target_radius = base_light_radius - flicker_intensity - 20
        current_light_radius += (target_radius - current_light_radius) * 0.1
    else:
        # Обычное мерцание
        if light_timer > 1:  # Обновляем каждые 5 кадров
            light_timer = 0
            # Случайное изменение радиуса
            change = random.randint(-flicker_intensity, flicker_intensity)
            current_light_radius = base_light_radius + change

            # Небольшой шанс на сильное затухание
            if random.random() < 0.01:
                dim_duration = random.randint(2, 8)  # Длительность затухания


def draw_lamp_light(surface, offset_x=0, offset_y=0, alpha=100):
    """Рисует свет лампы с мерцанием"""
    update_lamp_logic()

    # Создаем поверхность для света
    light_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Цвет света: светло-оранжевый
    light_color = (255, 200, 100)

    # Рисуем градиентный круг
    # Внешний круг (полупрозрачный)
    pygame.draw.circle(light_surface, (*light_color, 0), (896, 164), int(current_light_radius * 1.2))

    # Внутренние круги для градиента
    for r in range(int(current_light_radius), 0, -20):
        # Чем ближе к центру, тем меньше альфа (чтобы центр был ярче, но не белым)
        # Но так как мы рисуем поверх, нам нужно наоборот: центр прозрачнее для фона?
        # Нет, обычно свет - это добавление яркости.
        # В данном случае мы рисуем цветной оверлей. Чтобы имитировать свет,
        # центр должен быть более насыщенным, а края прозрачными.

        # Рассчитываем альфу для кольца: максимум в центре, 0 на краю
        ratio = r / current_light_radius
        ring_alpha = int(alpha * (1 - ratio))

        if ring_alpha > 0:
            # Рисуем кольцо
            pygame.draw.circle(light_surface, (*light_color, ring_alpha), (lamp_x, lamp_y), r, 2)

    surface.blit(light_surface, (0, 0))


# ------------------MENU--------------------------------

def main_menu():
    global effects_volume
    # Настройка звука для меню - включаем только 3 эффект
    effect1.stop()
    effect2.stop()
    effect3.stop()
    effect3.set_volume(effects_volume)
    effect3.play(loops=-1, fade_ms=2000)

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
        screen.blit(main_background, (200, 30))

        # Лампа в меню (если нужна, или только в игре? По ТЗ "на кухне", но пусть будет универсально)
        # В ТЗ сказано "вокруг лампы на кухне", значит в меню свет не рисуем, только фон.
        # Но если нужно освещение и в меню, раскомментируйте draw_lamp_light(screen)

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
                settings_menu(is_in_game=False)

            if event.type == pygame.USEREVENT and event.button == start_button:
                new_game()
                # После возврата из игры переключаем звук обратно на меню
                effect1.stop()
                effect2.stop()
                effect3.set_volume(effects_volume)
                effect3.play(loops=-1, fade_ms=2000)

            if event.type == pygame.USEREVENT and event.button == load_game_button:
                load_game()
                # После возврата из загрузки игры переключаем звук обратно на меню
                effect1.stop()
                effect2.stop()
                effect3.set_volume(effects_volume)
                effect3.play(loops=-1, fade_ms=2000)

            # Обработка кнопок
            for btn in [start_button, load_game_button, quit_button, settings_button]:
                btn.handle_event(event)

        for btn in [start_button, load_game_button, quit_button, settings_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # Отрисовка курсора и координат
        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor, (mx - 10, my))

        # Вывод координат
        font_small = pygame.font.Font(None, 20)
        coord_text = f"x: {mx} y: {my}"
        text_surf = font_small.render(coord_text, True, (255, 255, 255))
        screen.blit(text_surf, (mx + 20, my + 5))

        pygame.display.flip()


def settings_menu(is_in_game=False):
    global effects_volume

    audio_button = ImageButton(WIDTH / 2 - (252 / 2), 50, 252, 74, 'audio', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')
    video_button = ImageButton(WIDTH / 2 - (252 / 2), 150, 252, 74, 'video', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, 'back', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')

    volume_slider = Slider(WIDTH / 2 - 200, 250, 400, 20)
    slider_visible = False

    # Определяем фон в зависимости от того, где вызваны настройки
    bg_image = kitchenbg if is_in_game else main_background

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg_image, (200, 30))

        # Если настройки вызваны в игре, рисуем свет лампы и затемнение
        if is_in_game:
            draw_lamp_light(screen)
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

            if slider_visible:
                volume_slider.handle_event(event)

            for btn in [audio_button, video_button, back_button]:
                btn.handle_event(event)

        for btn in [audio_button, video_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        if slider_visible:
            volume_slider.draw(screen)

        # Курсор и координаты
        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor, (mx - 10, my))
        font_small = pygame.font.Font(None, 20)
        coord_text = f"x: {mx} y: {my}"
        text_surf = font_small.render(coord_text, True, (255, 255, 255))
        screen.blit(text_surf, (mx + 20, my + 5))

        pygame.display.flip()


def load_game():
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, 'back', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (200, 30))

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

        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor, (mx - 10, my))
        font_small = pygame.font.Font(None, 20)
        coord_text = f"x: {mx} y: {my}"
        text_surf = font_small.render(coord_text, True, (255, 255, 255))
        screen.blit(text_surf, (mx + 20, my + 5))

        pygame.display.flip()


def new_game():
    global effects_volume, kitchen_light_on
    # Настройка звука для игры
    effect3.stop()
    effect1.set_volume(effects_volume)
    effect2.set_volume(effects_volume)
    effect1.play(loops=-1, fade_ms=2000)
    effect2.play(loops=-1, fade_ms=2000)

    # Кнопки в левом верхнем углу
    exit_button = ImageButton(10, 10, 80, 50, 'esc', 'images/buttons/button.png',
                              'images/buttons/h_button.png', 'sounds/click.mp3')
    settings_btn = ImageButton(10, 70, 80, 50, 'set', 'images/buttons/button.png',
                               'images/buttons/h_button.png', 'sounds/click.mp3')
    turnlight_button = ImageButton(10, 130, 150, 50, 'turnlight', 'images/buttons/button.png',
                                   'images/buttons/h_button.png', 'sounds/click.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        
        # Выбираем фон в зависимости от состояния света
        if kitchen_light_on:
            screen.blit(kitchenbg, (200, 30))
        else:
            screen.blit(kitchenlightoff, (200, 30))

        # Рисуем свет лампы только если свет включен
        if kitchen_light_on:
            draw_lamp_light(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if show_confirm_dialog():
                    return

            if event.type == pygame.USEREVENT and event.button == exit_button:
                if show_confirm_dialog():
                    return

            if event.type == pygame.USEREVENT and event.button == settings_btn:
                settings_menu(is_in_game=True)

            if event.type == pygame.USEREVENT and event.button == turnlight_button:
                # Переключаем состояние света
                kitchen_light_on = not kitchen_light_on

            exit_button.handle_event(event)
            settings_btn.handle_event(event)
            turnlight_button.handle_event(event)

        exit_button.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen)
        settings_btn.check_hover(pygame.mouse.get_pos())
        settings_btn.draw(screen)
        turnlight_button.check_hover(pygame.mouse.get_pos())
        turnlight_button.draw(screen)

        # Курсор и координаты
        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor, (mx - 10, my))
        font_small = pygame.font.Font(None, 20)
        coord_text = f"x: {mx} y: {my}"
        text_surf = font_small.render(coord_text, True, (255, 255, 255))
        screen.blit(text_surf, (mx + 20, my + 5))

        pygame.display.flip()


def show_confirm_dialog():
    """Показывает окно подтверждения выхода в главное меню."""
    dialog_width, dialog_height = 600, 400
    dialog_x = WIDTH // 2 - dialog_width // 2
    dialog_y = HEIGHT // 2 - dialog_height // 2

    yes_button = ImageButton(dialog_x + 50, dialog_y + 250, 200, 74, 'yes', 'images/buttons/button.png',
                             'images/buttons/h_button.png', 'sounds/click.mp3')
    no_button = ImageButton(dialog_x + 350, dialog_y + 250, 200, 74, 'no', 'images/buttons/button.png',
                            'images/buttons/h_button.png', 'sounds/click.mp3')

    dialog_running = True
    result = False

    # Очищаем события, чтобы случайные клики не передались в диалог
    pygame.event.clear()

    while dialog_running:
        # Рисуем текущий кадр игры под затемнением (свет лампы уже нарисован в цикле new_game,
        # но так как мы в новом цикле, нужно перерисовать фон и свет)
        screen.fill((0, 0, 0))
        
        # Выбираем фон в зависимости от состояния света
        if kitchen_light_on:
            screen.blit(kitchenbg, (200, 30))
        else:
            screen.blit(kitchenlightoff, (200, 30))
        
        # Рисуем свет лампы только если свет включен
        if kitchen_light_on:
            draw_lamp_light(screen)

        # Затемнение
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Окно подтверждения
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, (50, 50, 50), dialog_rect)
        pygame.draw.rect(screen, (200, 200, 200), dialog_rect, 3)

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
                result = True
                break

            if event.type == pygame.USEREVENT and event.button == no_button:
                dialog_running = False
                result = False
                break

            yes_button.handle_event(event)
            no_button.handle_event(event)

        yes_button.check_hover(pygame.mouse.get_pos())
        no_button.check_hover(pygame.mouse.get_pos())
        yes_button.draw(screen)
        no_button.draw(screen)

        # Курсор и координаты в диалоге
        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor, (mx - 10, my))
        font_small = pygame.font.Font(None, 20)
        coord_text = f"x: {mx} y: {my}"
        text_surf = font_small.render(coord_text, True, (255, 255, 255))
        screen.blit(text_surf, (mx + 20, my + 5))

        pygame.display.flip()

    return result


# ------------------GAME PROCESS-------------------------
main_menu()
