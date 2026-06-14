import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60 

WIDTH = 864
HEIGHT = 936
CENTRE_X = 432
CENTRE_Y = 468

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

font = pygame.font.SysFont("Times New Roman", 60)

# Game variables 
ground_scroll = 0    
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# Load images
bg = pygame.image.load("images / bg.png")
ground = pygame.image.load("images / ground.png")
button = pygame.image.load("images / restart.png")

def draw_text(text, font, clr, x, y):
    txt = font.render(text, True, clr)
    screen.blit(txt, (x, y))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1, 4):
            img = pygame.image.load(f"images/bird{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.centre = [x, y]
        self.clicked = False
        self.vel = 0

    def update(self):
        if flying == True:
            # Apply gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            # Animating the bird
            flap_cooldown = 5
            self.counter += 1
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index > len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
            # Rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            # Ground landing 
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/pipe.png") 
        self.rect = self.image.get_rect()
        if pos == 1:             
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap // 2]
        elif pos == -1:
            self.rect.topleft = [x, y + pipe_gap // 2]
        
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True


        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, CENTRE_Y)
bird_group.add(flappy)

restart_button = Button(CENTRE_X - 50, CENTRE_Y - 100, button)

run = True
while run:
    clock.tick(FPS)
    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)

    bird_group.update()
    # Draw the ground and make it move
    screen.blit(ground, (ground_scroll, 768))

    if len(pipe_group) > 0:
        if (bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left) and (bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right) and pass_pipe == False:
            pass_pipe = True
        
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                pass_pipe = False
                score += 1
            
    draw_text(str(score), font, "grey", CENTRE_X, 35)

    # Check for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        flying = False

    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and game_over == True:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            height = random.randint(-100, 100)
            top_pipe = Pipe(WIDTH, ())