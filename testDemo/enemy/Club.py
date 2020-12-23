import pygame
from . import enemy

imgs = []
for x in range(7):
    # add_str = x
    imgs.append(pygame.image.load(r'../enemies/tencent/render000' + str(x) + '.png'))

class Club(enemy.Enemy):
    def __init__(self, money, health):
        super().__init__()
        self.name = 'Club'
        self.money = money
        self.max_health = health
        self.health = self.max_health

        self.imgs = imgs[:]