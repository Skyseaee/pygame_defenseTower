import pygame
import os
from . import enemy

imgs = []
for x in range(9):
    add_str = x
    imgs.append(pygame.image.load(r'../enemys/ghost/sprite_' + str(add_str) + '.png'))

class Scorpion(enemy.Enemy):

    def __init__(self):
        super().__init__()
        self.name = 'scorpion'
        self.money = 100
        self.max_health = 3
        self.health = self.max_health
        self.imgs = imgs[:]