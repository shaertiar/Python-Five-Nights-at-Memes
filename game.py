import pygame as pg
import json
import random

# Иниацилизация
pg.init()

# Функция перевода
def translate(text, language):
    # Словарь со словами
    translate_ru = {
        'New game': 'Новая игра',
        'Continue': 'Продолжить',
        'Settings': 'Настройки'
    }

# Класс игры
class Game:
    # Конструктор
    def __init__(self, window):
        self.window = window
        self.stage = 'menu'
        self.language = json.load(open(r'settings.json', 'r'))['Language']
        self.menu_display = MenuDisplay(self.window)
        self.settings_display = SettingDisplay(self.window, self.language)
        self.backstory = BackStory(self.window)
        self.game_play = GamePlay(self.window)
        self.music_volume = 100
        self.effects_volume = 100

    # Функция отображения экранов
    def draw(self):
        if self.stage == 'menu':
            self.menu_display.draw()

        elif self.stage == 'settings':
            self.settings_display.draw(self.music_volume, self.effects_volume)

        elif self.stage == 'backstory':
            self.backstory.draw()

        elif self.stage == 'gameplay':
            self.game_play.draw()

        if self.backstory.is_next_stage == True:
            self.stage = 'gameplay'

    # Функция обработки нажатий клавиш
    def pressed_on(self, key):
        if self.stage == 'backstory':
            if key == pg.K_ESCAPE:
                self.backstory.skip()

    # Функция обработки нажатия мыши
    def clicked_on(self, mouse_pos):
        if self.stage == 'menu':
            button_num = 0
            for button in self.menu_display.buttons:
                if self.menu_display.buttons[button].collidepoint(mouse_pos[0], mouse_pos[1]):
                    click_sound = pg.mixer.Sound(r'sound\Click.mp3')
                    pg.mixer.Channel(1).play(click_sound)

                    # Нажатие на "New game"
                    if button_num == 0:
                        self.stage = 'backstory'
                        self.backstory.start_music()

                    # Нажатие на "Continue"
                    elif button_num == 1:
                        self.stage = 'gameplay'

                    # Нажатие на "Settings"
                    elif button_num == 2:
                        self.stage = 'settings'

                    break

                button_num += 1

        elif self.stage == 'settings':
            button_num = 0
            for button in self.settings_display.buttons:
                if self.settings_display.buttons[button].collidepoint(mouse_pos[0], mouse_pos[1]):
                    click_sound = pg.mixer.Sound(r'sound\Click.mp3')
                    pg.mixer.Channel(1).play(click_sound)

                    # Нажатие на "Back"
                    if button_num == 0:
                        self.stage = 'menu'

                    # Нажатие на "+ add music volume"
                    elif button_num == 1:
                        if self.music_volume <= 95:
                            self.music_volume = int(self.music_volume + 5)
                            pg.mixer.Channel(0).set_volume(self.music_volume/100)

                    # Нажатие на "- remove music volume"
                    elif button_num == 2:
                        if self.music_volume >= 5:
                            self.music_volume = int(self.music_volume - 5)
                            pg.mixer.Channel(0).set_volume(self.music_volume/100)

                    # Нажатие на "+ add effects volume"
                    elif button_num == 3:
                        if self.effects_volume <= 95:
                            self.effects_volume = int(self.effects_volume + 5)
                            pg.mixer.Channel(1).set_volume(self.effects_volume/100)

                    # Нажатие на "- remove effects volume"
                    elif button_num == 4:
                        if self.effects_volume >= 5:
                            self.effects_volume = int(self.effects_volume - 5)
                            pg.mixer.Channel(1).set_volume(self.effects_volume/100)

                    # Нажатие на "en" \ "ru" 
                    # elif button_num == 5:
                    #     self.settings_display.change_language()
                    #     self.language = self.settings_display.language

                    break

                button_num += 1

# Класс меню
class MenuDisplay:
    # Конструктор
    def __init__(self, window):
        self.window = window
        self.title_font = pg.font.SysFont('couriernew', 75)
        self.buttons_font = pg.font.SysFont('couriernew', 50)
        self.subtitles_font = pg.font.SysFont('consolas', 14)
        self.buttons = {
            self.buttons_font.render('New game', True, (255, 0, 0)): pg.rect.Rect(50, 160, 240, 57),
            self.buttons_font.render('Continue', True, (255, 0, 0)): pg.rect.Rect(50, 257, 240, 57),
            self.buttons_font.render('Settings', True, (255, 0, 0)): pg.rect.Rect(50, 354, 240, 57),
        }
        # Запуск эмбиента
        ambient = pg.mixer.Sound(r'sound\Ambient.mp3')
        pg.mixer.Channel(0).play(ambient, -1)

    # Функция отображения
    def draw(self):
        self.window.blit(pg.transform.scale(pg.image.load(f'img\white noise BG{random.randint(1, 12)}.jpg'), (1200, 800)), (0, 0))
        self.window.blit(self.title_font.render('Five Night\'s at Memes', True, (255, 0, 0)), (50, 50))
        for button in self.buttons:
            self.window.blit(button, (self.buttons[button].x, self.buttons[button].y))
        self.window.blit(self.subtitles_font.render('Made by Shaertiar', True, (255, 255, 255)), (6, 780))
        self.window.blit(pg.transform.scale(pg.image.load(r'img\Freddy Fazbear main.png'), (800, 800)), (400, 200))

