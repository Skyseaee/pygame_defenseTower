from .Tower import Tower
import pygame
import math

imgs = [pygame.transform.scale((pygame.image.load(r'../towers/03.png')),(100,100))]
class RangeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.effect = [0.2, 0.4]
        self.range = 300
        self.original_range = self.range
        self.archer_imgs = imgs[:]
        self.width = self.height = 100
        self.name = 'range'
        self.price = [2000]
        self.level = 1
        self.moving = False

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)
        super().draw_menu(win)

    def support(self, towers):
        '''
        will modify towers according to ability
        :param towers: list
        :return:
        '''
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
            if dis <= self.range + tower.width/2:
                effected.append(tower)

        for tower in effected:
            tower.range = tower.range + round(tower.range * self.effect[self.level - 1])
        pass

damage_imgs = [pygame.transform.scale((pygame.image.load(r'../towers/04.png')),(100,100))]
class DamageTower(RangeTower):
    '''
    add damage to surrounding towers
    '''
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 400
        self.imgs = damage_imgs[:]
        self.effect = [0.5, 1]
        self.name = 'damage'
        self.price = [2000]

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)
        super().draw_menu(win)

    def support(self, towers):
        '''
        will modify towers according to ability
        :param towers: list
        :return:
        '''
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
            if dis <= self.range + tower.width/2:
                effected.append(tower)

        for tower in effected:
            tower.damage = tower.original_damage + round(tower.original_damage * self.effect[-1])
        pass