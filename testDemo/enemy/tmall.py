import pygame
from . import enemy

imgs = []
for x in range(7):
    add_str = x
    imgs.append(pygame.transform.scale(pygame.image.load(r'../enemies/tmall/render000' + str(add_str) + '.png'), (1920//4, 1080//4)))

class TMall(enemy.Enemy):

    def __init__(self, money, health):
        super().__init__()
        self.name = 'mall'
        self.money = money
        self.max_health = health
        self.health = self.max_health
        self.imgs = imgs[:]