import pygame
from math import*

LINE = (255, 128, 0)
NODE = (235, 235, 235)

screen = None
h = 0
w = 0

def get_screen(scrn):
    global screen, h, w
    screen = scrn
    h = screen.get_height()
    w = screen.get_width()

def change_color(line, node):
    global LINE, NODE
    LINE = line
    NODE = node

def get_obj(path):
    nodes = []
    edges = []
    file = open(path, 'r')
    for line in file:
        if line.startswith('v '):
            nodes.append([float(i) for i in line.split()[1:]] + [1])
        elif line.startswith('f'):
            lines = line.split()[1:]
            edges.append([int(line.split('/')[0]) - 1 for line in lines])
    return Object(nodes, edges)

class Object():
    def __init__(self, nodes, edges):
        self.points = nodes
        self.lines = edges

    def draw_point(self, pos):
        pygame.draw.circle(screen, NODE, [pos[0], pos[1]], 7)

    def draw_edge(self, pos1, pos2): 
        pygame.draw.line(screen, LINE, pos1, pos2, 7)

    def pitch(self, pos, angle):
        y = pos[1]
        z = pos[2]
        pos[1] = y*cos(angle) - z*sin(angle)
        pos[2] = y*sin(angle) + z*cos(angle)

    def yaw(self, pos, angle):
        x = pos[0]
        z = pos[2]
        pos[0] = x*cos(angle) + z*sin(angle)
        pos[2] = z*cos(angle) - x*sin(angle)

    def roll(self, pos, angle):
        x = pos[0]
        y = pos[1]
        pos[0] = x*cos(angle) - y*sin(angle)
        pos[1] = x*sin(angle) + y*cos(angle)

    def rotate(self, rota):
        for i in self.points:
            self.pitch(i, rota[0])
            self.yaw(i, rota[1])
            self.roll(i, rota[2])

    def project(self, camera, draw):
        pos_prj = []
        rot_points = []
        for i in self.points:
            point = i.copy()
            point[0] -= camera.pos[0]
            point[1] -= camera.pos[1]
            point[2] -= camera.pos[2]
            self.pitch(point, camera.rota[0])
            self.yaw(point, camera.rota[1])
            self.roll(point, camera.rota[2])
            point[0] += camera.pos[0]
            point[1] += camera.pos[1]
            point[2] += camera.pos[2]
            rot_points.append(point)

        for i in rot_points:
            x = i[0] - camera.pos[0]
            y = i[1] - camera.pos[1]
            z = i[2] - camera.pos[2]
            if z > 0:
                try:
                    x_prj = (x*camera.fov)/z+w/2
                    y_prj = (y*camera.fov)/z+h/2
                except:
                    x_prj = x
                    y_prj = y
                if draw[0]:
                    self.draw_point([x_prj , y_prj])
                pos_prj.append([x_prj, y_prj])
            else:
                pos_prj.append(None)
        if draw[1]:
            for i in self.lines:
                if pos_prj[i[0]] and pos_prj[i[1]]:
                    self.draw_edge(pos_prj[i[0]], pos_prj[i[1]])

class Cuboid(Object):
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
