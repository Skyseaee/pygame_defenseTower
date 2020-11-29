import pygame
from . import enemy

imgs = []
indexs = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
          '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
for index in indexs:
    # add_str = x
    # print('../enemys/3/3_enemies_1_attack_0' + str(add_str) + '.png')
    imgs.append(pygame.image.load(r'../enemys/3/3_enemies_1_attack_0' + index + '.png'))

class Club(enemy.Enemy):
    def __init__(self):
        super().__init__()
        self.name = 'Club'
        self.money = 200
        self.max_health = 3
        self.health = self.max_health

        self.imgs = imgs[:]