import pygame
import os
import random
import time
from enemy.scorpion import Scorpion
from towers.archerTower import ArcherTower
from towers.archerTower import ArcherTowerShort
from enemy.Club import Club
from towers.supportTower import DamageTower
from towers.supportTower import RangeTower
from menu.menu import VerticalMenu, PlayPauseButton
pygame.init()
pygame.font.init()

lives_img = pygame.image.load(r'../others/heart.png')
start_img = pygame.image.load(r'../others/fight.png')
bg = pygame.image.load(os.path.join('../bg', 'bg.jpg'))
text_font = pygame.font.SysFont(r'../Fonts/DINCond-BlackExpert.otf', 48)
diamond = pygame.transform.scale(pygame.image.load(r'../icons/coin.png'), (64, 64))
verticalMenu = pygame.transform.scale(pygame.image.load(r'../bg/verticalMenu.png'), (150, 500))

buy_archer = pygame.transform.scale(pygame.image.load(r'../icons/sword.png'), (80, 80))
buy_archer_2 = pygame.transform.scale(pygame.image.load(r'../icons/axe.png'), (80, 80))
buy_damage = pygame.transform.scale(pygame.image.load(r'../icons/hammer.png'), (80, 80))
buy_range = pygame.transform.scale(pygame.image.load(r'../icons/potionBlue.png'), (80, 80))

play_btn = pygame.transform.scale(pygame.image.load(r'../icons/play.png'), (50, 50))
pause_btn = pygame.transform.scale(pygame.image.load(r'../icons/pause.png'), (50, 50))

attack_tower_names = ['archer', 'archer_2']
support_tower_names = ['range', 'damage']

# load music
# pygame.mixer.music.load()

waves = [
    [20, 3],
    [50, 10],
    [100, 0],
    [0, 20],
    [0, 50],
    [100, 0],
    [20, 0],
    [50, 100],
    [100, 100],
    [50, 3],
    [20, 100],
    [20, 150],
    [200, 100],
]

