import pygame

pygame.init()

def get_player_sprite(sex):
    path = "sprites/"+sex+".png"
    image = pygame.image.load(path)
    return image

class Player():
    def __init__(self, sex, name):
        self.sex = sex
        self.name = name
        self.image = get_player_sprite(sex)
        self.pokemon = []
