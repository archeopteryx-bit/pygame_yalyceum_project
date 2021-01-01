import pygame
import sys
import datetime as dt
import time
from random import choice, sample, randint
import sqlite3
from classes import *
from sprites import *


class MainWindow:
    def __init__(self):
        super().__init__()
        self.math_games = Button(game_display, 100, 20, 600, 96, math_image, math_image_mouse)
        self.rus_games = Button(game_display, 100, 140, 600, 96, rus_image, rus_image_mouse)
        self.home = Button(game_display, 100, 260, 600, 96, home_image, home_image_mouse)
        self.shop = Button(game_display, 100, 380, 600, 96, shop_image, shop_image_mouse)

    def create_window(self):
        game_display.blit(back_select_game, (0, 0))
        self.math_games.draw_button()
        self.rus_games.draw_button()
        self.home.draw_button()
        self.shop.draw_button()

    def selecting(self):
        self.math_games.click(self.math)
        self.rus_games.click(self.rus)
        self.home.click(self.go_to_home)
        self.shop.click(self.go_to_shop)

    def math(self):
        global global_play, difficult
        difficult = True
        global_play = True
        diff = SelectDifficultyLevel()
        diff.create_window()
        while difficult:
            clock.tick(FPS)
            diff.select()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
        change_coins_quality()
        if global_play:
            mult_tab = MultiplicationTable()
            mult_tab.create_window()
            mult_tab.create_lvl()
        while global_play:
            pygame.mixer.music.pause()
            clock.tick(FPS)
            mult_tab.check_cards()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
        self.create_window()

    def rus(self):
        global global_play, difficult
        difficult = True
        global_play = True
        diff = SelectDifficultyLevel()
        diff.create_window()
        while difficult:
            clock.tick(FPS)
            diff.select()
            if current_level == NORMAL or current_level == HARD:
                difficult = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
        change_coins_quality()
        if global_play:
            vocab_words = VocabularyWords()
            vocab_words.create_window()
            vocab_words.create_level()
        while global_play:
            pygame.mixer.music.pause()
            clock.tick(FPS)
            vocab_words.change_letters()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
        self.create_window()

    def go_to_home(self):
        global global_play
        pygame.mixer.music.load('Music\\home_bg_melody.wav')
        pygame.mixer.music.play(-1)
        global_play = True
        home = House()
        home.create_window()
        while global_play:
            clock.tick(FPS)
            home.check_played()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
        self.create_window()

    def go_to_shop(self):
        global global_play
        global_play = True
        shop = Shop()
        shop.create_window()
        while global_play:
            clock.tick(FPS)
            shop.select()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
        self.create_window()


class SelectDifficultyLevel:
    def __init__(self):
        self.easy = Button(game_display, 100, 54, 600, 96, easy_lvl, easy_lvl_mouse)
        self.normal = Button(game_display, 100, 204, 600, 96, normal_lvl, normal_lvl_mouse)
        self.hard = Button(game_display, 100, 354, 600, 96, hard_lvl, hard_lvl_mouse)
        self.back_button = Button(game_display, 10, 10, 56, 56, back_img)

    def create_window(self):
        game_display.blit(back_select_game, (0, 0))
        self.easy.draw_button()
        self.normal.draw_button()
        self.hard.draw_button()
        self.back_button.draw_button()

    def select(self):
        self.easy.click(self.set_level_easy)
        self.normal.click(self.set_level_normal)
        self.hard.click(self.set_level_hard)
        self.back_button.click(self.close_)

    def set_level_easy(self):
        global current_level, difficult
        current_level = EASY
        difficult = False

    def set_level_normal(self):
        global current_level, difficult
        current_level = NORMAL
        difficult = False

    def set_level_hard(self):
        global current_level, difficult
        current_level = HARD
        difficult = False

    def close_(self):
        global global_play, difficult
        difficult = False
        global_play = False


