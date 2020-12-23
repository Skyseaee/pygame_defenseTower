import pygame
import os
import random
import time
from enemy.scorpion import Scorpion
from towers.archerTower import ArcherTower
from towers.archerTower import ArcherTowerShort
from enemy.Club import Club
from enemy.tmall import TMall
from towers.supportTower import DamageTower
from towers.supportTower import RangeTower
from menu.menu import VerticalMenu, PlayPauseButton
from menu.Rank import rank
from menu.StartMenu import StartMenu
import bs4
import re
import requests
import math
pygame.init()
pygame.font.init()
pygame.mixer.init()  # sound effects

# sound effects
pygame.mixer.music.load(r'../InGameSounds/BGM.mp3')     # BGM
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
Click_sound = pygame.mixer.Sound(r'../InGameSounds/Click.wav')  # Click_sound
Click_sound.set_volume(0.2)
construction_sound = pygame.mixer.Sound(r'../InGameSounds/constructionCompleted.wav')  # construction_sound
construction_sound.set_volume(0.2)
enemyDie_sound = pygame.mixer.Sound(r'../InGameSounds/enemyDie.wav')  # enemyDie_sound
enemyDie_sound.set_volume(0.2)
enemyRun_sound = pygame.mixer.Sound(r'../InGameSounds/enemyRun.wav')  # enemyRun_sound
enemyRun_sound.set_volume(0.2)
enhancedMachineGun_sound = pygame.mixer.Sound(r'../InGameSounds/enhancedMachineGun.wav')  # enhancedMachineGun_sound
enhancedMachineGun_sound.set_volume(0.2)
gameLost_sound = pygame.mixer.Sound(r'../InGameSounds/gameLost.wav')  # gameLost_sound
gameLost_sound.set_volume(0.2)
lifeLost_sound = pygame.mixer.Sound(r'../InGameSounds/lifeLost.wav')  # lifeLost_sound
lifeLost_sound.set_volume(0.2)
machineGun_sound = pygame.mixer.Sound(r'../InGameSounds/machineGun.wav')  # machineGun_sound
machineGun_sound.set_volume(0.2)

