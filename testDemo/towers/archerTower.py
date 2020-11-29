import pygame
import math
import time
from towers.Tower import Tower


archer_imgs = []
for x in range(1,7):
    add_str = x
    archer_imgs.append(pygame.image.load(r'../towers/tower01/01_' + str(add_str) + '.png'))

class ArcherTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = []
        self.archer_imgs = archer_imgs[:]
        self.archer_count = 0
        self.range = 350
        self.original_range = self.range
        self.inRange = False
        self.left = -1
        self.timer = time.time()
        self.tower_enemy_closest = []
        self.original_damage = self.damage
        self.moving = False
        self.name = 'archer'

    def draw(self, win):
        '''
        draw the archer tower and its orientation specially
        :param win: surface
        :return:
        '''
        super().draw_radius(win)
        super().draw_menu(win)
        # super().draw(win)

        archer = self.archer_imgs[self.archer_count]
        archer01 = pygame.transform.scale(archer, (100, 100))
        if self.inRange and not self.moving:
            self.archer_count += 1
            archer01 = pygame.transform.rotate(archer01, -10*self.archer_count*self.left)

            if self.archer_count >= len(self.archer_imgs):
                self.archer_count = 0
        else:
            self.archer_count = 0

        win.blit(archer01, ((self.x + self.width - archer01.get_width()/2), (self.y + self.height - archer01.get_height()/2)))


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
        # enemies = set(enemies)
        # self.tower_enemy_closest.sort(key=lambda x: x.x)
        if len(self.tower_enemy_closest)>0:
            first_enemy = self.tower_enemy_closest[0]
            # print(first_enemy.health)
            # print(len(self.tower_enemy_closest))
            if first_enemy.health < 0:
                self.tower_enemy_closest.clear()
                # self.tower_enemy_closest.remove(first_enemy)
                # del first_enemy
            # print(len(self.tower_enemy_closest))


            # for enemy in self.tower_enemy_closest:
            #     if enemy.health <= 0:
            #         index += 1
            #         continue
            #     else:
            #         first_enemy = self.tower_enemy_closest[index]
            # print(first_enemy == None)
            # print(type(first_enemy))
            if first_enemy:
                if time.time() - self.timer >= 0.5:
                    self.timer = time.time()
                    if first_enemy.hit():
                        # self.tower_enemy_closest.remove(first_enemy)
                        if first_enemy in enemies:
                            money = first_enemy.money
                            enemies.remove(first_enemy)


                # change the orientation of the tower
                for x, img in enumerate(self.archer_imgs):
                    if self.y <= first_enemy.y:
                        self.archer_imgs[x] = pygame.transform.flip(img, False, True)
                if first_enemy != None and first_enemy.x > self.x and not self.left:
                    self.left = 1

                elif first_enemy != None and self.left and first_enemy.x < self.x:
                    self.left = -1
        # print(money)
        return money

# draw another tower, which is the same as the first tower now
class ArcherTowerShort(ArcherTower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = []
        self.archer_imgs = archer_imgs[:]
        self.archer_count = 0
        self.range = 350
        self.inRange = False
        self.left = -1
        self.timer = time.time()
        self.tower_enemy_closest = []
        self.name = 'archer_2'