class MultiplicationTable:
    def __init__(self):
        super().__init__()
        self.back_button = Button(game_display, 10, 10, 56, 56, back_img)
        self.replay_button = Button(game_display, 135, 300, 56, 56, replay_img)
        self.expressions = []
        self.result = []
        self.couples = []
        self.couple = 0
        self.first_couple = ()
        self.second_couple = ()
        self.image = None
        self.flag = True

    def create_window(self):
        game_display.fill((168, 228, 160))
        self.back_button.draw_button()

    def create_lvl(self):
        self.flag = True
        con = sqlite3.connect('game_db.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT expression, result FROM multiplication
                                WHERE difficulty = (?)""", (current_level,)).fetchall()
        con.close()
        if current_level == EASY:
            self.image = math_lvl1
        elif current_level == NORMAL:
            self.image = math_lvl2
        elif current_level == HARD:
            self.image = math_lvl3
        exps = sample(result, 12)
        for i in exps:
            self.expressions.append(i[0])
            self.expressions.append(i[1])
        card_x = 160
        card_y = 40
        card_widht = 60
        card_height = 90
        for i in range(4):
            for j in range(6):
                card = Card(game_display, card_x, card_y, card_widht, card_height, self.image)
                card.draw_card()
                exp = choice(self.expressions)
                a = self.expressions.pop(self.expressions.index(exp))
                self.couples.append((a, card_x, card_y, card_widht, card_height))
                card_x += card_widht + 20
            card_x = 160
            card_y += card_height + 20

    def check_cards(self):
        global played_math
        cort = self.couples
        mouse = pygame.mouse.get_pos()
        self.back_button.click(self.close_)
        if cort:
            for i in cort:
                if (i[1] < mouse[0] < i[1] + i[3]) and (i[2] < mouse[1] < i[2] + i[4]):
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            self.turn_over(i[0], i[1], i[2], i[3], i[4])
        else:
            game_display.blit(event_img, (100, 100))
            to_write(game_display, 'Вы выиграли.', 325, 120)
            to_write(game_display, 'Получено ' + str(COINS) + ' денег.', 325, 150)
            self.replay_button.draw_button()
            self.replay_button.click(self.replay)
            if self.flag:
                self.add_coins(COINS)
                played_math = True
                self.flag = False

    def turn_over(self, name, x, y, widht, height):
        size = 20
        if self.couple == 0:
            pygame.draw.rect(game_display, (255, 255, 255), (x, y, widht, height))
            self.first_couple = (name, x, y, widht, height)
            x_cord = x + widht // 2 - 10
            if current_level == 2:
                x_cord -= 10
            if '*' in name:
                x_cord -= 10
                if current_level == 2:
                    x_cord += 5
            elif len(name) >= 5:
                size -= 7
                x_cord -= 20
            to_write(game_display, name, x_cord, y + height // 3, size)
            self.couple += 1
        elif self.couple == 1:
            pygame.draw.rect(game_display, (255, 255, 255), (x, y, widht, height))
            x_cord = x + widht // 2 - 10
            if current_level == 2:
                x_cord -= 10
            if '*' in name:
                x_cord -= 10
                if current_level == 2:
                    x_cord += 5
            elif len(name) >= 5:
                size -= 7
                x_cord -= 20
            to_write(game_display, name, x_cord, y + height // 3, size)
            pygame.display.update()
            self.second_couple = (name, x, y, widht, height)
            self.couple += 1

        if self.couple == 2:
            pygame.time.delay(1000)
            self.check_couple(widht, height)
            self.couple = 0

    def check_couple(self, widht, height):
        f = self.first_couple[0]
        s = self.second_couple[0]
        flag = False
        if '*' in f and '*' not in s:
            if eval(f) == int(s):
                self.couples.pop(self.couples.index(self.first_couple))
                self.couples.pop(self.couples.index(self.second_couple))
            else:
                flag = True
        elif '*' in s and '*' not in f:
            if eval(s) == int(f):
                self.couples.pop(self.couples.index(self.first_couple))
                self.couples.pop(self.couples.index(self.second_couple))
            else:
                flag = True
        else:
            flag = True

        if flag:
            image = pygame.transform.scale(self.image, (widht, height))
            game_display.blit(image, (self.first_couple[1], self.first_couple[2]))
            game_display.blit(image, (self.second_couple[1], self.second_couple[2]))
            self.first_couple = ()
            self.second_couple = ()

    def add_coins(self, quantity):
        con = sqlite3.connect('game_db.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT coins
                                FROM user_inf""").fetchall()
        for elem in result:
            cur.execute("""UPDATE user_inf
                            SET coins = (?),
                            last_math = (?),
                            last_math_date = (?)""",
                        (int(elem[0]) + quantity, 1, dt.date.today()))
            con.commit()
        con.close()

    def replay(self):
        self.create_window()
        self.create_lvl()

    def close_(self):
        global global_play
        global_play = False
        pygame.mixer.music.unpause()


