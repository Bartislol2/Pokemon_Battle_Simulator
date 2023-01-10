import random
import pygame
import json
import requests
from Move import Move
import math

# initialize pygame modules
pygame.init()

# open the json file
with open("pokemon.json") as json_file:
    data = json.load(json_file)

base_url = "https://pokeapi.co/api/v2"

typing_dict = [
    {
        "Type": "Normal",
        "Weak_to": ["Fighting"],
        "Resists": [],
        "Immunity": ["Ghost"]
    },
    {
        "Type": "Fire",
        "Weak_to": ["Water", "Ground", "Rock"],
        "Resists": ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"],
        "Immunity": []
    },
    {
        "Type": "Water",
        "Weak_to": ["Electric", "Grass"],
        "Resists": ["Fire", "Water", "Ice", "Steel"],
        "Immunity": []
    },
    {
        "Type": "Electric",
        "Weak_to": ["Ground"],
        "Resists": ["Electric", "Flying", "Steel"],
        "Immunity": []
    },
    {
        "Type": "Grass",
        "Weak_to": ["Fire", "Ice", "Poison", "Flying", "Bug"],
        "Resists": ["Electric", "Water", "Grass", "Ground"],
        "Immunity": []
    },
    {
        "Type": "Ice",
        "Weak_to": ["Fire", "Fighting", "Rock", "Steel"],
        "Resists": ["Ice"],
        "Immunity": []
    },
    {
        "Type": "Fighting",
        "Weak_to": ["Flying", "Psychic", "Fairy"],
        "Resists": ["Bug", "Rock", "Dark"],
        "Immunity": []
    },
    {
        "Type": "Poison",
        "Weak_to": ["Ground", "Psychic"],
        "Resists": ["Grass", "Fighting", "Poison", "Bug", "Fairy"],
        "Immunity": []
    },
    {
        "Type": "Ground",
        "Weak_to": ["Water", "Grass", "Ice"],
        "Resists": ["Poison", "Rock"],
        "Immunity": ["Electric"]
    },
    {
        "Type": "Flying",
        "Weak_to": ["Electric", "Ice", "Rock"],
        "Resists": ["Grass", "Fighting", "Bug"],
        "Immunity": ["Ground"]
    },
    {
        "Type": "Psychic",
        "Weak_to": ["Bug", "Ghost", "Dark"],
        "Resists": ["Fighting", "Psychic"],
        "Immunity": []
    },
    {
        "Type": "Bug",
        "Weak_to": ["Fire", "Flying", "Rock"],
        "Resists": ["Fighting", "Grass", "Ground"],
        "Immunity": []
    },
    {
        "Type": "Rock",
        "Weak_to": ["Water", "Grass", "Fighting", "Ground"],
        "Resists": ["Normal", "Fire", "Poison", "Flying"],
        "Immunity": []
    },
    {
        "Type": "Ghost",
        "Weak_to": ["Ghost", "Dark"],
        "Resists": ["Poison", "Bug"],
        "Immunity": ["Normal", "Fighting"]
    },
    {
        "Type": "Dragon",
        "Weak_to": ["Ice", "Dragon", "Fairy"],
        "Resists": ["Fire", "Water", "Electric", "Grass"],
        "Immunity": []
    },
    {
        "Type": "Dark",
        "Weak_to": ["Fighting", "Bug", "Fairy"],
        "Resists": ["Ghost", "Dark"],
        "Immunity": ["Psychic"]
    },
    {
        "Type": "Steel",
        "Weak_to": ["Fire", "Fighting", "Ground"],
        "Resists": ["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"],
        "Immunity": ["Poison"]
    },
    {
        "Type": "Fairy",
        "Weak_to": ["Poison", "Steel"],
        "Resists": ["Fighting", "Bug", "Dark"],
        "Immunity": ["Dragon"]
    }
]

# load sound effects
sound_hit = pygame.mixer.Sound("music/Hit_Normal_Damage.mpeg")
sound_super_hit = pygame.mixer.Sound("music/Hit_Super_Effective.mpeg")
sound_weak_hit = pygame.mixer.Sound("music/Hit_Not_Very_Effective.mpeg")

sound_hit.set_volume(.3)
sound_super_hit.set_volume(.3)
sound_weak_hit.set_volume(.3)


def get_sprite(id):
    path = "sprites/black-white/" + str(id) + ".png"
    image = pygame.image.load(path)
    return image

def get_back_sprite(id):
    path = "sprites/black-white/back/" + str(id) + ".png"
    image = pygame.image.load(path)
    return image


