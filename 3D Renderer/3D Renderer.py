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

points = [[-50, -50, 50],
          [-50, 50, 50],
          [50, 50, 50],
          [50, -50, 50],
          [-50, -50, -50],
          [-50, 50, -50],
          [50, 50, -50],
          [50, -50, -50]]
edges = [[0, 4],
         [0, 3],
         [0, 1],
         [1, 5],
         [1, 2],
         [2, 3],
         [2, 6],
         [4, 5],
         [4, 7],
         [5, 6],
         [6, 7],
         [3, 7]]
trns_vec = pygame.Vector3(0, 0, 0)
rota_vec = pygame.Vector3(0, 0, 0)
cam_speed = 4
turn_angle = 0.1

def draw_grid(pos, area, size):
    for x in range(pos[0], pos[0]+area[0], size):
        for y in range(pos[1], pos[1]+area[1], size):
            pygame.draw.rect(screen, PEACOCK, pygame.Rect(x, y, size, size), 1)

def draw_point(pos):
    pygame.draw.circle(screen, WHITE, [pos[0], pos[1]], 7)

def draw_edge(pos1, pos2):
    pygame.draw.line(screen, LBLUE, pos1, pos2, 7)

def translate(pos, trn):
    pos[0] += trn.x
    pos[1] += trn.y
    pos[2] += trn.z

def rotateAxisX(pos, angle):
    pos[1] = pos[1]*cos(angle) - pos[2]*sin(angle)
    pos[2] = pos[1]*sin(angle) + pos[2]*cos(angle)

def rotateAxisY(pos, angle):
    pos[0] = pos[2]*sin(angle) + pos[0]*cos(angle)
    pos[2] = pos[2]*cos(angle) - pos[0]*sin(angle)

def rotateAxisZ(pos, angle):
    pos[0] = pos[0]*cos(angle) - pos[1]*sin(angle)
    pos[1] = pos[0]*sin(angle) + pos[1]*cos(angle)

def rotate(pos, rota):
    rotateAxisX(pos, rota.x)
    rotateAxisY(pos, rota.y)
    rotateAxisZ(pos, rota.z)

def project(pos, lines):
    pos_prj = []
    for i in pos:
        x_prj = i[0]
        y_prj = i[1]
        x_prj += w/2
        y_prj += h/2
        draw_point([x_prj, y_prj])
        pos_prj.append([x_prj, y_prj])
    for i in lines:
        draw_edge(pos_prj[i[0]], pos_prj[i[1]])

while run: #Game loop
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_t]:
        rota_vec.x = turn_angle
    elif keys[pygame.K_g]:
        rota_vec.x = -turn_angle
    else:
        rota_vec.x = 0
    if keys[pygame.K_y]:
        rota_vec.y = turn_angle
    elif keys[pygame.K_h]:
        rota_vec.y = -turn_angle
    else:
        rota_vec.y = 0
    if keys[pygame.K_u]:
        rota_vec.z = turn_angle
    elif keys[pygame.K_j]:
        rota_vec.z = -turn_angle
    else:
        rota_vec.z = 0

    if keys[pygame.K_s]:
        trns_vec.y = cam_speed
    elif keys[pygame.K_w]:
        trns_vec.y = -cam_speed
    else:
        trns_vec.y = 0
    if keys[pygame.K_d]:
        trns_vec.x = cam_speed
    elif keys[pygame.K_a]:
        trns_vec.x = -cam_speed
    else:
        trns_vec.x = 0

    screen.fill(DDBLUE)
    draw_grid([0, 0], size, 50)

    for i in points:
        translate(i, trns_vec)
        rotate(i, rota_vec)
    project(points, edges)

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()