class VocabularyWords:
    def __init__(self):
        self.back_button = Button(game_display, 10, 10, 56, 56, back_img)
        self.replay_button = Button(game_display, 135, 300, 56, 56, replay_img)
        self.erase = Button(game_display, 678, 10, 112, 48, eraser_img)
        self.check_button = Button(game_display, 734, 68, 56, 56, color=(150, 200, 100))
        self.alphabet = [['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й'],
                         ['к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф'],
                         ['х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']]
        self.keybord = []
        self.word_number = 0
        self.current_word = ''
        self.current_img = None
        self.words = []
        self.word = ''
        self.change_img_flag = True
        self.flag = True

    def create_window(self):
        game_display.fill((255, 200, 100))
        self.back_button.draw_button()
        self.erase.draw_button()
        self.check_button.draw_button()
        card_x = 20
        card_y = 264
        card_widht = 60
        card_height = 70
        for i in range(3):
            for j in range(11):
                card = Card(game_display, card_x, card_y, card_widht,
                            card_height, color=(randint(100, 255), randint(100, 255), randint(100, 255)))
                card.draw_card()
                to_write(game_display, self.alphabet[i][j], card_x + card_widht // 3,
                         card_y + card_height // 4, size=30)
                self.keybord.append((self.alphabet[i][j], card_x, card_y, card_widht, card_height))
                card_x += card_widht + 10
            card_x = 20
            card_y += card_height + 10

    def create_level(self):
        con = sqlite3.connect('game_db.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT word, image_path FROM vocabulary_words
                                WHERE difficulty = (?)""", (current_level,)).fetchall()  # current_level
        con.close()
        self.words = sample(result, 5)
        self.init_level()

    def change_letters(self):
        self.erase.click(self.erase_last_letter)
        self.back_button.click(self.close_)
        self.check_button.click(self.check)
        mouse = pygame.mouse.get_pos()
        for i in self.keybord:
            if (i[1] < mouse[0] < i[1] + i[3]) and (i[2] < mouse[1] < i[2] + i[4]):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.word += i[0]
                        self.create_window()
        if self.change_img_flag:
            game_display.blit(self.current_img, (300, 0))
        to_write(game_display, self.word, 400 - len(self.word) * 10, 210, size=40)

    def init_level(self):
        global played_rus
        if self.word_number != len(self.words):
            self.current_word = self.words[self.word_number][0]
            self.current_img = pygame.image.load(self.words[self.word_number][1])
            game_display.blit(self.current_img, (300, 0))
        else:
            game_display.blit(event_img, (100, 100))
            to_write(game_display, 'Вы выиграли.', 325, 120)
            to_write(game_display, 'Получено ' + str(COINS) + ' денег.', 325, 150)
            self.replay_button.draw_button()
            self.replay_button.click(self.replay)
            self.change_img_flag = False
            if self.flag:
                self.add_coins(COINS)
                played_rus = True
                self.flag = False

    def check(self):
        if self.current_word == self.word:
            self.word_number += 1
            self.word = ''
            self.create_window()
            self.init_level()
        else:
            pygame.draw.rect(game_display, (255, 150, 150), (20, 200, 56, 56))

    def erase_last_letter(self):
        self.word = self.word[:-1]
        self.create_window()
        to_write(game_display, self.word, 400 - len(self.word) * 10, 210, size=40)

    def add_coins(self, quantity):
        con = sqlite3.connect('game_db.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT coins
                                FROM user_inf""").fetchall()
        for elem in result:
            cur.execute("""UPDATE user_inf
                            SET coins = (?),
                            last_rus = (?),
                            last_rus_date = (?)""",
                        (int(elem[0]) + quantity, 1, dt.date.today()))
            con.commit()
        con.close()

    def replay(self):
        self.create_window()
        self.create_level()

    def close_(self):
        global global_play
        global_play = False
        pygame.mixer.music.unpause()


class House:
    def __init__(self):
        self.back_button = Button(game_display, 10, 10, 56, 56, back_img)

    def create_window(self):
        game_display.blit(back_home, (0, 0))
        self.back_button.draw_button()

    def live(self):
        game_display.blit(back_home, (0, 0))
        self.back_button.draw_button()
        for anim in animal_list:
            anim[0].animation()
        self.animal_touch()
        self.back_button.click(self.close_)

    def animal_touch(self):
        mouse = pygame.mouse.get_pos()
        for anim in animal_list:
            if ((anim[1][0] < mouse[0] < anim[1][0] + anim[1][2]) and
                    (anim[1][1] < mouse[1] < anim[1][1] + anim[1][3])):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        animal_act = AnimalsWindow(anim[0], anim[1][4])
                        self.animal_actions(animal_act, anim[0])

    def animal_actions(self, animal, animatic):
        global feed
        feed = True
        while feed:
            clock.tick(FPS)
            animal.create_window()
            animatic.animation(300, 100)
            animal.live()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
        self.create_window()

    def check_played(self):
        self.back_button.click(self.close_)
        if (not played_math or not played_rus) and animal_list:
            events.trigger_notplayed_event(played_math, played_rus)
        else:
            self.live()

    def close_(self):
        global global_play
        global_play = False
        pygame.mixer.music.load('Music\\main_selecting.wav')
        pygame.mixer.music.play(-1)


class AnimalsWindow:
    def __init__(self, animal, animal_code):
        self.back_button = Button(game_display, 0, 25, 56, 56, back_img)
        self.feed_button = Button(game_display, 372, 454, 56, 32, bowl_img)
        self.animal = animal
        self.animal_code = animal_code
        self.msg = ''

    def create_window(self):
        game_display.fill((200, 200, 200))
        pygame.draw.rect(game_display, (175, 175, 175), (0, 0, 800, 25))
        pygame.draw.rect(game_display, (175, 175, 175), (0, 404, 800, 100))
        self.feed_button.draw_button()
        self.back_button.draw_button()
        con = sqlite3.connect('game_db.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT count_food FROM food_type
                                WHERE food_type_id = (SELECT food_type_id FROM animals
                                                    WHERE animal_code = (?))""",
                             (self.animal_code,)).fetchall()
        con.close()
        to_write(game_display, 'Количество корма: ' + str(result[0][0]), 25, 425)

    def live(self):
        self.back_button.click(self.close_)
        self.feed_button.click(self.feed_act)
        to_write(game_display, self.msg, 325, 252)

    def feed_act(self):
        con = sqlite3.connect('game_db.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT count_food FROM food_type
                                WHERE food_type_id = (SELECT food_type_id FROM animals
                                                    WHERE animal_code = (?))""",
                             (self.animal_code,)).fetchall()
        for count in result:
            if int(count[0]) == 0:
                self.msg = 'У Вас нет корма.'
            else:
                cur.execute("""UPDATE animals SET last_time_food = (?)
                                WHERE animal_code = (?)""",
                            (dt.datetime.today(), self.animal_code)).fetchall()
                cur.execute("""UPDATE food_type SET count_food = (?)
                                WHERE food_type_id = (SELECT food_type_id FROM animals
                                                    WHERE animal_code = (?))""",
                            (int(count[0]) - 1, self.animal_code)).fetchall()
                con.commit()
                self.msg = ''
                pygame.draw.rect(game_display, (193, 0, 32), (425, 50, 56, 56))
                pygame.display.update()
                pygame.time.delay(50)
        con.close()

    def close_(self):
        global feed
        feed = False


class Shop:
    def __init__(self):
        self.animal_section = Button(game_display, 76, 10, 352, 56, color=(100, 100, 100))
        self.food_section = Button(game_display, 438, 10, 352, 56, color=(100, 100, 100))
        self.back_button = Button(game_display, 10, 10, 56, 56, back_img)
        self.buy = Button(game_display, 120, 330, 104, 56, color=(200, 200, 200))
        self.cancel = Button(game_display, 576, 330, 104, 56, color=(200, 200, 200))
        self.section = shop_animal
        self.shop_animals_card = []
        self.shop_food_card = []
        self.buy.set_clicked(False)
        self.cancel.set_clicked(False)
        self.section_flag = ANIMAL_SECTION
        self.money = 0
        self.cost = 0
        self.count_food = 0
        self.item_name = ''
        self.type = None

    def create_window(self):
        game_display.fill((225, 225, 225))
        self.animal_section.draw_button()
        self.food_section.draw_button()
        self.back_button.draw_button()
        self.draw_cards(self.section)
        to_write(game_display, 'животные', 76, 10)
        to_write(game_display, 'корм', 438, 10)

    def select(self):
        self.animal_section.click(self.set_animal)
        self.food_section.click(self.set_food)
        self.back_button.click(self.close_)
        self.click_card()
        self.buy.click(self.buy_item)
        self.cancel.click(self.leave_item)

    def set_animal(self):
        self.section = shop_animal
        self.section_flag = ANIMAL_SECTION
        self.create_window()

    def set_food(self):
        self.section = shop_food
        self.section_flag = FOOD_SECTION
        self.create_window()

    def draw_cards(self, section):
        game_display.fill((225, 225, 225))
        self.animal_section.draw_button()
        self.food_section.draw_button()
        self.back_button.draw_button()
        x = 20
        y = 88
        w = 136
        h = 150
        for elem in range(len(section)):
            if self.is_already_bought(section[elem][1]):
                card = Card(game_display, x, y, w, h, color=(255, 255, 255))
                card.draw_card()
                if section == shop_animal:
                    self.shop_animals_card.append((section[elem][1], x, y, w, h, section[elem][0]))
                elif section == shop_food:
                    self.shop_food_card.append((section[elem][1], x, y, w, h, section[elem][0]))
                image = pygame.transform.scale(section[elem][0], (w, h - 20))
                game_display.blit(image, (x, y + 10))
                pygame.display.update()
                x += w + 20
        pygame.draw.rect(game_display, (175, 175, 175), (0, 475, 800, 29))
        pygame.display.update()

    def click_card(self):
        cort = []
        if self.section == shop_animal:
            cort = self.shop_animals_card
        elif self.section == shop_food:
            cort = self.shop_food_card
        mouse = pygame.mouse.get_pos()
        for i in cort:
            if (i[1] < mouse[0] < i[1] + i[3]) and (i[2] < mouse[1] < i[2] + i[4]):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.type = i[0]
                        self.discover_cost()
                        self.confirm_purchase(i)

    def confirm_purchase(self, what_buy):
        pygame.draw.rect(game_display, (78, 78, 128), (100, 100, 600, 304))
        image = pygame.transform.scale(what_buy[5], (what_buy[3], what_buy[4] - 20))
        game_display.blit(image, (110, 110))
        m = ''
        if self.section_flag == FOOD_SECTION:
            m = 'Корм для '
        to_write(game_display, m + self.item_name, 100 + what_buy[3] + 50, 110)
        to_write(game_display, 'Цена: ' + str(self.cost), 100 + what_buy[3] + 50, 135)
        to_write(game_display, 'У Вас есть: ' + str(self.money), 100 + what_buy[3] + 50, 160)
        self.type = what_buy[0]
        self.buy.draw_button()
        self.cancel.draw_button()
        self.animal_section.set_clicked(False)
        self.food_section.set_clicked(False)
        self.back_button.set_clicked(False)
        self.buy.set_clicked(True)
        self.cancel.set_clicked(True)

    def buy_item(self):
        flag = True
        con = sqlite3.connect('game_db.sqlite')
        cur = con.cursor()
        if self.section_flag == ANIMAL_SECTION:
            if self.money >= self.cost:
                cur.execute("""UPDATE animals
                                SET bought = (?)""",
                            (1,))
                cur.execute("""UPDATE user_inf
                                SET coins = (?)""",
                            (self.money - self.cost,))
                con.commit()
            else:
                to_write(game_display, 'У Вас не хватает денег.', 110, 275)
                flag = False

        elif self.section_flag == FOOD_SECTION:
            if self.money >= self.cost:
                cur.execute("""UPDATE food_type
                                SET count_food = (?)""",
                            (self.count_food + 1,))
                cur.execute("""UPDATE user_inf
                                SET coins = (?)""",
                            (self.money - self.cost,))
                con.commit()
            else:
                to_write(game_display, 'У Вас не хватает денег.', 110, 275)
                flag = False
        con.close()
        self.draw_cards(self.section)

        if flag:
            self.animal_section.set_clicked(True)
            self.food_section.set_clicked(True)
            self.back_button.set_clicked(True)
            self.buy.set_clicked(False)
            self.cancel.set_clicked(False)
            self.create_window()

    def leave_item(self):
        self.animal_section.set_clicked(True)
        self.food_section.set_clicked(True)
        self.back_button.set_clicked(True)
        self.buy.set_clicked(False)
        self.cancel.set_clicked(False)
        self.create_window()

    def discover_cost(self):
        con = sqlite3.connect('game_db.sqlite')
        cur = con.cursor()
        cost_and_id = (None, None)
        name = ''
        money = cur.execute("""SELECT coins FROM user_inf""").fetchall()
        if self.section_flag == ANIMAL_SECTION:
            cost_and_id = cur.execute("""SELECT cost, bought FROM animals
                                    WHERE animal_code = (?)""", (self.type,)).fetchall()
            name = cur.execute("""SELECT name FROM animals
                                    WHERE animal_code = (?)""", (self.type,)).fetchall()
        elif self.section_flag == FOOD_SECTION:
            cost_and_id = cur.execute("""SELECT cost, count_food FROM food_type
                                        WHERE food_type_id = (?)""",
                                      (int(self.type),)).fetchall()
            name = cur.execute("""SELECT for FROM food_type
                                    WHERE food_type_id = (?)""",
                               (int(self.type),)).fetchall()
        con.close()
        self.money = int(money[0][0])
        self.cost = int(cost_and_id[0][0])
        self.count_food = cost_and_id[0][1]
        self.item_name = name[0][0]

    def is_already_bought(self, code):
        try:
            con = sqlite3.connect('game_db.sqlite')
            cur = con.cursor()
            already_bought = cur.execute("""SELECT bought FROM animals
                                            WHERE animal_code = (?)""",
                                         (code,)).fetchall()
            con.close()
            if int(already_bought[0][0]) == 0:
                return True
            return False
        except:
            return True

    def close_(self):
        global global_play
        global_play = False


def change_coins_quality():
    global COINS
    if current_level == EASY:
        COINS = 10
    elif current_level == NORMAL:
        COINS = 20
    elif current_level == HARD:
        COINS = 30


def check():
    global played_math, played_rus

    con = sqlite3.connect('game_db.sqlite')
    cur = con.cursor()
    result = cur.execute("""SELECT last_time_food, animal_code
                            FROM animals
                            WHERE bought = 1""").fetchall()
    for elem in result:
        if dt.datetime.strptime(elem[0], '%Y-%m-%d %H:%M:%S.%f') < dt.datetime.today() - dt.timedelta(hours=24):
            cur.execute("""UPDATE animals
                            SET bought = (?)
                            WHERE animal_code = (?)""", (0, elem[1]))
            con.commit()

    result = cur.execute("""SELECT last_math, last_rus,
                                    last_math_date, last_rus_date
                            FROM user_inf""").fetchall()
    for elem in result:
        if dt.datetime.strptime(elem[2], '%Y-%m-%d') == dt.datetime.strptime(elem[3], '%Y-%m-%d'):
            if dt.datetime.strptime(elem[2], '%Y-%m-%d') == dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d'):
                played_math = True
                played_rus = True
            else:
                played_math = False
                played_rus = False
        else:
            if dt.datetime.strptime(elem[2], '%Y-%m-%d') < dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d'):
                played_math = False
            else:
                played_math = True
            if dt.datetime.strptime(elem[3], '%Y-%m-%d') < dt.datetime.strptime(str(dt.date.today()), '%Y-%m-%d'):
                played_rus = False
            else:
                played_rus = True
    con.close()


def animal_init():
    con = sqlite3.connect('game_db.sqlite')
    cur = con.cursor()
    result = cur.execute("""SELECT last_time_food, animal_code, widht, height
                            FROM animals
                            WHERE bought = 1""").fetchall()
    for elem in result:
        x = randint(0, 800 - int(elem[2]))
        if x >= 518 - int(elem[2]):
            y = randint(324, 500 - int(elem[3]))
        else:
            y = randint(300, 500 - int(elem[3]))
        anim = Animal(game_display, animal_sprites_dict[elem[1]], x, y)
        animal_list.append((anim, (x, y, int(elem[2]), int(elem[3]), elem[1])))
    con.close()


FPS = 60
global_play = True
difficult = True
feed = True
pygame.init()
game_display = pygame.display.set_mode((800, 504))
clock = pygame.time.Clock()
pygame.mixer.music.load('Music\\main_selecting.wav')
pygame.mixer.music.play(-1)
events = Event(game_display)
animal_list = []
ANIMAL_SECTION = 'ANIMAL'
FOOD_SECTION = 'FOOD'
EASY = 1
NORMAL = 2
HARD = 3
COINS = 0
current_level = None
played_math = None
played_rus = None


def main(main_wnd):
    global game_display
    main_wnd.create_window()
    while True:
        clock.tick(FPS)
        main_wnd.selecting()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


if __name__ == '__main__':
    check()
    animal_init()
    main_wnd = MainWindow()
    main(main_wnd)