lives_img = pygame.transform.scale(pygame.image.load(r'../icon/life.png'), (534//3, 159//3))
coin_img = pygame.transform.scale(pygame.image.load(r'../icon/money.png'), (534//3, 159//3))
grade_img = pygame.transform.scale(pygame.image.load(r'../icon/grade.png'), (534//3, 159//3))

startmenu_img = pygame.transform.scale(pygame.image.load(r'../icon/startmenu.png'), (2450//3, 1746//3))
# bgs = []
# indexs2 = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
#           '10', '11', '12', '13', '14', '15']
# for i in indexs2:
#     bgs.append(pygame.transform.scale(pygame.image.load(r'../渲染/background00' + i + '.jpg'), (1080, 720)))
bg = pygame.image.load(os.path.join('../渲染', 'background_new0009.jpg'))
text_font = pygame.font.Font(r'../Fonts/DIN-BlackItalicAlt.otf', 32)
# diamond = pygame.transform.scale(pygame.image.load(r'../icon/coins.png'), (64, 64))
verticalMenu = pygame.transform.scale(pygame.image.load(r'../icon/towermenu.png'), (180, 600))

buy_archer = pygame.transform.scale(pygame.image.load(r'../towers/apple.png'), (1214//18, 1421//18))
buy_archer_2 = pygame.transform.scale(pygame.image.load(r'../towers/Google.png'), (1757//24, 1756//24))
buy_damage = pygame.transform.scale(pygame.image.load(r'../towers/firefox.png'), (1712//24, 1714//24))
buy_range = pygame.transform.scale(pygame.image.load(r'../towers/twitter.png'), (2349//30, 1908//30))

play_btn = pygame.transform.scale(pygame.image.load(r'../icon/start.png'), (124//3, 157//3))
pause_btn = pygame.transform.scale(pygame.image.load(r'../icon/pause.png'), (124//3, 156//3))

attack_tower_names = ['archer', 'archer_2']
support_tower_names = ['range', 'damage']

# load music
# pygame.mixer.music.load()

waves = [
    [20, 3, 2],
    [50, 10, 5],
    [100, 0, 7],
    [0, 20, 10],
    [10, 10, 20],
    [30, 10, 20],
    [20, 10, 30],
    [50, 50, 0],
    [70, 30, 20],
    [50, 3, 20],
    [20, 100, 10],
    [20, 150, 30],
    [200, 100, 30],
]

class Game:
    def __init__(self,tencentprice,aliprice,jdprice,appleprice,googleprice,twitterprice):
        self.tencentprice = tencentprice
        self.aliprice = aliprice
        self.jdprice = jdprice
        self.appleprice = appleprice
        self.googleprice = googleprice
        self.twitterprice = twitterprice
        self.width = 1080
        self.height = 720
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.towers = []
        self.support_tower = []
        self.lives = 10
        # self.towers = 10
        self.money = 5000
        self.score = 0
        self.rank = rank()
        self.StartMenu = StartMenu(startmenu_img)
        self.bg = bg
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.bg_index = 0
        self.timer = time.time()
        self.selected_tower = None
        self.menu = VerticalMenu(self.width, 0, verticalMenu)
        self.menu.add_button(buy_archer, 'buy_archer', appleprice)
        self.menu.add_button(buy_archer_2, 'buy_archer_2', googleprice)
        self.menu.add_button(buy_damage, 'buy_damage', 0)
        self.menu.add_button(buy_range, 'buy_range', twitterprice)
        # self.moving_object = False
        self.moving_object = None
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = False
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 20, self.height - 85)
        self.font = pygame.font.Font(r'../Fonts/DINCond-BlackExpert.otf', 28)
        self.path = []
        self.score_list = []
        self.situation = False
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
            wave_enemies = [Scorpion(self.jdprice,self.jdprice / 30), Club(self.tencentprice,self.tencentprice / 20), TMall(self.aliprice , self.aliprice / 10)]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def run(self):
        self.rank.getScores('scoreRank.txt')
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(30)

            if self.situation:
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
                        if tower.collide(self.moving_object) or self.moving_object.occupyTheRoad():
                            collide = True
                            tower.place_color = (232, 131, 152, 100)
                            self.moving_object.place_color = (232, 131, 152, 150)
                        else:
                            tower.place_color = (36, 120, 132, 100)
                            if not collide:
                                self.moving_object.place_color = (36, 120, 132, 100)

                # main event loop
                for event in pygame.event.get():
                    pygame.time.delay(30)
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        # if you`re moving an object and click
                        if event.button == 1:  # 表示点击鼠标左键
                            Click_sound.play()

                        if self.moving_object:
                            not_allowed = False
                            tower_list = self.towers[:] + self.support_tower[:]
                            for tower in tower_list:
                                if tower.collide(self.moving_object) or self.moving_object.occupyTheRoad():
                                    not_allowed = True

                            if not not_allowed:
                                if self.moving_object.name in attack_tower_names:
                                    self.towers.append(self.moving_object)
                                    construction_sound.play()
                                elif self.moving_object.name in support_tower_names:
                                    self.support_tower.append(self.moving_object)
                                    construction_sound.play()

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
                                    if btn_clicked == "upgrade_button" and self.selected_tower.level<=2:
                                        if self.money >= self.selected_tower.menu.item_cost[self.selected_tower.level - 1]:
                                            self.money -= self.selected_tower.menu.item_cost[self.selected_tower.level - 1]
                                            self.selected_tower.upgrade()
                                            construction_sound.play()
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
                                    if tw.click(pos[0], pos[1]):
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
                        if en.y > 720:
                            to_del.append(en)
                    # delete all enemies off the screen
                    for d in to_del:
                        self.lives -= 1
                        lifeLost_sound.play()
                        self.enemys.remove(d)

                    # loop through towers
                    for tw in self.towers:
                        # tw.attack(self.enemys)
                        add = tw.attack(self.enemys)
                        self.money += add
                        self.score += add

                    if self.lives <= 0:
                        gameLost_sound.play()
                        self.rank.update(self.score, 'scoreRank.txt')
                        self.drawScoreBorad()
                        self.situation = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                            pos = pygame.mouse.get_pos()
                            if event.type == pygame.MOUSEBUTTONUP:
                                # print(pos[0],pos[1])
                                if pos[0] >= 350 and pos[0] <= 350 + 450 and pos[1] <= 280 + 80 and pos[1] >= 280:
                                    self.situation = True
                                    self.wave = 0
                                    self.lives = 10
                                    self.score = 0
                                    self.money = 5000
                                    print('You Lose')
                                    # run = False

                self.draw()
            else:
                self.drawScoreBorad()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONUP:
                        # print(pos[0],pos[1])
                        if pos[0] >= 350 and pos[0] <= 350 + 450 and pos[1] <= 280 + 80 and pos[1] >= 280:
                            self.situation = True
                            self.wave = 0
                            self.lives = 10
                            self.score = 0
                            self.money = 5000
                            self.enemys = []
                            self.towers = []
                            self.support_tower = []

            # check if moving object
        pygame.quit()

    def drawScoreBorad(self):
        self.win.blit(self.bg, (0, 0))
        self.StartMenu.draw(self.win)
        # generate score list
        self.score_list = self.rank.scores
        self.StartMenu.draw_score_list(self.win, self.score_list, self.score)
        # pygame.draw.rect(self.win, (255, 255, 255), (350, 280, 450, 80), 1)
        pygame.display.update()
        pass

    def draw(self):
        self.win.blit(self.bg, (0, 0))

        # for p in self.clicks:
        #   pygame.draw.circle(self.win, (255, 0, 0), (p[0], p[1]), 5, 0)
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
            tw.draw_shadow(self.win)
            tw.draw(self.win)

        # draw the range towers
        for st in self.support_tower:
            st.support(self.towers)
            st.draw_shadow(self.win)
            st.draw(self.win)
            st.draw_entity(self.win, self.towers)

        # draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)

        # redraw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)

        # draw play pause button
        self.playPauseButton.draw(self.win)

        # draw lives, grades, money
        live = lives_img
        start_x = self.width - live.get_width() - 55

        self.win.blit(live, (start_x + live.get_width() - 125, 10))

        text = text_font.render(str(self.lives), 1, (25, 29, 15))
        self.win.blit(text, (start_x + live.get_width() - 50, 15))
        # money
        money = coin_img
        start_x = self.width - money.get_width() - 55

        self.win.blit(money, (start_x + money.get_width() - 450, 10))

        text = text_font.render(str(self.money), 1, (25, 29, 15))
        self.win.blit(text, (start_x + money.get_width() - 385, 15))
        # grade
        grade = grade_img
        start_x = self.width - grade.get_width() - 55

        self.win.blit(grade, (start_x + grade.get_width() - 285, 10))

        text = text_font.render(str(self.score), 1, (25, 29, 15))
        self.win.blit(text, (start_x + grade.get_width() - 225, 15))

        # draws vertical menu
        self.menu.draw(self.win)

        # draw waves
        text = self.font.render('Wave # ' + str(self.wave), 1, (255, 255, 255))
        self.win.blit(text, (10, 20))

        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ['buy_archer', 'buy_archer_2', 'buy_damage', 'buy_range']
        object_list = [ArcherTower(x, y, self.appleprice / 8 ,self.appleprice / 5000), ArcherTowerShort(x, y, self.googleprice / 12 ,self.googleprice / 3000), DamageTower(x, y), RangeTower(x, y ,self.twitterprice / 1000)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True

        except Exception as e:
            print(str(e) + 'NOT VALID NAME')

headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
        }
tencenturl = 'http://push2.eastmoney.com/api/qt/stock/get?secid=116.00700&fields=f18,f59,f51,f52,f57,f58,f106,f105,f62,f108,f177,f43,f46,f60,f44,f45,f47,f48,f49,f113,f114,f115,f85,f84,f169,f170,f161,f163,f164,f171,f126,f168,f162,f116,f55,f92,f71,f50,f167,f117,f86,f172,f174,f175'
appleurl = 'http://push2.eastmoney.com/api/qt/stock/get?secid=105.AAPL&&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172'
googleurl = 'http://push2.eastmoney.com/api/qt/stock/get?secid=105.GOOG&&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172'
twitterurl = 'http://push2.eastmoney.com/api/qt/stock/get?secid=106.TWTR&&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172'
aliurl = 'http://push2.eastmoney.com/api/qt/stock/get?secid=106.BABA&&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172'
jdurl = 'http://push2.eastmoney.com/api/qt/stock/get?secid=105.JD&&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172'
rateurl = 'https://www.baidu.com/s?wd=港元兑换美元'
rate = float(re.findall("'1港元=(.*?)美元'",requests.get(rateurl,headers=headers).text)[0])
tencentprice = int(math.log10(float(re.findall("\"f116\":(.*?),",requests.get(tencenturl,headers=headers).text)[0]) * rate / 100000000) * 30)
aliprice = int(math.log10(float(re.findall("\"f116\":(.*?),",requests.get(aliurl,headers=headers).text)[0]) / 100000000) * 30)
jdprice = int(math.log10(float(re.findall("\"f116\":(.*?),",requests.get(jdurl,headers=headers).text)[0] )/ 100000000) * 30)
twitterprice = int(math.log10(float(re.findall("\"f116\":(.*?),",requests.get(twitterurl,headers=headers).text)[0]) / 100000000) * 400)
googleprice = int(math.log10(float(re.findall("\"f116\":(.*?),",requests.get(googleurl,headers=headers).text)[0]) / 100000000) * 400)
appleprice = int(math.log10(float(re.findall("\"f116\":(.*?),",requests.get(appleurl,headers=headers).text)[0]) / 100000000) * 400)
g = Game(tencentprice,aliprice,jdprice,appleprice,googleprice,twitterprice)
g.run()