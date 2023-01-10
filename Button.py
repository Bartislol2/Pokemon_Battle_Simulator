import pygame
from Pokemon import Pokemon


class Button:
    def __init__(self, id_pokemon):
        self.pokemon = Pokemon(id_pokemon, 50, 200, 377)
        self.font = pygame.font.SysFont("Aldrich", 22)
        self.text = self.font.render((str(self.pokemon.pokedex_id)+". "+self.pokemon.name), True, (255, 255, 255))

    def draw(self, surface, rect, info_rect):

        self.rect = rect
        pygame.draw.rect(surface, (105, 105, 105), rect)
        pygame.draw.rect(surface, (70, 70, 70), rect, 3)
        text_rect = self.text.get_rect()
        text_rect.center = rect.center
        surface.blit(self.text, text_rect)

        pos = pygame.mouse.get_pos()

        if rect.collidepoint(pos):
            pygame.draw.rect(surface, (255, 255, 255), rect, 3)
            surface.blit(self.pokemon.image, info_rect.info_rect)
            i = 0
            for p_type in self.pokemon.types:
                path = "sprites/types/" + str(p_type) + ".png"
                image = pygame.image.load(path)
                surface.blit(image, (info_rect.info_rect.x + self.pokemon.image.get_width()//2 - image.get_width()//2, info_rect.info_rect.y + 96 + i * 13))
                i = i+1
            hp_text = self.font.render("HP: " + str(self.pokemon.hp), True, (255, 255, 255))
            atk_text = self.font.render("ATK: " + str(self.pokemon.attack), True, (255, 255, 255))
            sp_atk_text = self.font.render("SP_ATK: " + str(self.pokemon.special_attack), True, (255, 255, 255))
            def_text = self.font.render("DEF: " + str(self.pokemon.defense), True, (255, 255, 255))
            sp_def_text = self.font.render("SP_DEF: " + str(self.pokemon.special_defense), True, (255, 255, 255))
            speed_text = self.font.render("SPEED: " + str(self.pokemon.speed), True, (255, 255, 255))
            text = [hp_text, atk_text, sp_atk_text, def_text, sp_def_text, speed_text]
            i = 0
            for t in text:
                surface.blit(t, (info_rect.info_rect.x + 106, info_rect.info_rect.y + 10 + i * 25))
                i = i + 1




