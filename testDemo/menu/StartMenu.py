import pygame

pygame.font.init()
title_img = pygame.transform.scale(pygame.image.load(r'../icon/newtitle.png'), (1955 // 4 + 19, 388 // 4 + 3))
start_img = pygame.transform.scale(pygame.image.load(r'../icon/startgame.png'), (1346 // 3, 167 // 3))

first_img = pygame.transform.scale(pygame.image.load(r'../icon/first.png'), (155 // 4, 188 // 4))
second_img = pygame.transform.scale(pygame.image.load(r'../icon/second.png'), (151 // 4, 197 // 4))
third_img = pygame.transform.scale(pygame.image.load(r'../icon/third.png'), (151 // 4, 163 // 4))

text_font = pygame.font.Font(r'../Fonts/DIN-BlackItalicAlt.otf', 32)

class StartMenu:
    def __init__(self, img):
        self.img = img
        self.x = 150
        self.y = 50
        self.title_img = title_img
        self.start_img = start_img
        self.score_img = [first_img, second_img, third_img]

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        win.blit(self.title_img, (self.x + 175, self.y + 120))
        win.blit(self.start_img, (self.x + 200, self.y + 240))
        pass

    def draw_score_list(self, win, score_list, current_score):
        index = 0
        for score, score_img in zip(score_list, self.score_img):
            win.blit(score_img, (self.x + 280, self.y + 320 + index*50))
            score = text_font.render(str(score), 1, (25, 29, 15))
            win.blit(score, (self.x + 480, self.y + 320 + index*50))
            index += 1

        current_text = text_font.render('YOUR SCORE', 1, (23, 17, 46))
        current_score = text_font.render(str(current_score), 1, (25, 29, 15))
        win.blit(current_score, (self.x + 480, self.y + 480))
        win.blit(current_text, (self.x + 200, self.y + 480))
        pass