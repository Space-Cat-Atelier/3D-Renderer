import pygame
from math import*

class Camera():
    def __init__(self, x, y, z, fov):
        self.pos = [x, y, z]
        self.rota = [0, 0, 0]
        self.angle = [0, 0, 0]
        self.fov = fov

    def move(self, trn):
        vec = pygame.Vector3(trn)
        vec = vec.rotate_x(-degrees(self.rota[0]))
        vec = vec.rotate_y(-degrees(self.rota[1]))
        vec = vec.rotate_z(degrees(self.rota[2]))
        self.pos[0] += vec.x
        self.pos[1] += vec.y
        self.pos[2] += vec.z

    def pitch(self, angle):
        self.rota[0] += angle

    def yaw(self, angle):
        self.rota[1] += angle

    def roll(self, angle):
        self.rota[2] += angle

    def rotate(self, rotate):
        self.pitch(rotate[0])
        self.yaw(rotate[1])
        self.roll(rotate[2])
