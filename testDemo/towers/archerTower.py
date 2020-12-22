import pygame
import math
import time
from towers.Tower import Tower
from menu.menu import Menu

menu_bg = pygame.transform.scale(pygame.image.load(r'../icon/updatemenu.png'), (922 // 6, 494 // 7))
upgrade_button = pygame.transform.scale(pygame.image.load(r'../icon/update.png'), (198//5, 189//5))

archer_imgs1 = []
indexs2 = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
for index in indexs2:
    archer_imgs1.append(pygame.transform.scale(pygame.image.load(r'../towers/apple01/render00' + str(index) + '.png'),
                                               (1920//9, 1080//9)))

class ArcherTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.archer_imgs = archer_imgs1[:]
        self.archer_count = 0
        self.range = 200
        self.original_range = self.range
        self.inRange = False
        self.damage = 1
        self.left = -1
        self.timer = time.time()
        self.tower_enemy_closest = []
        self.original_damage = self.damage
        self.moving = False
        self.name = 'archer'
        self.cost = [2000, 3500, 6000, 'MAX']

        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, 3500, 6000, "MAX"])
        self.menu.add_button(upgrade_button, "upgrade_button", self.cost)

    def draw(self, win):
        '''
        draw the archer tower and its orientation specially
        :param win: surface
        :return:
        '''
        super().draw_radius(win)
        super().draw_menu(win)
        super().draw(win)

        if self.inRange and not self.moving:
            self.archer_count += 1

            if self.archer_count >= len(self.archer_imgs)*2:
                self.archer_count = 0
        else:
            self.archer_count = 0

        archer = self.archer_imgs[self.archer_count // 2]
        # archer01 = pygame.transform.scale(archer, (100, 100))
        win.blit(archer, ((self.x + self.width - archer.get_width()/2 + 2), (self.y + self.height - archer.get_height()/2 - 30)))


    def change_range(self,range):
        self.range = range + (self.level-1)*50

    def attack(self, enemies):
        '''
        attacks an enemy in the enemy list
        :param enemies: list of enemies
        :return: int
        '''
        money = 0
        self.inRange = False
        self.left = 1
        for enemy in enemies:
            enemy_x, enemy_y = enemy.x, enemy.y
            dis = math.sqrt((self.x-enemy_x)**2 + (self.y-enemy_y)**2)
            # print(dis)
            if dis < self.range and enemy.health > 0.5 and enemy.x <= 1080:
                self.inRange = True
                self.tower_enemy_closest.append(enemy)

        if len(self.tower_enemy_closest)>0:
            first_enemy = self.tower_enemy_closest[0]
            if first_enemy.health < 0:
                self.tower_enemy_closest.clear()

            if first_enemy:
                if time.time() - self.timer >= 0.5:
                    self.timer = time.time()
                    if first_enemy.hit():
                        # self.tower_enemy_closest.remove(first_enemy)
                        if first_enemy in enemies:
                            money = first_enemy.money
                            enemies.remove(first_enemy)

        # print(money)
        return money

archer_imgs = []
for index in indexs2:
    archer_imgs.append(pygame.transform.scale(pygame.image.load(r'../towers/Google/render00' + str(index) + '.png'),
                                               (1920//8, 1080//8)))

# draw another tower, which is the same as the first tower now
class ArcherTowerShort(ArcherTower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.archer_imgs = archer_imgs[:]
        self.archer_count = 0
        self.range = 120
        self.damage = 2
        self.original_damage = self.damage
        self.inRange = False
        self.left = -1
        # self.timer = time.time()
        self.name = 'archer_2'
        self.cost = [2500, 5500, 7000, 'MAX']

        self.menu = Menu(self, self.x, self.y, menu_bg, [2500, 5500, 7000, 'MAX'])
        self.menu.add_button(upgrade_button, 'upgrade_button', self.cost)

