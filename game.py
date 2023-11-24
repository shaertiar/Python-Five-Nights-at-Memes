import pygame as pg
import json
import random
from translator import *

# Иниацилизация
pg.init()

# функция изменения настроек
def settings_change(change, to):
    settings = json.load(open(r'settings.json', 'r'))
    settings[change] = to
    json.dump(settings, open(r'settings.json', 'w'))

# Класс игры
class Game:
    # Конструктор
    def __init__(self, window):
        self.window = window
        self.stage = 'menu'
        self.settings = json.load(open(r'settings.json', 'r'))
        self.language = self.settings['Language']
        self.current_night = self.settings['Current night']
        self.menu_display = MenuDisplay(self.window, self.current_night, self.language)
        self.settings_display = SettingDisplay(self.window, self.language)
        self.backstory_display = BackStoryDisplay(self.window, self.language)
        self.art_display = ArtDisplay(self.window)
        self.gameplay = GamePlay(self.window, self.language)
        self.music_volume = 100
        self.effects_volume = 100

        pg.mixer.Channel(0).set_volume(self.music_volume/100)
        pg.mixer.Channel(1).set_volume(self.effects_volume/100)

    # Функция отображения экранов
    def draw(self):
        if self.stage == 'menu':
            self.menu_display.draw()

        elif self.stage == 'settings':
            self.settings_display.draw(self.music_volume, self.effects_volume)

        elif self.stage == 'backstory':
            self.backstory_display.draw()

        elif self.stage == 'gameplay':
            self.gameplay.draw()

        elif self.stage == 'art':
            self.art_display.draw()

        if self.art_display.is_next_stage == True:
            self.stage = 'gameplay'
            self.gameplay.start_music()
            self.art_display = ArtDisplay(self.window)

        if self.backstory_display.is_next_stage == True:
            self.stage = 'art'
            self.backstory_display = BackStoryDisplay(self.window, self.language)

        if self.settings_display.is_restart:
            self.settings = json.load(open(r'settings.json', 'r'))
            self.language = self.settings['Language']
            self.current_night = self.settings['Current night']
            self.menu_display = MenuDisplay(self.window, self.current_night, self.language)
            self.settings_display = SettingDisplay(self.window, self.language)
            self.backstory_display = BackStoryDisplay(self.window, self.language)
            self.art_display = ArtDisplay(self.window)
            self.gameplay = GamePlay(self.window, self.language)

        if self.gameplay.stage == 'menu':
            self.gameplay = GamePlay(self.window, self.language)
            self.stage = 'menu'
            self.menu_display.start_music()
            self.settings = json.load(open(r'settings.json', 'r'))
            self.current_night = self.settings['Current night']
            self.menu_display.current_night = self.current_night

    # Функция обработки нажатий клавиш
    def pressed_on(self, key):
        if self.stage == 'backstory':
            if key == pg.K_ESCAPE:
                self.backstory_display.skip()

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
                        self.backstory_display.start_music()

                    # Нажатие на "Continue"
                    elif button_num == 1:
                        self.stage = 'art'
                        self.gameplay.start_music()

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
                    elif button_num == 5:
                        self.settings_display.change_language()
                        self.language = self.settings_display.language

                    break

                button_num += 1

        elif self.stage == 'gameplay':
            self.gameplay.clicked_on(mouse_pos)

# Класс меню
class MenuDisplay:
    # Конструктор
    def __init__(self, window, current_night, language):
        self.window = window
        self.language = language
        self.current_night = current_night
        self.title_font = pg.font.SysFont('couriernew', 75)
        self.buttons_font = pg.font.SysFont('couriernew', 50)
        self.subtitles_font = pg.font.SysFont('consolas', 14)
        self.buttons = {
            self.buttons_font.render(translate_text('New game', self.language), True, (255, 0, 0)): translate_objects('New game', self.language),
            self.buttons_font.render(translate_text('Continue', self.language), True, (255, 0, 0)): translate_objects('Continue', self.language),
            self.buttons_font.render(translate_text('Settings', self.language), True, (255, 0, 0)): translate_objects('Settings', self.language),
        }
        self.start_music()

    # Функция отображения
    def draw(self):
        self.window.blit(pg.transform.scale(pg.image.load(f'img\white noise BG{random.randint(1, 12)}.jpg'), (1200, 800)), (0, 0))
        self.window.blit(self.title_font.render(translate_text('Five Night\'s at Memes', self.language), True, (255, 0, 0)), (50, 50))
        self.window.blit(self.buttons_font.render(f' ({str(self.current_night)})', True, (255, 0, 0)), translate_objects('Continue night', self.language))
        self.window.blit(self.subtitles_font.render(translate_text('Made by Shaertiar (Alpha 0.5.1)', self.language), True, (255, 255, 255)), (6, 780))
        self.window.blit(pg.transform.scale(pg.image.load(r'img\Freddy Fazbear main.png'), (800, 800)), (400, 200))
        for button in self.buttons:
            self.window.blit(button, (self.buttons[button].x, self.buttons[button].y))

    # функция запуска музыки
    def start_music(self):
        # Запуск эмбиента
        ambient = pg.mixer.Sound(r'sound\Ambient.mp3')
        pg.mixer.Channel(0).play(ambient, -1)

