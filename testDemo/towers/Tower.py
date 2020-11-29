import pygame
import math
from menu.menu import Menu

menu_bg = pygame.transform.scale(pygame.image.load(r'../bg/menu.png'), (128, 128))
upgrade_button = pygame.transform.scale(pygame.image.load(r'../icons/tools.png'), (64, 64))

class Tower:
    '''
    abstract class for towers
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.level = 1
        self.sell_cost = [0, 0, 0]
        self.price = [0, 0, 0]
        self.selected = False
        self.item_cost = [5000, 7000, 12000, 'MAX']
        self.menu = Menu(self, self.x, self.y, menu_bg, self.item_cost)
        self.tower_imgs = []
        self.archer_imgs = []
        self.damage = 1
        self.range = 0
        self.inRange = 0
        self.left = 1
        self.menu.add_button(upgrade_button, 'upgrade_button', 0)
        self.place_color = (36, 120, 132, 100)

    def draw(self, win):
        imgs = self.archer_imgs[-1]
        win.blit(imgs,(self.x - imgs.get_width()//2, self.y - imgs.get_height()//2))

    def draw_menu(self, win):
        # draw menu
        if self.selected and self.selected:
            self.menu.draw(win)

        pass

    def draw_radius(self, win):
        # draw range circle
        if self.selected:
            circle_surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
            # circle_surface.set_alpha(128)
            # circle_surface.fill(0,255,0))
            surface = pygame.draw.circle(circle_surface, (44, 195, 206, 50), (self.range, self.range), self.range, 0)
            win.blit(circle_surface, (self.x - self.range, self.y - self.range))

    def draw_placement(self, win):
        # draw range circle

        circle_surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(circle_surface, self.place_color, (50, 50), 45, 0)
        win.blit(circle_surface, (self.x - 50, self.y - 50))
        # print('draw placement range')

    def click(self, X, Y):
        '''
        return true if tower be clicked, else false
        :param x: int
        :param y: int
        :return: bool
        '''
        img = self.archer_imgs[-1]
        if X <= self.x - img.get_width() // 2 + 120 and X >= self.x - img.get_width() // 2:
            if Y <= self.y + 120 - img.get_height() // 2 and Y >= self.y - img.get_height() // 2:
                return True
        return False

        pass

    def sell(self):
        '''
        call to sell the tower, returns sell price
        :return: int
        '''
        pass

    def upgrade(self):
        '''
        upgrade the tower by cost
        :return:
        '''
        if self.level <= 3:
            self.level += 1
            self.damage += 1
            self.range += 50
        pass

    def get_upgrade_cost(self):
        return self.price[self.level - 1]

    def move(self, x, y):
        '''
        moves tower to given x and y
        :param x: int
        :param y: int
        :return:
        '''
        self.x = x
        self.y = y
        self.menu.x = x
        self.menu.y = y
        self.menu.update()

    def collide(self, otherTower):
        x2 = otherTower.x
        y2 = otherTower.y

        dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
        if dis >= 100:
            return False
        else:
            return True