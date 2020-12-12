import pygame
import datetime as dt
from sprites import *
import sqlite3


class Card:
    def __init__(self, window, x, y, widht, height, image=None, color=None):
        self.window = window
        self.x = x
        self.y = y
        self.image = image
        self.widht = widht
        self.height = height
        self.color = color

    def draw_card(self):
        if self.image:
            self.image = pygame.transform.scale(self.image, (self.widht, self.height))
            self.window.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(self.window, self.color, (self.x, self.y, self.widht, self.height))


class Button:
    def __init__(self, window, x, y, widht, height, image=None, image2=None, color=None):
        self.window = window
        self.x = x
        self.y = y
        self.widht = widht
        self.height = height
        self.image = image
        self.image_m = image2
        self.color = color
        self.flag = True

    def draw_button(self, x=None, y=None):
        if not x:
            x = self.x
        if not y:
            y = self.y
        if not self.color:
            self.image = pygame.transform.scale(self.image, (self.widht, self.height))
            self.window.blit(self.image, (x, y))
        else:
            pygame.draw.rect(self.window, self.color, (x, y, self.widht, self.height))

    def click(self, function):
        mouse = pygame.mouse.get_pos()
        if ((self.x < mouse[0] < self.x + self.widht) and
                (self.y < mouse[1] < self.y + self.height)):
            if self.image_m:
                self.window.blit(self.image_m, (self.x, self.y))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.flag:
                        function()
        elif self.image:
            self.window.blit(self.image, (self.x, self.y))

    def set_clicked(self, bool):
        if bool:
            self.flag = True
        else:
            self.flag = False


class Animal:
    def __init__(self, window, sprites, x, y):
        self.window = window
        self.sprites = sprites
        self.x = x
        self.y = y
        self.n = 0
        self.flag = True

    def animation(self, x=None, y=None):
        if not x:
            x = self.x
        if not y:
            y = self.y
        if self.n == len(self.sprites):
            self.flag = False
            self.n -= 1
        if self.n < 0:
            self.flag = True
            self.n += 1
        self.window.blit(self.sprites[self.n], (x, y))
        if self.flag:
            self.n += 1
        else:
            self.n -= 1
        pygame.time.delay(100)

    def feed(self, code):
        con = sqlite3.connect('game_db.sqlite')
        cur = con.cursor()
        cur.execute("""UPDATE animals
                        SET last_time_food = (?)
                        WHERE animal_code = '(?)'""",
                    (dt.datetime.today(), code)).fetchall()
        con.commit()
        con.close()


class Event:
    def __init__(self, window):
        self.window = window
        self.x = 120
        self.y = 112
        self.widht = 560
        self.height = 280
        self.image = event_img

    def trigger_event(self):
        self.window.blit(self.image, (self.x, self.y))

    def trigger_notplayed_event(self, math, rus):
        self.window.blit(self.image, (self.x, self.y))
        to_write(self.window, 'Ваши питомцы устроили забастовку!',
                 self.x + 25, self.y + 25, size=35)
        to_write(self.window, 'Для того чтобы они прекратили забастовку, надо сыграть',
                 self.x + 25, self.y + 60)
        msg = ''
        if math != rus:
            if not math:
                msg = 'в игру из математики.'
            elif not rus:
                msg = 'в игру из русского.'
        else:
            msg = 'в любую игру.'
        to_write(self.window, msg, self.x + 25, self.y + 80)


def to_write(window, msg, x, y, size=20):
    font = pygame.font.SysFont('arial', size)
    text = font.render(msg, True, (0, 0, 0))
    window.blit(text, (x, y))
