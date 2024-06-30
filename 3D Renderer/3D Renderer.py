import pygame #Modules
import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Color Constants
PEACOCK = (3, 37, 45)
BLACK = (0, 22, 22)
LBLUE = (26, 170, 228)

pygame.init() #Initaization and clock and game loop condition
clock = pygame.time.Clock()
run = True

#Screen
size = (800, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('3D Renderer')
h = screen.get_height()
w = screen.get_width()

positions = [[],
             [],
             [],
             [],
             [],
             [],
             [],
             []]

def draw_grid(pos, area, size):
    for x in range(pos[0], pos[0]+area[0], size):
        for y in range(pos[1], pos[1]+area[1], size):
            pygame.draw.rect(screen, PEACOCK, pygame.Rect(x, y, size, size), 1)

while run: #Game loop
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(BLACK)
    draw_grid([0, 0], size, 50)

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()
