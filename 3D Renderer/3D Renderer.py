import pygame #Modules
import os
import sys
from math import*
from DATA.camera import*
from DATA.objects import*

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Color Constants
PEACOCK = (3, 37, 45)
DDBLUE = (0, 22, 22)
BLACK = (0, 0, 0)

pygame.init() #Initaization and clock and game loop condition
clock = pygame.time.Clock()
run = True

#Screen
size = (1000, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('3D Renderer')
h = screen.get_height()
w = screen.get_width()

def draw_grid(pos, area, size):
    for x in range(pos[0], pos[0]+area[0], size):
        for y in range(pos[1], pos[1]+area[1], size):
            pygame.draw.rect(screen, PEACOCK, pygame.Rect(x, y, size, size), 1)

cam_speed = 0.1
turn_speed = 0.05

get_screen(screen)
shapes = [get_obj('Object Files\\apple_obj.obj')]
shapes[0].rotate([0, 0, radians(180)])

cam = Camera(0, 0, -10, w/2)

while run: #Game loop
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_d]:
        cam.move([cam_speed, 0, 0])
    elif keys[pygame.K_a]:
        cam.move([-cam_speed, 0, 0])
    if keys[pygame.K_w]:
        cam.move([0, -cam_speed, 0])
    elif keys[pygame.K_s]:
        cam.move([0, cam_speed, 0])

    if keys[pygame.K_UP]:
        cam.move([0, 0, cam_speed])
    elif keys[pygame.K_DOWN]:
        cam.move([0, 0, -cam_speed])

    if keys[pygame.K_LEFT]:
        cam.yaw(turn_speed)
    elif keys[pygame.K_RIGHT]:
        cam.yaw(-turn_speed)

    screen.fill(DDBLUE)
    draw_grid([0, 0], size, 50)

    for shape in shapes:
        shape.project(cam, [False, True])

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()
