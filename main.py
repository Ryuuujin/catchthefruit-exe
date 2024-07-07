import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import time
import random

# Initialize pygame
pygame.init()
pygame.font.init()  # Initialize the font module
pygame.mixer.init()  # Initialize the mixer module

# Check if font module is initialized
if not pygame.font.get_init():
    print("Font module not initialized.")
else:
    print("Font module initialized successfully.")

# COLORS
black = (0, 0, 0)
white = (255, 255, 255)
dark_blue = (0, 0, 200)
dark_red = (200, 0, 0)
dark_green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

# DISPLAY
display_width = 500
display_height = 800
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Catch The Fruit")

# IMAGES
basket_img = pygame.image.load('assets/img/basket.png')
basket_img = pygame.transform.scale(basket_img, (150, 100))
bg = pygame.image.load('assets/img/bgbaru-2.jpg')
bomb_img = pygame.image.load('assets/img/bomb.png')
bomb_img = pygame.transform.scale(bomb_img, (100, 100))
fruit_img_1 = pygame.image.load('assets/img/anggur.png')
fruit_img_1 = pygame.transform.scale(fruit_img_1, (100, 100))
fruit_img_2 = pygame.image.load('assets/img/strawberry.png')
fruit_img_2 = pygame.transform.scale(fruit_img_2, (100, 100))

# Button images
start_img = pygame.image.load('assets/img/start.png')
help_img = pygame.image.load('assets/img/help.png')
quit_img = pygame.image.load('assets/img/quit.png')
restart_img = pygame.image.load('assets/img/restart.png')

# Load sounds
pygame.mixer.music.load('assets/sfx/backsound.mp3')
pygame.mixer.music.set_volume(0.5)
catch_sound = pygame.mixer.Sound('assets/sfx/correct.wav')
bomb_sound = pygame.mixer.Sound('assets/sfx/explosion.wav')
game_over_sound = pygame.mixer.Sound('assets/sfx/gameover.wav')

clock = pygame.time.Clock()

# High Score Functions
def read_high_score():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
def write_high_score(score):
    with open('highscore.txt', 'w') as file:
        file.write(str(score))

high_score = read_high_score()

