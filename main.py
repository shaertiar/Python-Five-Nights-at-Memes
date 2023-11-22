import pygame as pg
import json

import game

# Функция изменения настроек
def change_settings(change, to):
    settings = json.load(open(r'settings.json', 'r'))
    settings[change] = to
    json.dump(settings, open(r'settings.json', 'w'))

# Функция отрисовки консольных данных
def print_console():
    window.blit(console_font.render(f'To remove the console, click on (`) ', True, (255, 255, 255), (0, 0, 0)), (0, 0))
    window.blit(console_font.render(f'FPS: {round(clock.get_fps(), 1)}/{float(FPS)}', True, (255, 255, 255), (0, 0, 0)), (0, 14))
    window.blit(console_font.render(f'Mouse pos: {pg.mouse.get_pos()}', True, (255, 255, 255), (0, 0, 0)), (0, 28))
    window.blit(console_font.render(f'Current night: {current_night}', True, (255, 255, 255), (0, 0, 0)), (0, 42))

# Настройки
settings = json.load(open(r'settings.json', 'r'))
is_print_console = False
current_night = settings['Current night']

# Иниацилизация
pg.init()

# Создание часов
clock = pg.time.Clock()

# Создание шрифта
console_font = pg.font.SysFont('consolas', 14)

# Создание окна
window = pg.display.set_mode((1200, 800))
pg.display.set_caption('Five Night\'s at Memes')
FPS = 12

# Создание игры
game = game.Game(window)

# Игровой цикл
is_game = True
while is_game:
    # Обработка событий
    for event in pg.event.get():
        # Обработка выхода из игры
        if event.type == pg.QUIT:
            is_game = False

        # Обработка нажатий клавиш
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKQUOTE:
                is_print_console = not is_print_console
            else:
                game.pressed_on(event.key)

        # Обработка нажатий на кнопку мыши
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                game.clicked_on(event.pos)

    # Отрисовка игры
    game.draw()

    # Отрисовка консоли при надобности
    if is_print_console:
        print_console()

    # Обновление окна
    pg.display.update()
    clock.tick(FPS)