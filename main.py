import random
import pygame
from itertools import cycle
import math
import sys
from Player import Player
from InfoDisplay import InfoDisplay
import ButtonList
from Pokemon import Pokemon
import time

# initialize pygame modules
pygame.init()

# creating a display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 707
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pokemon Arena")


def create_button(width, height, x, y, text):
    # position of the mouse cursor
    mouse_cursor = pygame.mouse.get_pos()

    button = pygame.Rect(x, y, width, height)

    # highlight the button if mouse is pointing to it
    if button.collidepoint(mouse_cursor):
        pygame.draw.rect(display_surface, (0, 255, 0), button)
        pygame.draw.rect(display_surface, (0, 0, 0), button, 3)
    else:
        pygame.draw.rect(display_surface, (0, 0, 0), button, 3)

    # add the label to the button
    font = pygame.font.SysFont("Aldrich", 35)
    text = font.render(f'{text}', True, (0, 0, 0))
    text_rect = text.get_rect(center=button.center)
    display_surface.blit(text, text_rect)
    return button


def display_message(message, rect):
    # draw a white box with black border
    pygame.draw.rect(display_surface, (255, 255, 255), rect)
    pygame.draw.rect(display_surface, (0, 0, 0), rect, 3)

    # display the message
    font = pygame.font.SysFont("Aldrich", 35)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = rect.center
    display_surface.blit(text, text_rect)

    pygame.display.update()

