import pygame
import math
from menu.menu import Menu
pygame.mixer.init()  # sound effects

# sound effects
construction_sound = pygame.mixer.Sound(r'../InGameSounds/constructionCompleted.wav')  # construction_sound
construction_sound.set_volume(0.2)

menu_bg = pygame.transform.scale(pygame.image.load(r'../icon/updatemenu.png'), (922 // 6, 494 // 7))
upgrade_button = pygame.transform.scale(pygame.image.load(r'../icon/update.png'), (198//5, 189//5))

path = [
    (153, 9), (685, 201), (739, 279), (704, 373), (625, 414), (549, 406), (497, 364), (438, 287), (339, 253),
    (238, 256), (170, 284), (118, 345), (94, 495), (169, 630), (320, 702), (330, 740)
]

tower_imgs1 = []
# load archer tower images
for x in range(1, 4):
    tower_imgs1.append(pygame.transform.scale(pygame.image.load(r'../icon/base0' + str(x) + '.png')
                                              , (1920//9, 1080//9)))

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
        self.price = [5000, 7000, 12000, 'MAX']
        self.selected = False
        self.item_cost = [5000, 7000, 12000, 'MAX']
        self.menu = Menu(self, self.x, self.y, menu_bg, self.item_cost)
        self.tower_imgs = tower_imgs1[:]
        self.damage = 1
        self.range = 0
        self.inRange = 0
        self.left = 1
        self.menu.add_button(upgrade_button, 'upgrade_button', 0)
        self.place_color = (36, 120, 132, 100)
        self.effected = True

    def draw(self, win):
        imgs = self.tower_imgs[self.level - 1]
        win.blit(imgs, (self.x - imgs.get_width()//2, self.y - imgs.get_height()//2))

    def draw_menu(self, win):
        # draw menu
        if self.selected:
            self.menu.draw(win)

        pass

    def draw_radius(self, win):
        # draw range circle
        if self.selected:
            # print(self.range*4, self.range*4)
            circle_surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
            # circle_surface.set_alpha(128)
            # circle_surface.fill(0,255,0))
            pygame.draw.circle(circle_surface, (44, 195, 206, 20), (self.range, self.range), self.range, 0)
            win.blit(circle_surface, (self.x - self.range, self.y - self.range))
            # pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), 200, 3)

    def draw_placement(self, win):
        # draw range circle
        circle_surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(circle_surface, self.place_color, (50, 50), 45, 0)
        win.blit(circle_surface, (self.x - 50, self.y - 50))
        # print('draw placement range')

    def draw_shadow(self, win):
        circle_surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(circle_surface, (0, 0, 0, 50), (50, 50), 50)
        win.blit(circle_surface, (self.x - 50, self.y - 45))

    def click(self, X, Y):
        '''
        return true if tower be clicked, else false
        :param x: int
        :param y: int
        :return: bool
        '''
        img = self.tower_imgs[self.level-1]
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
            self.effected = True
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

    def occupyTheRoad(self):
        '''
        for each two node points in path
        judge whether the position where tower to be constructed
        is in a range of t that might occupy the road for monsters
        :param self: tower object
        :param path: path node list
        :param t: range that a tower cant be constructed this amount away from the path of monsters
        :return: true or false
        '''
        t = 50
        for nodeIndex in range(len(path) - 1):
            x1 = path[nodeIndex][0]
            y1 = path[nodeIndex][1]

            x2 = path[nodeIndex + 1][0]
            y2 = path[nodeIndex + 1][1]
            # the line where the segment from is Ax+By+C=0
            # B=1
            A = -((y2 - y1) / (x2 - x1))
            C = x1 * ((y2 - y1) / (x2 - x1)) - y1

            disToSegment = abs(A * self.x + self.y + C) / math.sqrt(A ** 2 + 1)

            disToNodePoint1 = math.sqrt((self.x - x1) ** 2 + (self.y - y1) ** 2)
            disToNodePoint2 = math.sqrt((self.x-x2) ** 2 + (self.y - y2) ** 2)

            maxDis_NotToIgnore = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + t ** 2)

            if disToSegment < t and disToNodePoint1 <= maxDis_NotToIgnore and disToNodePoint2 <= maxDis_NotToIgnore:
                return True

        return False