class Pokemon(pygame.sprite.Sprite):
    # a class to represent a Pokemon
    def __init__(self, id, level, x, y):
        # calling the sprite init method
        super().__init__()
        self.lvl = level
        self.name = data[id-1]['Name']
        self.types = data[id-1]['Types']
        self.hp = data[id-1]['HP'] + self.lvl
        self.current_hp = self.hp
        self.attack = data[id - 1]['Attack']
        self.defense = data[id - 1]['Defense']
        self.special_attack = data[id - 1]['Special Attack']
        self.special_defense = data[id - 1]['Special Defense']
        self.speed = data[id - 1]['Speed']
        self.pokedex_id = data[id-1]['ID']
        self.image = get_sprite(self.pokedex_id)
        self.back = get_back_sprite(self.pokedex_id)
        self.moves = []
        self.x = x
        self.y = y


    def print_stats(self):
        print(self.name, ", Types: ", self.types, ", HP: ", self.hp, ", Attack:", self.attack, ", Defense: ", self.defense, ", Special Attack: ", self.special_attack, ", Special Defense: ", self.special_defense, ", Speed:", self.speed)

    def set_moves(self):
        req = requests.get(f'{base_url}/pokemon/{self.name.lower()}')
        self.api_json = req.json()
        for i in range(len(self.api_json['moves'])):
            versions = self.api_json["moves"][i]["version_group_details"]
            for j in range(len(versions)):
                version = versions[j]
                if version["version_group"]["name"] != "black-white":
                    continue

                move = Move(self.api_json["moves"][i]["move"]["url"])
                if move.power is not None:
                    self.moves.append(move)
        if len(self.moves) > 4:
            self.moves = random.sample(self.moves, 4)

    def print_moves(self):
        for move in self.moves:
            print(move.name)
            #print(move.power)
            #print(type(move.power))

    def take_dmg(self, dmg):
        self.current_hp -= dmg
        if self.current_hp < 0:
            self.current_hp = 0

    def perform_attack(self, move, target):
        multiplier = 1
        for typing in target.types:
            for dictionary in typing_dict:
                if dictionary["Type"] == typing:
                    target_type = dictionary
                    print(target_type)
                    if move.type.capitalize() in target_type["Immunity"]:
                        multiplier = 0
                    elif move.type.capitalize() in target_type["Resists"]:
                        multiplier *= 0.5
                    elif move.type.capitalize() in target_type["Weak_to"]:
                        multiplier *= 2
        print(multiplier)
        dmg = (2 * self.lvl + 10) / 250 * self.attack / target.defense * move.power
        if move.type in self.types:
            dmg *= 1.5
        dmg = math.floor(multiplier * dmg)
        if multiplier > 1:
            text = "It's super effective!"
            sound_super_hit.play()
        elif multiplier == 0:
            text = "It doesn't affect "+target.name+"..."
        elif 1 > multiplier > 0:
            text = "It's not very effective..."
            sound_weak_hit.play()
        else:
            text = ""
            sound_hit.play()

        target.take_dmg(dmg)
        return text

    def draw_back(self, surface):
        image = pygame.transform.scale(self.back, (200, 200))
        surface.blit(image, (self.x, self.y))

    def draw_front(self, surface):
        image = pygame.transform.scale(self.image, (200, 200))
        surface.blit(image, (self.x, self.y))

    def display_info(self, surface, rect):
        font = pygame.font.SysFont("Aldrich", 35)
        info_text = font.render(self.name + "   lv. " + str(self.lvl), True, (0, 0, 0))
        info_text_rect = info_text.get_rect()
        info_text_rect.topleft = rect.topleft
        info_text_rect.x += 10
        info_text_rect.y += 10
        surface.blit(info_text, info_text_rect)
        # set up hp bars for pokemon
        max_hp = pygame.Rect(0, 0, 400, 20)
        max_hp.center = rect.center
        current_hp = pygame.Rect(max_hp.x, max_hp.y, (self.current_hp / self.hp) * 400, 20)
        pygame.draw.rect(surface, (255, 0, 0), max_hp)
        pygame.draw.rect(surface, (0, 255, 0), current_hp)
        hp_text = font.render(
            str(self.current_hp) + "/" + str(self.hp),
            True, (0, 0, 0))

        hp_text_rect = hp_text.get_rect()
        hp_text_rect.center = rect.center
        hp_text_rect.y += 25
        surface.blit(hp_text, hp_text_rect)











#p = Pokemon(1, 50, 0, 0)
#p.set_moves()
#p.print_moves()

#p.print_stats()
