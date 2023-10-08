import pygame
from pygame.locals import *
class Enemy():
    def __init__(self,x,y,speed,spawn_timer,spawn_interval):
        self.x = x
        self.y = y
        self.speed = speed
        self.e_img = pygame.image.load("City_Rumble/enemy.png")
        self.img = self.e_img
        self.flipped_img = pygame.transform.flip(self.img,True,False)
        self.rect = self.img.get_rect()
        self.spawn_timer = spawn_timer
        self.spawn_interval = spawn_interval
        self.direction = ""
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.active = False
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.direction = ""

    def update(self):
        if self.active:
            if self.direction == "right":
                self.x += self.speed
                self.rect.x = self.x
                if self.x > 1280:
                    self.active = False
            elif self.direction == "left":
                self.x -= self.speed
                self.rect.x = self.x
                if self.x < 0:
                    self.active = False

                