class Basket(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.hitbox = (self.x, self.y + 20, 150, 80)
    def draw(self, window):
        window.blit(basket_img, (self.x, self.y))
        self.hitbox = (self.x, self.y + 20, 200, 80)
    
class Fruits(object):
    def __init__(self, x, y, f_type):
        self.x = x
        self.y = y
        self.f_type = f_type
        self.vel = 10
        self.hitbox = (self.x, self.y, 100, 100)
    def draw(self, window):
        if self.f_type == 0:
            fruit = fruit_img_1
        else:
            fruit = fruit_img_2
        window.blit(fruit, (self.x, self.y))
        self.hitbox = (self.x, self.y, 100, 100)

class Bombs(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.hitbox = (self.x, self.y, 100, 100)
    def draw(self, window):
        window.blit(bomb_img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 100, 100)
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, x, y, size):
    try:
        regText = pygame.font.Font("freesansbold.ttf", size)
    except FileNotFoundError:
        print("Font file not found.")
        pygame.quit()
        quit()
    textSurf, textRect = text_objects(msg, regText)
    textRect.center = (x, y)
    window.blit(textSurf, textRect)

def button(image, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    window.blit(image, (x, y))
    if (x+width > mouse[0] > x and y+height > mouse[1] > y):
        if (click[0] == 1 and action != None):
            if (action == "play"):
                main(player_name)
            elif (action == "quit"):
                pygame.quit()
                quit()
            elif (action == "instructions"):
                help_page()
            elif (action == "back"):
                game_intro()
            elif (action == "restart"):
                main(player_name)

def help_page():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        window.fill(white) #help page background here
        message_to_screen("CARA BERMAIN", 250, 200, 50)
        message_to_screen("Gunakan tombol panah kiri dan kanan untuk memindahkan keranjang.", 250, 270, 20)
        message_to_screen("Tangkap buah sebanyak yang Anda bisa,", 250, 300, 20)
        message_to_screen("tapi hindari bom!", 250, 330, 20)
        message_to_screen("Every time a fruit enters the basket, 1 points is added:", 250, 390, 20)
        button(help_img, 100, 600, 75, 50, "back")
        pygame.display.update()
        clock.tick(15)
        
def game_intro():
    pygame.mixer.music.play(-1)  # Play background music on loop
    intro = True
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    global player_name
    player_name = ''
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    active = not active
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name = text
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        window.blit(bg, (0,0))
        message_to_screen("FRUIT CATCHER", display_width/2, display_height/2, 50)
        button(start_img, 100, 450, 75, 50, "play")
        button(quit_img, 300, 450, 75, 50, "quit")
        button(help_img, 200, 450, 75, 50, "instructions")
        
        # Render the current text.
        txt_surface = pygame.font.Font(None, 32).render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        pygame.display.update()
        clock.tick(15)

def game_over(score):
    global high_score
    pygame.mixer.music.stop()  # Stop background music
    game_over_sound.play()  # Play game over sound
    if score > high_score:
        high_score = score
        write_high_score(high_score)
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        window.fill(white) #game over background here
        message_to_screen("GAME OVER", 250, 200, 50)
        message_to_screen("Your Score: " + str(score), 250, 300, 30)
        message_to_screen("High Score: " + str(high_score), 250, 350, 30)
        button(restart_img, 100, 450, 75, 50, "restart")
        button(quit_img, 300, 450, 75, 50, "quit")
        pygame.display.update()
        clock.tick(15)
    
def main(player_name):
    score = 0
    fruits = []
    bombs = []
    fruit_add_counter = 0
    bomb_add_counter = 0
    add_fruit_rate = 30
    add_bomb_rate = 100
    basket = Basket(display_width * 0.35, display_height - 160)
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False      
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket.x > basket.vel - 5:
            basket.x -= basket.vel
        elif keys[pygame.K_RIGHT] and basket.x < 500 - 150 - basket.vel:
            basket.x += basket.vel  
        window.blit(bg, (0,0))
        fruit_add_counter += 1
        bomb_add_counter += 1
        if fruit_add_counter == add_fruit_rate:
            fruit_add_counter = 0
            f_startx = random.randrange(100, display_width - 100)
            f_starty = 0
            f_type = random.choice([0, 1])
            new_fruit = Fruits(f_startx, f_starty, f_type)
            fruits.append(new_fruit)
        if bomb_add_counter == add_bomb_rate:
            bomb_add_counter = 0
            b_startx = random.randrange(100, display_width - 100)
            b_starty = 0
            new_bomb = Bombs(b_startx, b_starty)
            bombs.append(new_bomb)
        for item in fruits:
            item.draw(window)
            item.y += item.vel
        for item in fruits[:]:
            if (item.hitbox[0] >= basket.hitbox[0] - 20) and (item.hitbox[0] <= basket.hitbox[0] + 70):
                if basket.hitbox[1] - 120 <= item.hitbox[1] <= basket.hitbox[1] - 40:
                    fruits.remove(item)
                    score += 1
                    catch_sound.play()  # Play catch sound
                    print("Score:", score)
        for item in bombs:
            item.draw(window)
            item.y += item.vel
        for item in bombs[:]:
            if (item.hitbox[0] >= basket.hitbox[0]) and (item.hitbox[0] <= basket.hitbox[0] + 50):
                if basket.hitbox[1] - 120 <= item.hitbox[1] <= basket.hitbox[1] - 40:
                    play = False
                    bomb_sound.play()  # Play bomb sound
        message_to_screen("Score: "+str(score), 50, 30, 20)
        basket.draw(window)
        pygame.display.update()
        clock.tick(60)
    game_over(score)
    pygame.quit()

game_intro()
main(player_name)