path = [
    (-5, 20),
    (20, 20),
    (40, 99),
    (49, 389),
    (158, 475),
    (463, 568),
    (768, 490),
    (1066, 512),
    (1100, 512)
]
class Game:
    def __init__(self):
        self.width = 1080
        self.height = 720
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.towers = []
        self.support_tower = []
        self.lives = 10
        # self.towers = 10
        self.money = 5000
        self.bg = bg
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.selected_tower = None
        self.menu = VerticalMenu(self.width, 0, verticalMenu)
        self.menu.add_button(buy_archer, 'buy_archer', 500)
        self.menu.add_button(buy_archer_2, 'buy_archer_2', 700)
        self.menu.add_button(buy_damage, 'buy_damage', 1000)
        self.menu.add_button(buy_range, 'buy_range', 1000)
        # self.moving_object = False
        self.moving_object = None
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = False
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 20, self.height - 85)
        self.font = pygame.font.SysFont(r'../Fonts/DINCond-BlackExpert.otf', 30)
        self.path = []
        # self.clicks = []

        self.lives = 10
    def gen_enemies(self):
        '''
        generate the next enemy or enemies to show
        :return: enemy
        '''
        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.playPauseButton.pause = self.pause

        else:
            wave_enemies = [Scorpion(), Club()]
            for x in range(len(self.current_wave)):
                # print(len(self.current_wave))
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)

            if self.pause == False:
                # generate monstors
                if time.time() - self.timer >= random.randrange(1, 6) / 5:
                    self.timer = time.time()
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()
            # check for moving object
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.towers[:] + self.support_tower[:]
                collide = False
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (232, 131, 152, 100)
                        self.moving_object.place_color = (232, 131, 152, 150)
                    else:
                        tower.place_color = (36, 120, 132, 100)
                        if not collide:
                            self.moving_object.place_color = (36, 120, 132, 100)
            #     tower_

            # main event loop
            for event in pygame.event.get():
                pygame.time.delay(30)
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # if you`re moving an object and click
                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.towers[:] + self.support_tower[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object):
                                not_allowed = True

                        if not not_allowed and self.perp_bisector_dis(self.moving_object):
                            if self.moving_object.name in attack_tower_names:
                                self.towers.append(self.moving_object)
                            elif self.moving_object.name in support_tower_names:
                                self.support_tower.append(self.moving_object)

                            self.moving_object.moving = False
                            self.moving_object = None

                    else:
                        # check for play or pause
                        if self.playPauseButton.click(pos[0], pos[1]):
                            self.pause = not self.pause
                            self.playPauseButton.pause = self.pause

                        # look if you clicked on attack tower or support tower
                        side_menu_button = self.menu.get_click(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)

                            # print(side_menu_button)

                        # check if clicked on the attack tower or support tower
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_click(pos[0], pos[1])
                            if btn_clicked:
                                # print(btn_clicked)
                                if btn_clicked == "upgrade_button":
                                    if self.money >= self.selected_tower.menu.item_cost[self.selected_tower.level - 1]:
                                        self.money -= self.selected_tower.menu.item_cost[self.selected_tower.level - 1]
                                        self.selected_tower.upgrade()
                                pass

                        if not btn_clicked:
                            # look the range of the attack_towers
                            for tw in self.towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False
                            # look the range of the support_towers
                            for tw in self.support_tower:
                                if tw.click(pos[0],pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False
                    # self.clicks.append(pos)
                    # print(self.clicks)
            if not self.pause:
                # loop through enemies
                to_del = []
                for en in self.enemys:
                    en.move()
                    if en.x > 1080:
                        to_del.append(en)
                # delete all enemies off the screen
                for d in to_del:
                    self.lives -= 1
                    self.enemys.remove(d)

                # loop through towers
                for tw in self.towers:
                    # tw.attack(self.enemys)
                    self.money += tw.attack(self.enemys)

                if self.lives <= 0:
                    print('You Lose')
                    run = False

            self.draw()

            # check if moving object
        pygame.quit()

    def perp_bisector_dis(self, tower):
        '''
        return if you can place tower based on distance from path
        :param tower:
        :return: bool
        '''
        # find two closest points
        closest = []
        # for point in path:
        #     dis = math.sqrt((tower.x - point[0])**2 + (tower.y - point[1])**2)
        #     closest.append([dis, point])
        #
        # closest = closest.sort(key = lambda x: x[0])
        # closest1 = closest[0][1]
        # closest2 = closest[1][1]
        #
        # line_vector = (closest2[0] - closest1[0], closest2[1] - closest1[1])
        # slope = line_vector[1] / line_vector[0]
        # c = closest1[1] - closest1[0]*slope
        # b = 1/slope
        # c_left = -closest1[1] * b
        # c_right = closest1[0]
        # dis = abs(line_vector[0]*tower.x + line_vector[1]*tower.y + c)/math.sqrt(line_vector[0]**2 + line_vector[1]**2)

        return True

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        # print('draw is over')
        # for p in self.clicks:
          # pygame.draw.circle(self.win,(255,0,0),(p[0],p[1]),5,0)
        # draw attack towers
        if self.moving_object:
            for tower in self.towers:
                tower.draw_placement(self.win)

            for tower in self.support_tower:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)

        # draw the enemies
        for en in self.enemys:
            en.draw(self.win)

        # draw the towers
        for tw in self.towers:
            tw.draw(self.win)

        # draw the range towers
        for st in self.support_tower:
            st.support(self.towers)
            st.draw(self.win)

        # draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)

        # redraw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)

        # draw play pause button
        self.playPauseButton.draw(self.win)

        # draw lives
        live = lives_img
        start_x = self.width - live.get_width() - 55

        self.win.blit(live, (start_x + live.get_width() + 5, 10))

        text = text_font.render(str(self.lives), 1, (255, 255, 255))
        self.win.blit(text, (start_x + 17, 19))

        # draws money
        money = diamond
        start_x = self.width - money.get_width() - 45
        self.win.blit(money, (start_x + live.get_width() + 5, 5 + live.get_height()))

        text = text_font.render(str(self.money), 1, (255, 255, 255))
        self.win.blit(text, (start_x - 20, 20 + live.get_height()))

        # draws vertical menu
        self.menu.draw(self.win)

        # draw waves
        text = self.font.render('Wave # ' + str(self.wave), 1, (255, 255, 255))
        self.win.blit(text, (10, 20))

        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ['buy_archer', 'buy_archer_2', 'buy_damage', 'buy_range']
        object_list = [ArcherTower(x, y), ArcherTowerShort(x, y), DamageTower(x, y), RangeTower(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True

        except Exception as e:
            print(str(e) + 'NOT VALID NAME')

g = Game()
g.run()