import pygame as pg

# Функция перевода
def translate_text(text, language):
    # Словарь со словами для Русского
    translate_ru = {
        'New game': 'Новая игра',
        'Continue': 'Продолжить',
        'Settings': 'Настройки',
        'Five Night\'s at Memes': 'Пять ночей с Мемами',
        'Made by Shaertiar (Alpha 0.5.1)': 'Сделанj Shaertiar-ом (Alpha 0.5.1)',
        'Back': 'Назад',
        '+ add music volume': '+ Увеличить громкость музыки',
        '- remove music volume': '- Уменьшить громкость музыки',
        '+ add effects volume': '+ Увеличить громкость эффектов',
        '- remove effects volume': '- Уменьшить громкость эффектов',
        'Music volume': 'Громкость музыки',
        'Effects volume': 'Громкость эффектов',
        'Language': 'Язык',
        'Press "Esc" to continue': 'Нажмите на "Esc" для продолжения',
        'After watching the FNaF movie, I decided to scroll': 'После просмотра фильма про ФНАФ я решил просто по ',
        'through my social network feed and suddenly passed': 'скролить ленту социальных сетей, и странным образом ',
        'out... I woke up in this strange office...': 'потерял сознание... Очнулся я уже в этом странном',
        '.': 'офисе...',
    }

    if language == 'en':
        return text
    elif language == 'ru':
        return translate_ru[text]

# Функция перевода кнопак
def translate_objects(text, language):
    # Словарь со словами для Английского
    translate_en = {
        'New game': pg.rect.Rect(50, 160, 240, 57),
        'Continue': pg.rect.Rect(50, 257, 240, 57),
        'Continue night':  (290, 257),
        'Settings': pg.rect.Rect(50, 354, 240, 57),
        'Back': pg.rect.Rect(0, 0, 120, 57),
        '+ add music volume': pg.rect.Rect(50, 107, 540, 57),
        '- remove music volume': pg.rect.Rect(50, 164, 630, 57),
        '+ add effects volume': pg.rect.Rect(50, 304, 600, 57),
        '- remove effects volume': pg.rect.Rect(50, 361, 690, 57),
        'Music volume': (410, 50),
        'Effects volume': (470, 246),
    }
    # Словарь со словами для Русского
    translate_ru = {
        'New game': pg.rect.Rect(50, 160, 300, 57),
        'Continue': pg.rect.Rect(50, 257, 300, 57),
        'Continue night':  (350, 257),
        'Settings': pg.rect.Rect(50, 354, 270, 57),
        'Back': pg.rect.Rect(0, 0, 150, 57),
        '+ add music volume': pg.rect.Rect(50, 107, 840, 57),
        '- remove music volume': pg.rect.Rect(50, 164, 840, 57),
        '+ add effects volume': pg.rect.Rect(50, 304, 900, 57),
        '- remove effects volume': pg.rect.Rect(50, 361, 900, 57),
        'Music volume': (530, 50),
        'Effects volume': (590, 246),
    }

    if language == 'en':
        return translate_en[text]
    elif language == 'ru':
        return translate_ru[text]
