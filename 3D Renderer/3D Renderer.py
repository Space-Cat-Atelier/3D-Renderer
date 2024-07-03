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


trns_vec = pygame.Vector3(0, 0, 0)
rota_vec = pygame.Vector3(0, 0, 0)
cam_speed = 4
turn_angle = 0.1
focal_length = 100

def draw_grid(pos, area, size):
    for x in range(pos[0], pos[0]+area[0], size):
        for y in range(pos[1], pos[1]+area[1], size):
            pygame.draw.rect(screen, PEACOCK, pygame.Rect(x, y, size, size), 1)

class Cuboid():
    def __init__(self, x, y, z, w, h, d):
        self.points = [[x,   y,   z  ],
                       [x,   y,   z+d],
                       [x,   y+h, z  ],
                       [x,   y+h, z+d],
                       [x+w, y,   z  ],
                       [x+w, y,   z+d],
                       [x+w, y+h, z  ],
                       [x+w, y+h, z+d]]
        self.lines = [[0, 1],
                      [1, 3],
                      [3, 2],
                      [2, 0],
                      [4, 5],
                      [5, 7],
                      [7, 6],
                      [6, 4],
                      [0, 4],
                      [1, 5],
                      [2, 6],
                      [3, 7]]

    def draw_point(self, pos):
        pygame.draw.circle(screen, WHITE, [pos[0], pos[1]], 7)

    def draw_edge(self, pos1, pos2):
        pygame.draw.line(screen, LBLUE, pos1, pos2, 7)

    def translate(self, trn):
        for pos in self.points:
            pos[0] += trn.x
            pos[1] += trn.y
            pos[2] += trn.z

    def pitch(self, pos, angle):
        y = pos[1]
        z = pos[2]
        pos[1] = y*cos(angle) - z*sin(angle)
        pos[2] = y*sin(angle) + z*cos(angle)

    def yaw(self, pos, angle):
        x = pos[0]
        z = pos[2]
        pos[0] = z*sin(angle) + x*cos(angle)
        pos[2] = z*cos(angle) - x*sin(angle)

    def roll(self, pos, angle):
        x = pos[0]
        y = pos[1]
        pos[0] = x*cos(angle) - y*sin(angle)
        pos[1] = x*sin(angle) + y*cos(angle)

    def rotate(self, rota):
        for pos in self.points:
            self.pitch(pos, rota.x)
            self.yaw(pos, rota.y)
            self.roll(pos, rota.z)

    def project(self, fcl):
        pos_prj = []
        for i in self.points:
            x = i[0]
            y = i[1]
            z = i[2]
            try:
                x_prj = (x)+w/2
                y_prj = (y)+h/2
            except:
                x_prj = x
                y_prj = y
            self.draw_point([x_prj, y_prj])
            pos_prj.append([x_prj, y_prj])
        for i in self.lines:
            self.draw_edge(pos_prj[i[0]], pos_prj[i[1]])

cube = Cuboid(0, 0, 100, 100, 100, 100)

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
        trns_vec.y = -cam_speed
    elif keys[pygame.K_w]:
        trns_vec.y = cam_speed
    else:
        trns_vec.y = 0
    if keys[pygame.K_d]:
        trns_vec.x = -cam_speed
    elif keys[pygame.K_a]:
        trns_vec.x = cam_speed
    else:
        trns_vec.x = 0

    if keys[pygame.K_i]:
        focal_length += cam_speed/2
    elif keys[pygame.K_o]:
        focal_length -= cam_speed/2

    screen.fill(DDBLUE)
    draw_grid([0, 0], size, 50)

    cube.translate(trns_vec)
    cube.rotate(rota_vec)
    cube.project(focal_length)

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()