# Класс настроек
class SettingDisplay:
    # Конструктор
    def __init__(self, window, language):
        self.window = window
        self.language = language
        self.buttons_font = pg.font.SysFont('couriernew', 50)
        self.buttons = {
            self.buttons_font.render(translate_text('Back', self.language), True, (255, 255, 255), (255, 0, 0)): translate_objects('Back', self.language),
            self.buttons_font.render(translate_text('+ add music volume', self.language), True, (255, 0, 0)): translate_objects('+ add music volume', self.language),
            self.buttons_font.render(translate_text('- remove music volume', self.language), True, (255, 0, 0)): translate_objects('- remove music volume', self.language),
            self.buttons_font.render(translate_text('+ add effects volume', self.language), True, (255, 0, 0)): translate_objects('+ add effects volume', self.language),
            self.buttons_font.render(translate_text('- remove effects volume', self.language), True, (255, 0, 0)): translate_objects('- remove effects volume', self.language),
            self.buttons_font.render(self.language, True, (255, 0, 0)): pg.rect.Rect(50, 500, 60, 57)
        }
        self.is_restart = False

    # Функция отображения
    def draw(self, music_volume, effects_volume):
        self.window.blit(pg.transform.scale(pg.image.load(f'img\white noise BG{random.randint(1, 12)}.jpg'), (1200, 800)), (0, 0))
        self.window.blit(self.buttons_font.render(translate_text('Music volume', self.language), True, (255, 0, 0)), (50, 50))
        self.window.blit(self.buttons_font.render(translate_text('Effects volume', self.language), True, (255, 0, 0)), (50, 246))
        self.window.blit(self.buttons_font.render(f' ({music_volume}%{"min" if music_volume < 5 else "max" if music_volume > 95 else ""})', True, (255, 0, 0)), translate_objects('Music volume', self.language))
        self.window.blit(self.buttons_font.render(f' ({effects_volume}%{"min" if effects_volume < 5 else "max" if effects_volume > 95 else ""})', True, (255, 0, 0)), translate_objects('Effects volume', self.language))
        self.window.blit(self.buttons_font.render(translate_text('Language', self.language), True, (255, 0 ,0)), (50, 443))
        for button in self.buttons:
            self.window.blit(button, (self.buttons[button].x, self.buttons[button].y))

    # Функция изменения языка
    def change_language(self):
        if self.language == 'en': 
            self.language = 'ru'
        elif self.language == 'ru': 
            self.language = 'en'

        self.buttons = {
            self.buttons_font.render(translate_text('Back', self.language), True, (255, 255, 255), (255, 0, 0)): translate_objects('Back', self.language),
            self.buttons_font.render(translate_text('+ add music volume', self.language), True, (255, 0, 0)): translate_objects('+ add music volume', self.language),
            self.buttons_font.render(translate_text('- remove music volume', self.language), True, (255, 0, 0)): translate_objects('- remove music volume', self.language),
            self.buttons_font.render(translate_text('+ add effects volume', self.language), True, (255, 0, 0)): translate_objects('+ add effects volume', self.language),
            self.buttons_font.render(translate_text('- remove effects volume', self.language), True, (255, 0, 0)): translate_objects('- remove effects volume', self.language),
            self.buttons_font.render(self.language, True, (255, 0, 0)): pg.rect.Rect(50, 500, 60, 57)
        }

        settings_change('Language', self.language)

        self.is_restart = True