def select_player():

    # set FPS and clock
    FPS = 60
    clock = pygame.time.Clock()

    # load images
    text_image = pygame.image.load("images/boygirl.png"). convert_alpha()
    name_image = pygame.image.load("images/name_enter.png").convert_alpha()
    image_boy = pygame.image.load("images/boy1.png").convert_alpha()
    image_girl = pygame.image.load("images/girl1.png").convert_alpha()
    end_image = pygame.image.load("images/Is this you_.png").convert_alpha()
    yes_image = pygame.image.load("images/Yes.png").convert_alpha()
    no_image = pygame.image.load("images/No.png").convert_alpha()
    BG = pygame.image.load("images/lab.jpg").convert_alpha()

    # set up the user input
    font = pygame.font.SysFont("Aldrich", 50)
    user_input = ""
    input_rect = pygame.Rect(250, WINDOW_HEIGHT - 70, 700, 60)

    # set up boolean variables
    running = True
    boy = False
    girl = False
    name = False
    input_done = False
    yes = False
    no = False

    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if not name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        girl = False
                        boy = True
                    if event.key == pygame.K_RIGHT:
                        boy = False
                        girl = True
                    if event.key == pygame.K_RETURN and (boy or girl):
                        user_input = ""
                        name = True
            if name and not input_done:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        name = False
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        if len(user_input) < 15 and not event.key == pygame.K_RETURN:
                            user_input += event.unicode
                        if event.key == pygame.K_RETURN and len(user_input) > 0:
                            input_done = True
                        else:
                            pass
            if name and input_done:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        input_done = False
                    if event.key == pygame.K_UP:
                        no = False
                        yes = True
                    if event.key == pygame.K_DOWN:
                        yes = False
                        no = True
                    if event.key == pygame.K_RETURN and yes:
                        running = False
                    if event.key == pygame.K_RETURN and no:
                        no = False
                        yes = False
                        input_done = False


        # copy assets to the screen
        display_surface.blit(BG, (0, 0))
        pygame.draw.rect(display_surface, (105, 105, 105), [0, WINDOW_HEIGHT - 150, 1200, 150])
        pygame.draw.rect(display_surface, (70, 70, 70), [0, WINDOW_HEIGHT - 150, 1200, 150], 5)
        if not name and not input_done:
            if boy:
                pygame.draw.rect(display_surface, (70, 70, 70), [100, 0, 300, 557], 3)
            if girl:
                pygame.draw.rect(display_surface, (70, 70, 70), [WINDOW_WIDTH - 396, 0, 300, 557], 3)
            display_surface.blit(image_boy, (110, 4))
            display_surface.blit(image_girl, (WINDOW_WIDTH - 386, 4))
            display_surface.blit(text_image, (68, WINDOW_HEIGHT - 150))
        if name and not input_done:
            if boy:
                pygame.draw.rect(display_surface, (70, 70, 70), [100, 0, 300, 557], 3)
            if girl:
                pygame.draw.rect(display_surface, (70, 70, 70), [WINDOW_WIDTH - 396, 0, 300, 557], 3)
            display_surface.blit(image_boy, (110, 4))
            display_surface.blit(image_girl, (WINDOW_WIDTH - 386, 4))
            display_surface.blit(name_image, (250, WINDOW_HEIGHT - 150))
            pygame.draw.rect(display_surface, (70, 70, 70), input_rect)
            text_surface = font.render(user_input, True, (255, 255, 255))
            display_surface.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        if name and input_done:
            if boy:
                display_surface.blit(image_boy, (WINDOW_WIDTH//2 - image_boy.get_width()//2, 4))
            else:
                display_surface.blit(image_girl, (WINDOW_WIDTH//2 - image_girl.get_width()//2, 4))
            name_display = font.render(user_input, True, (255, 255, 255), (70, 70, 70))
            display_surface.blit(name_display, (WINDOW_WIDTH//2 + image_girl.get_width()//2, image_girl.get_height()//2))
            display_surface.blit(end_image, (WINDOW_WIDTH//2 - 260, WINDOW_HEIGHT - 150))
            display_surface.blit(yes_image, (WINDOW_WIDTH // 2 - image_girl.get_width()*2, 100))
            display_surface.blit(no_image, (WINDOW_WIDTH // 2 - image_girl.get_width() * 2 + 25, 220))
            if yes:
                pygame.draw.rect(display_surface, (70, 70, 70), [WINDOW_WIDTH // 2 - image_girl.get_width() * 2, 100, 200, 124], 3)
            if no:
                pygame.draw.rect(display_surface, (70, 70, 70), [WINDOW_WIDTH // 2 - image_girl.get_width() * 2, 224, 200, 124], 3)

        pygame.display.update()
        clock.tick(FPS)
    if boy:
        sex = "boy"
    else:
        sex = "girl"
    player = Player(sex, user_input)
    return player

def main_menu():

    # set FPS and clock
    FPS = 60
    clock = pygame.time.Clock()

    # load and play background music
    pygame.mixer.music.load("music/Gym.mp3")
    pygame.mixer.music.set_volume(.1)
    pygame.mixer.music.play(-1, 0.0)

    # load background image
    BG = pygame.image.load("images/tlo2.png").convert_alpha()

    # load logo image
    logo_image = pygame.image.load("images/logo.png")
    logo_rect = logo_image.get_rect()
    logo_rect.centerx = WINDOW_WIDTH//2
    logo_rect.bottom = WINDOW_HEIGHT//2 - 40

    # load starting text
    text_image = pygame.image.load("images/text.png")
    text_rect = text_image.get_rect()
    text_rect.centerx = WINDOW_WIDTH//2
    text_rect.bottom = WINDOW_HEIGHT//2 + 200

    # creating a blinking effect for the starting text
    BLINK_EVENT = pygame.USEREVENT + 0
    blank = pygame.Surface(text_rect.size, pygame.SRCALPHA, 32)
    blank = blank.convert_alpha()
    blink_surfaces = cycle([text_image, blank])
    blink_surface = next(blink_surfaces)
    pygame.time.set_timer(BLINK_EVENT, 1000)

    # set up scrolling background
    BG_WIDTH = BG.get_width()
    BG_RECT = BG.get_rect()
    scroll = 0
    tiles = math.ceil(WINDOW_WIDTH / BG_WIDTH) + 10

    # main loop
    running = True
    while running:

        # draw scrolling background
        for i in range(0, tiles):
            display_surface.blit(BG, (i * BG_WIDTH + scroll, 0))
            BG_RECT.x = i * BG_WIDTH + scroll

        # scroll background
        scroll -= 5

        # reset scroll
        if abs(scroll) > BG_WIDTH:
            scroll = 0
        # iterate through events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == BLINK_EVENT:
                blink_surface = next(blink_surfaces)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        # copy assets to the screen
        display_surface.blit(logo_image, logo_rect)
        display_surface.blit(blink_surface, text_rect)


        # update the display
        pygame.display.update()
        clock.tick(FPS)




def choose_pokemon():

    # set FPS and clock
    FPS = 60
    clock = pygame.time.Clock()

    # set caption
    pygame.display.set_caption("Choose your Pokemon!")

    # load background image
    BG = pygame.image.load("images/lab.jpg").convert_alpha()

    # set up pokemon array
    pokemon = []

    # button setup
    buttons = []
    for i in range(5):
        blist = ButtonList.ButtonList("Gen" + str(i+1), 20 + i * 240, 0)
        buttons.append(blist)

    # team display setup
    pokemon_display = InfoDisplay(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 175, 200, 175)
    team_display = []
    for i in range(3):
        p = pygame.Rect(0, 0, 100, 100)
        p.center = pokemon_display.info_rect.center
        p.x = pokemon_display.info_rect.x - (3 - i) * 100
        team_display.append(p)
    for i in range(3):
        p = pygame.Rect(0, 0, 100, 100)
        p.center = pokemon_display.info_rect.center
        p.x = pokemon_display.info_rect.x + (i + 2) * 100
        team_display.append(p)


    # main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    pos = pygame.mouse.get_pos()
                    if button.clicked:
                        if button.rect.collidepoint(pos):
                            # left mouse click (hide button list)
                            if event.button == 1:
                                button.clicked = False
                        elif button.rect.x <= pos[0] <= button.rect.x + button.rect.width:
                            # scroll down
                            if event.button == 5:
                                if button.first_to_draw + 6 < (button.last - button.first + 1):
                                    button.first_to_draw += 1
                                    button.how_many = 6
                                else:
                                    if button.first_to_draw + 6 > (button.last - button.first + 1):
                                        pass
                                    else:
                                        button.first_to_draw += 1
                                        button.how_many = (button.last - button.first + 1) - button.first_to_draw
                            # scroll up
                            if event.button == 4:
                                if button.first_to_draw - 1 >= 0:
                                    button.first_to_draw -= 1
                                    button.how_many = 6
                    else:
                        if button.rect.collidepoint(pos):
                            # left mouse click (show button list)
                            if event.button == 1:
                                button.clicked = True
            if event.type == pygame.KEYDOWN:
                # confirm selected team
                if event.key == pygame.K_RETURN and len(pokemon) > 0:
                    running = False
                # delete last selected pokemon
                if event.key == pygame.K_ESCAPE and len(pokemon) > 0:
                    pokemon.pop()
                    time.sleep(0.1)





        # blit background image
        display_surface.blit(BG, (0, 0))


        # draw current pokemon info display
        pygame.draw.rect(display_surface, (105, 105, 105), pokemon_display.info_rect)
        pygame.draw.rect(display_surface, (70, 70, 70), pokemon_display.info_rect, 3)

        # draw selected pokemon display windows
        for window in team_display:
            pygame.draw.rect(display_surface, (105, 105, 105), window)
            pygame.draw.rect(display_surface, (70, 70, 70), window, 3)

        # draw button lists
        for button in buttons:
            button.draw(display_surface, button.first_to_draw, button.how_many, pokemon_display)

        # check for clicked buttons in a button list
        if len(pokemon) < 6:
            for button in buttons:
                if button.clicked:
                    for i in range(button.how_many):
                        pos = pygame.mouse.get_pos()
                        b = button.buttons[button.first_to_draw + i]
                        if b.rect.collidepoint(pos):
                            if pygame.mouse.get_pressed()[0] == 1:
                                new_pokemon = Pokemon(b.pokemon.pokedex_id, 50, b.pokemon.x, b.pokemon.y)
                                pokemon.append(new_pokemon)
                                time.sleep(0.1)


        # display chosen pokemon
        if len(pokemon) > 0:
            for i in range(len(pokemon)):
                image = pokemon[i].image
                rect = image.get_rect()
                rect.center = team_display[i].center
                display_surface.blit(pokemon[i].image, rect)

        # update the display
        pygame.display.update()
        clock.tick(FPS)

    return pokemon


def team_setup(player, opponent):

    for pokemon in player.pokemon:
        print(pokemon.name + " loading...")
        pokemon.set_moves()
        print(pokemon.name + " done!")

    for pokemon in opponent.pokemon:
        print(pokemon.name + " loading...")
        pokemon.set_moves()
        print(pokemon.name + " done!")
        pokemon.print_moves()



def battle(player, opponent):
    '''
    for pokemon in player.pokemon:
        pokemon.print_moves()

    for pokemon in opponent.pokemon:
        pokemon.print_moves()
    '''
    # load arena image
    image = pygame.image.load("images/ARENA.png")

    # set caption
    pygame.display.set_caption("Battle!")

    # load background music
    pygame.mixer.music.load("music/Battle.mp3")
    pygame.mixer.music.set_volume(.1)
    pygame.mixer.music.play(-1, 0.0)

    # set up turn variable
    turn = "starting"

    # set the first pokemon in the array as starting pokemon for both players
    player_current_pokemon = player.pokemon[0]
    opponent_current_pokemon = opponent.pokemon[0]

    # set up player menu
    menu = pygame.Rect(0, WINDOW_HEIGHT - 150, WINDOW_WIDTH, 150)
    message_display = pygame.Rect(10, WINDOW_HEIGHT - 140, WINDOW_WIDTH//2 - 20, 130)
    option_display = pygame.Rect(WINDOW_WIDTH - 605, WINDOW_HEIGHT - 140, WINDOW_WIDTH // 2, 130)



    # set up current pokemon hp status
    player_rect = pygame.Rect(WINDOW_WIDTH - 570, WINDOW_HEIGHT - 290, WINDOW_WIDTH // 2 - 30, 130)
    opponent_rect = pygame.Rect(0, 90, WINDOW_WIDTH // 2 - 30, 130)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if turn == "player_move" and event.key == pygame.K_ESCAPE:
                    turn = "player_turn"
                if turn == "player_switch" and event.key == pygame.K_ESCAPE:
                    turn = "player_turn"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == "player_move":
                    pos = event.pos
                    for i in range(len(move_buttons)):
                        if move_buttons[i].collidepoint(pos):
                            move = player_current_pokemon.moves[i]
                            if player_current_pokemon.speed > opponent_current_pokemon.speed:
                                display_message(player_current_pokemon.name + " used " + move.name.upper(),
                                                    message_display)
                                time.sleep(2)
                                display_message(player_current_pokemon.perform_attack(move, opponent_current_pokemon), message_display)
                                time.sleep(2)
                                pygame.draw.rect(display_surface, (255, 255, 255), opponent_rect)
                                pygame.draw.rect(display_surface, (0, 0, 0), opponent_rect, 3)
                                opponent_current_pokemon.display_info(display_surface, opponent_rect)
                                pygame.display.update()
                                if opponent_current_pokemon.current_hp == 0:
                                    turn = "fainted"
                                else:
                                    opponent_move = random.choice(opponent_current_pokemon.moves)
                                    display_message(
                                        opponent_current_pokemon.name + " used " + opponent_move.name.upper(),
                                        message_display)
                                    time.sleep(2)
                                    display_message(opponent_current_pokemon.perform_attack(opponent_move, player_current_pokemon), message_display)
                                    time.sleep(2)
                                    pygame.draw.rect(display_surface, (255, 255, 255), player_rect)
                                    pygame.draw.rect(display_surface, (0, 0, 0), player_rect, 3)
                                    player_current_pokemon.display_info(display_surface, player_rect)
                                    pygame.display.update()
                                    if player_current_pokemon.current_hp == 0:
                                        turn = "fainted"
                                    else:
                                        turn = "player_turn"
                            else:
                                opponent_move = random.choice(opponent_current_pokemon.moves)
                                display_message(opponent_current_pokemon.name + " used " + opponent_move.name.upper(),
                                                message_display)
                                time.sleep(2)
                                display_message(opponent_current_pokemon.perform_attack(opponent_move, player_current_pokemon), message_display)
                                time.sleep(2)
                                pygame.draw.rect(display_surface, (255, 255, 255), player_rect)
                                pygame.draw.rect(display_surface, (0, 0, 0), player_rect, 3)
                                player_current_pokemon.display_info(display_surface, player_rect)
                                pygame.display.update()
                                if player_current_pokemon.current_hp == 0:
                                    turn = "fainted"
                                else:
                                    display_message(player_current_pokemon.name + " used " + move.name.upper(),
                                                    message_display)
                                    time.sleep(2)
                                    display_message(player_current_pokemon.perform_attack(move, opponent_current_pokemon), message_display)
                                    time.sleep(2)
                                    pygame.draw.rect(display_surface, (255, 255, 255), opponent_rect)
                                    pygame.draw.rect(display_surface, (0, 0, 0), opponent_rect, 3)
                                    opponent_current_pokemon.display_info(display_surface, opponent_rect)
                                    pygame.display.update()
                                    if opponent_current_pokemon.current_hp == 0:
                                        turn = "fainted"
                                    else:
                                        turn = "player_turn"


                if turn == "player_switch":
                    pos = event.pos
                    for i in range(len(switch_buttons)):
                        if switch_buttons[i].collidepoint(pos):
                            if player.pokemon[i] == player_current_pokemon:
                                display_message(player_current_pokemon.name+" is already in battle!", message_display)
                                time.sleep(2)
                            else:
                                player_current_pokemon = player.pokemon[i]
                                display_message("Go, " + player_current_pokemon.name + " !",
                                                message_display)
                                time.sleep(2)
                                display_surface.blit(image, (0, 0))
                                pygame.draw.rect(display_surface, (105, 105, 105), menu)
                                pygame.draw.rect(display_surface, (0, 0, 0), menu, 3)
                                pygame.draw.rect(display_surface, (255, 255, 255), message_display)
                                pygame.draw.rect(display_surface, (0, 0, 0), message_display, 3)
                                pygame.draw.rect(display_surface, (255, 255, 255), option_display)
                                pygame.draw.rect(display_surface, (0, 0, 0), option_display, 3)
                                pygame.draw.rect(display_surface, (255, 255, 255), player_rect)
                                pygame.draw.rect(display_surface, (0, 0, 0), player_rect, 3)
                                pygame.draw.rect(display_surface, (255, 255, 255), opponent_rect)
                                pygame.draw.rect(display_surface, (0, 0, 0), opponent_rect, 3)
                                pygame.draw.rect(display_surface, (255, 255, 255), player_rect)
                                pygame.draw.rect(display_surface, (0, 0, 0), player_rect, 3)
                                player_current_pokemon.draw_back(display_surface)
                                opponent_current_pokemon.draw_front(display_surface)
                                opponent_current_pokemon.display_info(display_surface, opponent_rect)
                                player_current_pokemon.display_info(display_surface, player_rect)
                                opponent_move = random.choice(opponent_current_pokemon.moves)
                                display_message(opponent_current_pokemon.name + " used " + opponent_move.name.upper(),
                                                message_display)
                                time.sleep(2)
                                display_message(opponent_current_pokemon.perform_attack(opponent_move, player_current_pokemon), message_display)
                                time.sleep(2)
                                pygame.draw.rect(display_surface, (255, 255, 255), player_rect)
                                pygame.draw.rect(display_surface, (0, 0, 0), player_rect, 3)
                                player_current_pokemon.display_info(display_surface, player_rect)
                                pygame.display.update()
                                if player_current_pokemon.current_hp == 0:
                                    turn = "fainted"
                                else:
                                    turn = "player_turn"

                if turn == "player_switch_fainted":
                    pos = event.pos
                    for i in range(len(switch_buttons)):
                        if switch_buttons[i].collidepoint(pos):
                            player_current_pokemon = player.pokemon[i]
                            display_message("Go, " + player_current_pokemon.name + " !",
                                                message_display)
                            time.sleep(2)
                            turn = "player_turn"
                if turn == "player_turn":
                    pos = event.pos
                    if fight_button.collidepoint(pos):
                        turn = "player_move"
                    if switch_button.collidepoint(pos):
                        turn = "player_switch"

        display_surface.blit(image, (0, 0))

        pygame.draw.rect(display_surface, (105, 105, 105), menu)
        pygame.draw.rect(display_surface, (0, 0, 0), menu, 3)
        pygame.draw.rect(display_surface, (255, 255, 255), message_display)
        pygame.draw.rect(display_surface, (0, 0, 0), message_display, 3)
        pygame.draw.rect(display_surface, (255, 255, 255), option_display)
        pygame.draw.rect(display_surface, (0, 0, 0), option_display, 3)
        pygame.draw.rect(display_surface, (255, 255, 255), player_rect)
        pygame.draw.rect(display_surface, (0, 0, 0), player_rect, 3)
        pygame.draw.rect(display_surface, (255, 255, 255), opponent_rect)
        pygame.draw.rect(display_surface, (0, 0, 0), opponent_rect, 3)

        if turn == "starting":
            opponent_current_pokemon.draw_front(display_surface)
            display_message(opponent.name + " sent out "+opponent_current_pokemon.name + "!", message_display)
            pygame.display.update()
            time.sleep(1)

            player_current_pokemon.draw_back(display_surface)
            display_message("Go, " + player_current_pokemon.name + "!", message_display)
            pygame.display.update()
            time.sleep(1)
            turn = "player_turn"

        if turn == "player_turn":
            player_current_pokemon.draw_back(display_surface)
            opponent_current_pokemon.draw_front(display_surface)

            fight_button = create_button(option_display.width//2, option_display.height, option_display.x, option_display.y, "Fight")
            switch_button = create_button(option_display.width // 2, option_display.height, option_display.x + option_display.width // 2,
                                         option_display.y, "Switch")

            # render pokemon information (name, lvl, hp bars)
            player_current_pokemon.display_info(display_surface, player_rect)
            opponent_current_pokemon.display_info(display_surface, opponent_rect)

            # render pre_move text
            display_message("What will you do?", message_display)

        if turn == "player_move":
            player_current_pokemon.draw_back(display_surface)
            opponent_current_pokemon.draw_front(display_surface)
            # render pokemon information (name, lvl, hp bars)
            player_current_pokemon.display_info(display_surface, player_rect)
            opponent_current_pokemon.display_info(display_surface, opponent_rect)
            move_buttons = []
            for i in range(len(player_current_pokemon.moves)):
                move = player_current_pokemon.moves[i]
                button = create_button(300, 65, option_display.x + (i % 2) * 300, option_display.y + (i//2) * 65, move.name.capitalize())
                move_buttons.append(button)
            for i in range(len(move_buttons)):
                pos = pygame.mouse.get_pos()
                if move_buttons[i].collidepoint(pos):
                    display_message("Type: "+player_current_pokemon.moves[i].type.capitalize() + "           Power: " + str(player_current_pokemon.moves[i].power), message_display)
            pygame.display.update()

        if turn == "player_switch" or turn == "player_switch_fainted":
            player_current_pokemon.draw_back(display_surface)
            opponent_current_pokemon.draw_front(display_surface)
            # render pokemon information (name, lvl, hp bars)
            player_current_pokemon.display_info(display_surface, player_rect)
            opponent_current_pokemon.display_info(display_surface, opponent_rect)
            switch_buttons = []
            for i in range(len(player.pokemon)):
                pokemon = player.pokemon[i]
                button = create_button(200, 65, option_display.x + (i % 3) * 200, option_display.y + ((i + 1) % 2) * 65, pokemon.name)
                switch_buttons.append(button)
            pygame.display.update()

        if turn == "fainted":
            if opponent_current_pokemon.current_hp == 0:
                player_current_pokemon.draw_back(display_surface)
                display_message(opponent_current_pokemon.name + " fainted!", message_display)
                time.sleep(4)
                pygame.display.update()
                opponent.pokemon.remove(opponent_current_pokemon)
                if len(opponent.pokemon) > 0:
                    opponent_current_pokemon = random.choice(opponent.pokemon)
                    display_message(opponent.name + " sent out " + opponent_current_pokemon.name + "!", message_display)
                    time.sleep(2)
                    turn = "player_turn"
                else:
                    turn = "game_over"
            else:
                opponent_current_pokemon.draw_front(display_surface)
                display_message(player_current_pokemon.name + " fainted!", message_display)
                time.sleep(4)
                pygame.display.update()
                player.pokemon.remove(player_current_pokemon)
                if len(player.pokemon) > 0:
                    turn = "player_switch_fainted"
                else:
                    turn = "game_over"
            pygame.display.update()

        if turn == "game_over":
            display_message("Game over!", message_display)
            time.sleep(4)
            running = False


main_menu()
player = select_player()
player.pokemon = choose_pokemon()

p2 = Player("girl", "Test")
for x in range(1):
    poke_id = random.randint(1, 649)
    p = Pokemon(poke_id, 50, WINDOW_WIDTH - 400, WINDOW_HEIGHT//2-200)
    p2.pokemon.append(p)


team_setup(player, p2)
battle(player, p2)


pygame.quit()


