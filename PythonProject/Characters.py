import pygame

class Character:

    def __init__(self):
        self.image = pygame.image.load('images/character.png')
        self.rect = self.image.get_rect()