# Класс предистории
class BackStoryDisplay:
    # Конструктор
    def __init__(self, window, language):
        self.window = window
        self.language = language
        self.text_font = pg.font.SysFont('couriernew', 35)
        self.subtitles_font = pg.font.SysFont('couriernew', 25)
        self.is_next_stage = False
        self.frames = 360

    # Функция отображения
    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.subtitles_font.render(translate_text('Press "Esc" to continue', self.language), True, (255, 255, 255)), (0, 0))
        self.window.blit(self.text_font.render(translate_text('After watching the FNaF movie, I decided to scroll', self.language), True, (255, 255, 255)), (50, 50))
        self.window.blit(self.text_font.render(translate_text('through my social network feed and suddenly passed', self.language), True, (255, 255, 255)), (50, 79))
        self.window.blit(self.text_font.render(translate_text('out... I woke up in this strange office...', self.language), True, (255, 255, 255)), (50, 108))
        self.window.blit(self.text_font.render(translate_text('.', self.language), True, (255, 255, 255)), (50, 137))

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

# Класс слайда
class ArtDisplay:
    # Конструктор
    def __init__(self, window):
        self.window = window
        self.is_next_stage = False
        self.frames = 36

    # Функция отрисовки
    def draw(self):
        self.window.blit(pg.transform.scale(pg.image.load(r'img\Slide.png'), (1200, 800)), (0, 0))

        self.frames -= 1

        if self.frames <= 0:
            self.skip()

    # Функция продолжения
    def skip(self):
        self.is_next_stage = True

