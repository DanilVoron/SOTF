import pygame
pygame.init()

pygame.display.set_caption("HORROR")
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_icon(pygame.image.load('images/icon.png'))

screen.fill((18, 17, 20))

running = True
while running:



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()