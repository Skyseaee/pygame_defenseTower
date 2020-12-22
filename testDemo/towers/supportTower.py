from .Tower import Tower
import pygame
import math

archer_imgs1 = []
indexs = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
for index in indexs:
    archer_imgs1.append(pygame.transform.scale(pygame.image.load(r'../towers/twitter/render00' + str(index) + '.png'),
                                               (1920//9, 1080//9)))

class RangeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.effect = [0.2, 0.4]
        self.range = 200
        self.damage = 0
        self.original_range = self.range
        self.archer_imgs = archer_imgs1[:]
        self.width = self.height = 100
        self.name = 'range'
        self.price = [2000]
        self.level = 1
        self.inRange = False
        self.archer_count = 0
        self.changeFrame = False

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)
        super().draw_menu(win)
        # self.draw_entity(win)

    def draw_entity(self, win, towers):
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
            if dis <= self.range + 50:
                effected.append(tower)

        for effect in effected:
            if effect.inRange:
                self.changeFrame = True

        if self.inRange and self.changeFrame:
            self.archer_count += 1

            if self.archer_count >= len(self.archer_imgs)*1:
                self.archer_count = 0
        else:
            self.archer_count = 0

        archer = self.archer_imgs[self.archer_count // 1]
        win.blit(archer, ((self.x + self.width - archer.get_width()/2 - 110), (self.y + self.height - archer.get_height()/2 - 160)))

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
            if dis <= self.range + 50:
                effected.append(tower)

        for tower in effected:
            if tower.effected:
                tower.range = tower.range + int(round(tower.range * self.effect[self.level - 1]))
                tower.effected = False

        if len(effected)>0:
            self.inRange = True
        else:
            self.inRange = False
        pass

damage_imgs1 = []
indexs = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
for index in indexs:
    damage_imgs1.append(pygame.transform.scale(pygame.image.load(r'../towers/fox/render00' + str(index) + '.png'),
                                               (1920//9, 1080//9)))

class DamageTower(RangeTower):
    '''
    add damage to surrounding towers
    '''
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 200
        self.archer_imgs = damage_imgs1[:]
        self.effect = [0.5, 1]
        self.name = 'damage'
        self.price = [2000]
        self.inRange = False

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)
        super().draw_menu(win)

    def draw_entity(self, win, towers):
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
            if dis <= self.range + 50:
                effected.append(tower)

        for effect in effected:
            if effect.inRange:
                self.changeFrame = True

        if self.inRange and self.changeFrame:
            self.archer_count += 1

            if self.archer_count >= len(self.archer_imgs)*1:
                self.archer_count = 0
        else:
            self.archer_count = 0

        archer = self.archer_imgs[self.archer_count // 1]
        # archer01 = pygame.transform.scale(archer, (100, 100))
        win.blit(archer, ((self.x + self.width - archer.get_width()/2 - 100), (self.y + self.height - archer.get_height()/2 - 140)))

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
            if dis <= self.range + 50:
                effected.append(tower)

        for tower in effected:
            tower.damage = tower.original_damage + int(round(tower.original_damage * self.effect[self.level-1]))

        if len(effected)>0:
            self.inRange = True
        else:
            self.inRange = False

        pass