# Класс игрового процесса
class GamePlay:
    # Конструктор
    def __init__(self, window, language):
        self.window = window
        self.language = language
        self.stage = 'office'
        self.text_font = pg.font.Font(r'font\Segment16B Regular.ttf', 25)
        self.cam_font = pg.font.SysFont('consolas', 20)
        self.cam_small_font = pg.font.SysFont('consolas', 15)
        self.cam_num = 1
        self.is_cam_ventilation = False
        self.game_display = GameDisplay(self.window, self.language)
        self.win_display = WinDisplay(self.window)
        self.buttons = {
            self.text_font.render(f'{"Open":^86}', True, (255, 255, 255), (123, 0, 0)): pg.rect.Rect(0, 775, 1200, 25),
        }
        self.time = 4320

    # Функция отображения
    def draw(self):
        self.game_display.draw(self.stage, self.cam_num)
        
        # Если открыт экран
        if self.stage == 'display':
            # Если включена камера винтеляции
            if self.is_cam_ventilation:
                # Отображаем карту вентеляции
                self.window.blit(pg.transform.scale(pg.image.load(r'img\ventilation map.png'), (300, 300)), (900, 469))
                # Создаем кнопки вентеляции
                self.buttons = {
                    self.text_font.render(f'{"Close":^86}', True, (255, 255, 255), (123, 0, 0)): pg.rect.Rect(0, 775, 1200, 25),
                    self.cam_font.render(' V ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1120, 685, 42, 20),
                    self.cam_small_font.render(' 10', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1139, 735, 24, 15),
                    self.cam_small_font.render(' 11', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(957, 702, 24, 15),
                    self.cam_small_font.render(' 12', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1037, 740, 24, 15)
                }
            # Если камера вентеляции не включена
            else:
                # Отображаем обычную карту
                self.window.blit(pg.transform.scale(pg.image.load(r'img\map.png'), (300, 300)), (900, 469))
                # Создаем кнопки без вентеляции
                self.buttons = {
                    self.text_font.render(f'{"Close":^86}', True, (255, 255, 255), (123, 0, 0)): pg.rect.Rect(0, 775, 1200, 25),
                    self.cam_font.render(' V ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1120, 685, 42, 20),
                    self.cam_font.render(' 1 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1105, 484, 42, 20),
                    self.cam_font.render(' 2 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(972, 649, 42, 20),
                    self.cam_font.render(' 3 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1073, 627, 42, 20),
                    self.cam_font.render(' 4 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(990, 482, 42, 20),
                    self.cam_font.render(' 5 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(905, 628, 42, 20),
                    self.cam_font.render(' 6 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(971, 731, 42, 20),
                    self.cam_small_font.render(' 7 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(938, 654, 24, 15),
                    self.cam_small_font.render(' 8 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1050, 727, 24, 15),
                    self.cam_small_font.render(' 9 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1089, 727, 24, 15),
                }

            # Отображаем все нужные кнопки
            for button in self.buttons:
                self.window.blit(button, (self.buttons[button].x, self.buttons[button].y))

            # Отображение времени
            self.window.blit(self.text_font.render(f'{self.return_time()}', True, (255, 255, 255)), (0, 0))

        # Отображаем лишь кнопку открытия монитора
        elif self.stage == 'office':
            for button in self.buttons:
                self.window.blit(button, (self.buttons[button].x, self.buttons[button].y))
                break

            # Отображение времени
            self.window.blit(self.text_font.render(f'{self.return_time()}', True, (255, 255, 255)), (0, 0))

        # Отображение окна победы
        elif self.stage == 'win':
            self.win_display.draw()


        # Уменьшаем время (увеличиваем)
        self.time -= 1

        if self.time <= 0:
            self.time = 121
            if self.stage != 'over':
                self.stage = 'win'
                self.win_display.start_music()
                settings_change('Current night', json.load(open(r'settings.json', 'r'))['Current night']+1)

        if self.win_display.is_next_stage:
            self.win_display = WinDisplay(self.window)
            self.stage = 'menu'

    # Функция обработки нажатий мыши
    def clicked_on(self, mouse_pos):
        is_need_change = False

        button_num = 0
        for button in self.buttons:
            if self.buttons[button].collidepoint(mouse_pos[0], mouse_pos[1]):
                click_sound = pg.mixer.Sound(r'sound\Click3.mp3')
                pg.mixer.Channel(1).play(click_sound)

                # Нажатие на кнопку открытия монитора
                if button_num == 0:
                    if self.stage == 'office': 
                        # Звук нажатия
                        click_sound = pg.mixer.Sound(r'sound\Click2.mp3')
                        pg.mixer.Channel(1).play(click_sound)

                        self.stage = 'display'

                        is_need_change = True

                    elif self.stage == 'display':
                        # Звук нажатия
                        click_sound = pg.mixer.Sound(r'sound\Click2.mp3')
                        pg.mixer.Channel(1).play(click_sound)

                        self.stage = 'office'

                        is_need_change = True

                # Нажатие на кнопку отображения вентиляционной карты
                elif button_num == 1:
                    self.is_cam_ventilation = not self.is_cam_ventilation
                    # Звук нажатия
                    click_sound = pg.mixer.Sound(r'sound\Click4.mp3')
                    pg.mixer.Channel(1).play(click_sound)

                # Нажатие на камеру
                elif button_num == 2:
                    if self.is_cam_ventilation:
                        self.cam_num = 10
                    else:
                        self.cam_num = 1

                # Нажатие на камеру
                elif button_num == 3:
                    if self.is_cam_ventilation:
                        self.cam_num = 11
                    else:
                        self.cam_num = 2

                # Нажатие на камеру
                elif button_num == 4:
                    if self.is_cam_ventilation:
                        self.cam_num = 12
                    else:
                        self.cam_num = 3

                # Нажатие на камеру
                elif button_num == 4:
                    self.cam_num = 3

                # Нажатие на камеру 
                elif button_num == 5:
                    self.cam_num = 4

                # Нажатие на камеру
                elif button_num == 6:
                    self.cam_num = 5

                # Нажатие на камеру
                elif button_num == 7:
                    self.cam_num = 6

                # Нажатие на камеру
                elif button_num == 8:
                    self.cam_num = 7

                # Нажатие на камеру
                elif button_num == 9:
                    self.cam_num = 8

                # Нажатие на камеру
                elif button_num == 10:
                    self.cam_num = 9

            button_num += 1

        if is_need_change:
            if self.stage == 'office':
                if self.is_cam_ventilation:
                    self.buttons = {
                        self.text_font.render(f'{"Open":^86}', True, (255, 255, 255), (123, 0, 0)): pg.rect.Rect(0, 775, 1200, 25),
                        self.cam_font.render(' V ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1120, 685, 42, 20),
                        self.cam_small_font.render(' 10', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1139, 735, 24, 15),
                        self.cam_small_font.render(' 11', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(957, 702, 24, 15),
                        self.cam_small_font.render(' 12', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1037, 740, 24, 15)
                    }
                else:
                    self.buttons = {
                        self.text_font.render(f'{"Open":^86}', True, (255, 255, 255), (123, 0, 0)): pg.rect.Rect(0, 775, 1200, 25),
                        self.cam_font.render(' V ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1120, 685, 42, 20),
                        self.cam_font.render(' 1 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1105, 484, 42, 20),
                        self.cam_font.render(' 2 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(972, 649, 42, 20),
                        self.cam_font.render(' 3 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1073, 627, 42, 20),
                        self.cam_font.render(' 4 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(990, 482, 42, 20),
                        self.cam_font.render(' 5 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(905, 628, 42, 20),
                        self.cam_font.render(' 6 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(971, 731, 42, 20),
                        self.cam_small_font.render(' 7 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(938, 654, 24, 15),
                        self.cam_small_font.render(' 8 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1050, 727, 24, 15),
                        self.cam_small_font.render(' 9 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1089, 727, 24, 15),
                    }
            else:
                if self.is_cam_ventilation:
                    self.buttons = {
                        self.text_font.render(f'{"Close":^86}', True, (255, 255, 255), (123, 0, 0)): pg.rect.Rect(0, 775, 1200, 25),
                        self.cam_font.render(' V ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1120, 685, 42, 20),
                        self.cam_small_font.render(' 10', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1139, 735, 24, 15),
                        self.cam_small_font.render(' 11', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(957, 702, 24, 15),
                        self.cam_small_font.render(' 12', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1037, 740, 24, 15)
                    }
                else:
                    self.buttons = {
                        self.text_font.render(f'{"Close":^86}', True, (255, 255, 255), (123, 0, 0)): pg.rect.Rect(0, 775, 1200, 25),
                        self.cam_font.render(' V ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1120, 685, 42, 20),
                        self.cam_font.render(' 1 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1105, 484, 42, 20),
                        self.cam_font.render(' 2 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(972, 649, 42, 20),
                        self.cam_font.render(' 3 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1073, 627, 42, 20),
                        self.cam_font.render(' 4 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(990, 482, 42, 20),
                        self.cam_font.render(' 5 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(905, 628, 42, 20),
                        self.cam_font.render(' 6 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(971, 731, 42, 20),
                        self.cam_small_font.render(' 7 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(938, 654, 24, 15),
                        self.cam_small_font.render(' 8 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1050, 727, 24, 15),
                        self.cam_small_font.render(' 9 ', True, (255, 255, 255), (123, 123, 123)): pg.rect.Rect(1089, 727, 24, 15),
                    }

    # Функция преобразования времени в красивый формат
    def return_time(self):
        time = 4320 - self.time
        hours = time // (12 * 60)
        minutes = (time - hours * (12 * 60)) / (12 * 10)
        return f'0{int(hours)}:{int(minutes)}0AM'

    # Функция запуска музыкки
    def start_music(self):
        # Запуск музыки
        music = pg.mixer.Sound(r'sound\Ambient2.mp3')
        pg.mixer.Channel(0).play(music)

# Класс офиса
class GameDisplay:
    # Конструктор
    def __init__(self, window, language):
        self.window = window
        self.language = language
        self.camera = Camera(self.window)

    # Функция отрисовки
    def draw(self, stage, cam_num=0):
        if stage == 'office':
            self.window.fill((0, 123, 0))

        elif stage == 'display':
            self.camera.draw(cam_num)

# Класс окна победы 
class WinDisplay:
    # Конструктор
    def __init__(self, window):
        self.window = window
        self.text_font = pg.font.Font(r'font\Segment16B Regular.ttf', 50)
        self.frames = 120
        self.is_next_stage = False

    # Функция отрисовки
    def draw(self):
        self.window.fill((0, 0, 0))
        if self.frames % 2 == 0 and self.frames % 1 == 0:
            text = self.text_font.render('6:00AM', True, (255, 255, 255))
            self.window.blit(text, ((1200-text.get_width())/2, (800-text.get_height())/2, ))

        self.frames -= 1

        if self.frames <= 0:
            self.is_next_stage = True

    # функция запуска музыки
    def start_music(self):
        # Запуск музыки
        music = pg.mixer.Sound(r'sound\Alarm.mp3')
        pg.mixer.Channel(0).play(music)

# Класс камер
class Camera:
    # Конструктор
    def __init__(self, window):
        self.window = window

    # Функция отрисовки
    def draw(self, cam_num):
        self.window.fill((cam_num*20, cam_num*20, cam_num*20))

# Класс аниматроников
class Animatronics:
    # Конструктор
    def __init__(self, name):
        self.name = name

    # Функция отрисовки
    def draw(self):
        if name == 'Man':
            ...
        elif name == 'Bear':
            ...
        elif name == 'Grandfather':
            ...
        elif name == 'Airplane':
            ...

    # Функция перемещения 
    def move(self):
        ...


if __name__ == '__main__':
    pg.init()

    print(pg.font.get_fonts())