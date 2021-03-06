import math
import pygame
pygame.mixer.init()  # sound effects

path = [
    (153, 9), (685, 201), (739, 279), (704, 373), (625, 414), (549, 406), (497, 364), (438, 287), (339, 253),
    (238, 256), (170, 284), (118, 345), (94, 495), (169, 630), (320, 702), (330, 740)
]

# sound effects
enemyDie_sound = pygame.mixer.Sound(r'../InGameSounds/enemyDie.wav')  # enemyDie_sound
enemyDie_sound.set_volume(0.2)
enemyRun_sound = pygame.mixer.Sound(r'../InGameSounds/enemyRun.wav')  # enemyRun_sound
enemyRun_sound.set_volume(0.2)
machineGun_sound = pygame.mixer.Sound(r'../InGameSounds/machineGun.wav')  # machineGun_sound
machineGun_sound.set_volume(0.2)

class Enemy:
    def __init__(self):
        self.width = 38
        self.height = 38
        self.img = None
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = path[:]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path_pos = 0
        self.dis = 0
        self.imgs = []
        self.flapped = True
        self.max_health = 1

    def draw(self, win):
        '''
        Draws the enemy with the given images
        :param win:surface
        :return:None
        '''
        self.img = self.imgs[self.animation_count//10]

        self.img = pygame.transform.scale(self.img, (60, 60))
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
        self.health_bar_cul(win)


    def collide(self, x, y):
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False

    def move(self):
        # print(self.path_pos)
        self.animation_count += 1
        # print(len(self.imgs))
        if self.animation_count >= len(self.imgs)*10:
            # enemyRun_sound.play()
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos+1 >= len(self.path):
            x2, y2 = (720, 740)
        else:
            x2, y2 = self.path[self.path_pos+1]

        move_dis = math.sqrt((x2-x1)**2+(y2-y1)**2) / 1.5
        dirn = ((x2-x1) / move_dis, (y2-y1) / move_dis)
        # turn over the direction of the img
        if dirn[0] < 0 and self.flapped:
            self.flapped = False
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, False, self.flapped)

        move_x, move_y = ((self.x + dirn[0]), (self.y+dirn[1]))
        # self.dis += math.sqrt((move_x - x1) ** 2 + (move_y - y1) ** 2)

        self.x = move_x
        self.y = move_y
        self.dis = math.sqrt((self.x - x1)**2 + (self.y - y1)**2)

        # go to next point
        if self.dis >= move_dis*1.5:
            self.dis = 0
            self.path_pos += 1
        pass

    def health_bar_cul(self, win):
        length = 30
        move_by = length / self.max_health
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255, 0, 0), (self.x - 20, self.y - 30, length, 5), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x - 20, self.y - 30, int(health_bar), 5), 0)

    def hit(self):
        self.health -= 1
        machineGun_sound.play()
        if self.health <= 0:
            enemyDie_sound.play()
            return True