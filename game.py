import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60 

WIDTH = 864
HEIGHT = 936

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