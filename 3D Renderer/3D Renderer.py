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

def draw_grid(pos, area, size):
    for x in range(pos[0], pos[0]+area[0], size):
        for y in range(pos[1], pos[1]+area[1], size):
            pygame.draw.rect(screen, PEACOCK, pygame.Rect(x, y, size, size), 1)

cam_speed = 5

class Camera():
    def __init__(self, x, y, z, z_offset, fov):
        self.pos = [x, y, z]
        self.fov = fov
        self.z_offset = z_offset

    def move(self, vec):
        self.pos[0] += vec[0]
        self.pos[1] += vec[1]
        self.pos[2] += vec[2]

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

    def project(self, camera):
        pos_prj = []
        for i in self.points:
            x = i[0] - camera.pos[0]
            y = i[1] - camera.pos[1]
            z = i[2] - camera.pos[2]
            if z + camera.z_offset > 0:
                try:
                    x_prj = (x*camera.fov)/(z+camera.z_offset)+w/2
                    y_prj = (y*camera.fov)/(z+camera.z_offset)+h/2
                except:
                    x_prj = x
                    y_prj = y
                self.draw_point([x_prj , y_prj])
                pos_prj.append([x_prj, y_prj])
            else:
                pos_prj.append(None)
        for i in self.lines:
            if pos_prj[i[0]] and pos_prj[i[1]]:
                self.draw_edge(pos_prj[i[0]], pos_prj[i[1]])

cube = Cuboid(-50, -50, -50, 25, 100, 300)
cube2 = Cuboid(-50, -50, 225, 350, 100, 25)
cube3 = Cuboid(275, -50, -50, 25, 100, 300)
shapes = [cube, cube2, cube3]

cam = Camera(0, 0, 0, 200, w/2)

while run: #Game loop
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_s]:
        cam.move([0, cam_speed, 0])
    elif keys[pygame.K_w]:
        cam.move([0, -cam_speed, 0])
    if keys[pygame.K_d]:
        cam.move([cam_speed, 0, 0])
    elif keys[pygame.K_a]:
        cam.move([-cam_speed, 0, 0])
    if keys[pygame.K_UP]:
        cam.move([0, 0, cam_speed])
    elif keys[pygame.K_DOWN]:
        cam.move([0, 0, -cam_speed])

    screen.fill(DDBLUE)
    draw_grid([0, 0], size, 50)

    for shape in shapes:
        shape.project(cam)

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()
