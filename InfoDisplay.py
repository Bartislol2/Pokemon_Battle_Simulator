import pygame

pygame.init()

class InfoDisplay():
    def __init__(self, x, y, width, height):
        self.info_rect = pygame.Rect(x, y, width, height)
