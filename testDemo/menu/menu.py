import pygame

diamond = pygame.transform.scale(pygame.image.load(r'../icons/coin.png'), (48, 48))

class Button:
    def __init__(self, menu, img, name, cost):
        self.name = name
        self.img = img
        self.x = menu.x - 60
        self.y = menu.y - 121
        self.menu = menu
        self.cost = cost
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def click(self, x, y):
        '''
        return if the position haa collided with the menu
        :param x:
        :param y:
        :return: bool
        '''
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False
        pass

    def draw(self, win):
        win.blit(self.img, (self.x - 5, self.y))

    def update(self):
        self.x = self.menu.x - 60
        self.y = self.menu.y - 121

class VerticalButton(Button):
    def __init__(self, x, y, img, name, cost):
        self.name = name
        self.img = img
        self.x = x - 60
        self.y = y - 120
        # self.menu = menu
        self.cost = cost
        self.width = self.img.get_width()
        self.height = self.img.get_height()

class PlayPauseButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        # self.name = name
        self.img = pause_img
        self.play = play_img
        self.pause_img = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.pause = True

    def draw(self, win):
        if self.pause:
            win.blit(self.play, (self.x, self.y))
        else:
            win.blit(self.pause_img, (self.x, self.y))

class Menu:
    def __init__(self, tower, x, y, menu_bg, item_cost):
        self.x = x
        self.y = y
        self.width = menu_bg.get_width()
        self.height = menu_bg.get_height()
        self.component_names = []
        self.item_cost = item_cost
        self.imgs = []
        self.buttons = []
        self.items = 0
        self.menu_bg = menu_bg
        self.font = pygame.font.SysFont(r'../Fonts/DINCond-BlackExpert.otf', 30)
        self.tower = tower

    def click(self, x, y):
        '''
        return if the position haa collided with the menu
        :param x:
        :param y:
        :return: bool
        '''
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False
        pass

    def add_button(self, img, name, cost):
        '''
        add buttons into menu
        :param img:
        :param name:
        :return:
        '''
        self.items += 1
        inc_x = self.width / self.items
        btn_x = self.x - self.menu_bg.get_width() // 2
        btn_y = self.y - 120
        self.buttons.append(Button(self, img, name, cost))

    def draw(self, win):
        '''
        draw the menu and buttons
        :param win: surface
        :return:
        '''
        win.blit(self.menu_bg, (self.x - self.width // 2, self.y - self.height - 10))
        for button in self.buttons:
            button.draw(win)
            win.blit(diamond, (button.x + 30, button.y + 10))
            text = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, (255, 255, 255))
            win.blit(text, (button.x + button.width + 7, button.y + diamond.get_height() // 1.6))

    def get_click(self, x, y):
        '''
        return the clicked item from the menu
        :param x:
        :param y: 
        :return: str
        '''
        for button in self.buttons:
            if button.click(x, y):
                return button.name

    def update(self):
        '''
        update menu and button location
        :return:
        '''
        for button in self.buttons:
            button.update()

class VerticalMenu(Menu):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.buttons = []
        self.img = img
        self.items = 0
        self.font = pygame.font.SysFont(r'C:\Users\timing\AppData\Local\Microsoft\Windows\Fonts\DINCond-BlackAlternate.otf', 30)

    def add_button(self, img, name, cost):
        '''
        add buttons into menu
        :param img:
        :param name:
        :return:
        '''
        self.item_cost = cost
        self.items += 1
        # inc_x = self.width / self.items
        btn_x = self.x - self.img.get_width() + 70
        btn_y = (self.items - 1)*120 + 240
        self.buttons.append(VerticalButton(btn_x, btn_y, img, name, cost))

    def draw(self, win):
        '''
        draw the menu and buttons
        :param win: surface
        :return:
        '''
        win.blit(self.img, (self.x - self.img.get_width() - 25, self.y + 110))

        for button in self.buttons:
            button.draw(win)
            win.blit(diamond, (button.x - 10, button.y + 60))
            text = self.font.render(str(button.cost), 1, (255, 255, 255))
            win.blit(text, (button.x + button.width / 2 - text.get_width()/2 + 15, button.y + button.height - 5))

    def get_item_cost(self, name):
        '''
        gets cost of items
        :return:
        '''
        for button in self.buttons:
            if button.name == name:
                return button.cost
        return -1