# Класс настроек
class SettingDisplay:
    # Конструктор
    def __init__(self, window, language):
        self.window = window
        self.language = language
        self.buttons_font = pg.font.SysFont('couriernew', 50)
        self.buttons = {
            self.buttons_font.render('Back', True, (255, 255, 255), (255, 0, 0)): pg.rect.Rect(0, 0, 120, 57),
            self.buttons_font.render('+ add music volume', True, (255, 0, 0)): pg.rect.Rect(50, 107, 540, 57),
            self.buttons_font.render('- remove music volume', True, (255, 0, 0)): pg.rect.Rect(50, 164, 630, 57),
            self.buttons_font.render('+ add effects volume', True, (255, 0, 0)): pg.rect.Rect(50, 304, 600, 57),
            self.buttons_font.render('- remove effects volume', True, (255, 0, 0)): pg.rect.Rect(50, 361, 690, 57),
            self.buttons_font.render('In developing', True, (255, 0, 0)): pg.rect.Rect(50, 500, 60, 57)
        }

    # Функция отображения
    def draw(self, music_volume, effects_volume):
        self.window.blit(pg.transform.scale(pg.image.load(f'img\white noise BG{random.randint(1, 12)}.jpg'), (1200, 800)), (0, 0))
        self.window.blit(self.buttons_font.render(f'Music volume ({music_volume}%{"min" if music_volume < 5 else "max" if music_volume > 95 else ""})', True, (255, 0, 0)), (50, 50))
        self.window.blit(self.buttons_font.render(f'Effects volume ({effects_volume}%{"min" if effects_volume < 5 else "max" if effects_volume > 95 else ""})', True, (255, 0, 0)), (50, 246))
        self.window.blit(self.buttons_font.render('Language', True, (255, 0 ,0)), (50, 443))
        for button in self.buttons:
            self.window.blit(button, (self.buttons[button].x, self.buttons[button].y))

    # Функция изменения языка
    def change_language(self):
        if self.language == 'en': self.language = 'ru'
        elif self.language == 'ru': self.language = 'en'

        self.buttons = {
            self.buttons_font.render('Back', True, (255, 255, 255), (255, 0, 0)): pg.rect.Rect(0, 0, 120, 57),
            self.buttons_font.render('+ add music volume', True, (255, 0, 0)): pg.rect.Rect(50, 107, 540, 57),
            self.buttons_font.render('- remove music volume', True, (255, 0, 0)): pg.rect.Rect(50, 164, 630, 57),
            self.buttons_font.render('+ add effects volume', True, (255, 0, 0)): pg.rect.Rect(50, 304, 600, 57),
            self.buttons_font.render('- remove effects volume', True, (255, 0, 0)): pg.rect.Rect(50, 361, 690, 57),
            self.buttons_font.render(self.language, True, (255, 0, 0)): pg.rect.Rect(50, 500, 60, 57)
        }

# Класс предистории
class BackStory:
    # Конструктор
    def __init__(self, window):
        self.window = window
        self.text_font = pg.font.SysFont('couriernew', 35)
        self.subtitles_font = pg.font.SysFont('couriernew', 25)
        self.is_next_stage = False
        self.frames = 360

    # Функция отображения
    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.subtitles_font.render('Press "Esc" to continue', True, (255, 255, 255)), (0, 0))
        self.window.blit(self.text_font.render('After watching the FNaF movie, I decided to scroll', True, (255, 255, 255)), (50, 50))
        self.window.blit(self.text_font.render('through my social network feed and suddenly passed', True, (255, 255, 255)), (50, 90))
        self.window.blit(self.text_font.render('out... I woke up in this strange office...', True, (255, 255, 255)), (50, 130))

        self.frames -= 1

        if self.frames <= 0:
            self.skip()

    # Функция продолжения
    def skip(self):
        self.is_next_stage = True

    # функция запуска музыки
    def start_music(self):
        # Запуск музыки
        music = pg.mixer.Sound(r'sound\Backstory.mp3')
        pg.mixer.Channel(0).play(music)

# Класс игры
class GamePlay:
    # Конструктор
    def __init__(self, window):
        self.window = window
        self.stage = 'office'
        self.office = ...
        self.screen = ...

    # Функция отображения
    def draw(self):
        if self.stage == 'office':
            self.office.draw()

        elif self.stage == 'screen':
            self.screen.draw()

if __name__ == '__main__':
    pg.init()

    print(pg.font.get_fonts())

    # ⟰ ⟱
    # ⮝ ⮟