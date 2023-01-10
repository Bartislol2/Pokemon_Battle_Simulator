import pygame
from Button import Button

class ButtonList:

    def __init__(self, gen_name, x, y):
        self.rect = pygame.Rect(x, y, 200, 75)
        self.font = pygame.font.SysFont("Aldrich", 22)
        self.text = self.font.render(gen_name, True, (255, 255, 255))
        self.buttons = []
        self.clicked = False
        self.gen = gen_name
        self.first_to_draw = 0
        self.how_many = 6
        if gen_name == "Gen1":
            self.first = 1
            self.last = 151
        if gen_name == "Gen2":
            self.first = 152
            self.last = 251
        if gen_name == "Gen3":
            self.first = 252
            self.last = 386
        if gen_name == "Gen4":
            self.first = 387
            self.last = 493
        if gen_name == "Gen5":
            self.first = 494
            self.last = 649
        i = self.first
        while i <= self.last:
            b = Button(i)
            self.buttons.append(b)
            i = i + 1

    def draw(self, surface, first_to_draw, how_many, info_rect):

        pygame.draw.rect(surface, (105, 105, 105), self.rect)
        pygame.draw.rect(surface, (70, 70, 70), self.rect, 3)
        text_rect = self.text.get_rect()
        text_rect.center = self.rect.center
        surface.blit(self.text, text_rect)

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 3)

        if self.clicked:
            i = 0
            while i < how_many:
                rect = pygame.Rect(self.rect.x, self.rect.y + (i+1) * 75, 200, 75)
                self.buttons[(first_to_draw + i)].draw(surface, rect, info_rect)
                i = i + 1













