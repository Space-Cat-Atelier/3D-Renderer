import pygame #Modules
import os
import sys
from math import*

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Color Constants
PEACOCK = (3, 37, 45)
DDBLUE = (0, 22, 22)
LBLUE = (26, 170, 228)
BLACK = (0, 0, 0)
WHITE = (235, 235, 235)

pygame.init() #Initaization and clock and game loop condition
clock = pygame.time.Clock()
run = True

#Screen
size = (800, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('3D Renderer')
h = screen.get_height()
w = screen.get_width()

points = [[0, 0, 50],
          [0, 100, 50],
          [100, 100, 50],
          [100, 0, 50],
          [0, 0, -50],
          [0, 100, -50],
          [100, 100, -50],
          [100, 0, -50]]

def draw_grid(pos, area, size):
    for x in range(pos[0], pos[0]+area[0], size):
        for y in range(pos[1], pos[1]+area[1], size):
            pygame.draw.rect(screen, PEACOCK, pygame.Rect(x, y, size, size), 1)

def projection(pos, fcl):
    for i in pos:
        try:
            i[0] *= fcl/i[2]
            i[1] *= fcl/i[2]
        except:
            pass
        i[2] = 0

def draw(pos):
    for i in pos:
        pygame.draw.circle(screen, BLACK, [i[0], i[1]], 10)
        pygame.draw.circle(screen, WHITE, [i[0], i[1]], 7)

def translate(pos, trn):
    for i in pos:
        i[0] += trn[0]
        i[1] += trn[1]
        i[2] += trn[2]

translate(points, [100, 100, 0])
projection(points, 100)

while run: #Game loop
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_UP]:
        translate(points, [0, -5, 0])
    elif keys[pygame.K_DOWN]:
        translate(points, [0, 5, 0])
    if keys[pygame.K_LEFT]:
        translate(points, [-5, 0, 0])
    elif keys[pygame.K_RIGHT]:
        translate(points, [5, 0, 0])

    screen.fill(DDBLUE)
    draw_grid([0, 0], size, 50)

    draw(points)

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()
