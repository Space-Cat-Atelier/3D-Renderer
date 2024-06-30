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
focal_length = 100
cam_speed = 4
turn_angle = 0.001

def draw_grid(pos, area, size):
    for x in range(pos[0], pos[0]+area[0], size):
        for y in range(pos[1], pos[1]+area[1], size):
            pygame.draw.rect(screen, PEACOCK, pygame.Rect(x, y, size, size), 1)

def draw_point(pos):
    pygame.draw.circle(screen, BLACK, [pos[0], pos[1]], 10)
    pygame.draw.circle(screen, WHITE, [pos[0], pos[1]], 7)

def draw_edge(pos1, pos2):
    pygame.draw.line(screen, BLACK, pos1, pos2, width=10)
    pygame.draw.line(screen, LBLUE, pos1, pos2, width=7)

def project(pos, lines, fcl):
    pos_prj = []
    for i in pos:
        try:
            x_prj = (i[0]*fcl)/(i[2]+fcl)+w/2
            y_prj = (i[1]*fcl)/(i[2]+fcl)+h/2
            draw_point([x_prj, y_prj])
            pos_prj.append([x_prj, y_prj])
        except:
            pos_prj.append([i[0], i[1]])
    for i in lines:
        draw_edge(pos_prj[i[0]], pos_prj[i[1]])

def translate(pos, trn):
    for i in pos:
        i[0] += trn[0]
        i[1] += trn[1]
        i[2] += trn[2]

def rotateX(pos, angle):
    for i in pos:
        i[1] = i[1]*cos(degrees(angle)) - i[2]*sin(degrees(angle))
        i[2] = i[1]*sin(degrees(angle)) + i[2]*cos(degrees(angle))

def rotateY(pos, angle):
    for i in pos:
        i[0] = i[2]*sin(degrees(angle)) + i[0]*cos(degrees(angle))
        i[2] = i[2]*cos(degrees(angle)) - i[0]*sin(degrees(angle))

def rotateZ(pos, angle):
    for i in pos:
        i[0] = i[0]*cos(degrees(angle)) - i[1]*sin(degrees(angle))
        i[1] = i[0]*sin(degrees(angle)) + i[1]*cos(degrees(angle))

while run: #Game loop
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_t]:
        rotateX(points, turn_angle)
    elif keys[pygame.K_g]:
        rotateX(points, -turn_angle)
    if keys[pygame.K_y]:
        rotateY(points, turn_angle)
    elif keys[pygame.K_h]:
        rotateY(points, -turn_angle)
    if keys[pygame.K_u]:
        rotateZ(points, turn_angle)
    elif keys[pygame.K_j]:
        rotateZ(points, -turn_angle)

    if keys[pygame.K_s]:
        translate(points, [0, -cam_speed, 0])
    elif keys[pygame.K_w]:
        translate(points, [0, cam_speed, 0])
    if keys[pygame.K_d]:
        translate(points, [-cam_speed, 0, 0])
    elif keys[pygame.K_a]:
        translate(points, [cam_speed, 0, 0])

    if keys[pygame.K_o]:
        focal_length += cam_speed/2
    elif keys[pygame.K_i]:
        focal_length -= cam_speed/2

    screen.fill(DDBLUE)
    draw_grid([0, 0], size, 50)

    project(points, edges, focal_length)

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()
