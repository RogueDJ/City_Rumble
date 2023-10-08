import pygame
class Player:
    def __init__(self,x,y):
        self.p_image = pygame.image.load("City_Rumble/player.png")
        self.player_image = self.p_image
        self.slide_left = pygame.image.load("City_Rumble/slide_left.png")
        self.slide_right = pygame.image.load("City_Rumble/slide_right.png")
        self.right_kick = pygame.image.load("City_Rumble/kickingright.png")
        self.left_kick =  pygame.image.load("City_Rumble/kickingleft.png")
        self.lives = 3
        self.x = x
        self.y = y
        self.moving_right = False
        self.moving_left = False
        self.speed = 4
        self.jump_count = 10
        self.jumping = False
        self.sliding = False
        self.slide_count = 5
        self.direction = "right"
        self.kick_count = 2
        self.kicking = False
        self.rect = pygame.Rect(x,y,self.player_image.get_width(),self.player_image.get_height())
    def change_direction(self):
        if self.moving_right == True:
            self.direction = "right"
        elif self.moving_left == True:
            self.direction = "left"
            