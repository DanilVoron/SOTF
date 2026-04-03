import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.mixer.music.load('sounds/firefly.mp3')
pygame.mixer.music.play(-1)

slider_x = 50
slider_y = 100
slider_width = 300
slider_height = 20
slider_pos = slider_x  # Текущая позиция ползунка

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, _ = pygame.mouse.get_pos()
            if slider_x <= mouse_x <= slider_x + slider_width:
                slider_pos = mouse_x
        if event.type == pygame.MOUSEMOTION:
            mouse_x, _ = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if slider_x <= mouse_x <= slider_x + slider_width:
                    slider_pos = mouse_x

    # Вычисляем громкость в зависимости от положения ползунка
    volume = (slider_pos - slider_x) / slider_width
    pygame.mixer.music.set_volume(volume)

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.circle(screen, (255, 0, 0), (int(slider_pos), slider_y + slider_height // 2), 12)
    pygame.display.flip()

pygame.quit()