from copy import deepcopy, copy
from random import choice
from .state import State
import json

with open("/home/AbilityForAlice2/mysite/case_skill/data_file.json", "r", encoding='utf-8') as read_file:
    DATA_WEAPONS_CASES = json.load(read_file)

WORDS = {
    'yes': "да/давай/поехали/начали/начинаем/гоу/го/конечно/полетели/начать/ес",
    'no': "нет/не/нит/никак/ноу",
    'menu': "главное/меню",
    'repeat': "повтори/повторить/повтор/рипит",
    'help': "помощь/помоги/подсказка/подскажи/подскажите/help/правила",
    'exit': "выйти/выход/закрыть/выйди/закрой/покинь",
    'ability': "навык/навыка/диалог/диалога",
    'can': "умеешь/уметь",
    'close': "завершить/заве",
    'choose': "выбрать/выберу",
    'top': "топ/топы",
    'statistics': "статистика",
    'back': "назад",
    'next': "вперёд/далее",
    'open': "открыть",
    'drop': "дроп"

}

for w in WORDS:
    WORDS[w] = tuple(WORDS[w].split('/'))


def txt(string):
    return choice(string)


def btn(string):
    if isinstance(string, tuple):
        return list(map(lambda x: txt(x.split('/')), string))
    return txt(string.split('/')),


BUTTONS = {State.CREATE_USER: ('Помощь', 'Выход'),
           State.MENU: ('Выбрать кейс', 'Топ', 'Статистика', 'Что ты умеешь?', 'Выход'),
           State.CHOOSE_OPEN_CASE: ('Назад', 'Далее'),
           State.STATISTICS: ("Меню", 'Помощь'),
           State.TOP: ('Меню', 'Помощь'),
           State.OPEN: ("Открыть", "Дроп", "Меню", 'Помощь')}

DIALOGS_CONTENT = {
    "dialogs": {
        "exit": [["До свидания!", "До свидания!"]],
        "hello": [["Выбрать топ!", "Выбрать топ!"]],
        "hello_first": [["Привет!", "Привет!"]],
        "can": [["Я умею", "Я умею"]],
        "create_user":
            {"create_phraz": [['Скажи имя', '']],
             "help": [['Помощь', '']],
             "none_name": [['Повтори имя', 'Повтори имя']]
             },
        "menu":
            {
                "menu_phraz": [['выбрать кейс, топ, статистика, помощь', '']],
                "help": [['Помощь', '']],
            },
        "choose_case":
            {
                "help": [['Помощь', '']],
            },
        "open":
            {"menu_phraz": [['открой', '']],
             "help": [['Открыть', '']]
             },
        "top":
            {"menu_phraz": [['', '']],
             "help": [['Топ', '']]
             },
        "statistics":
            {"menu_phraz": [[
                'Открыто кейсов всего: {}\nВыбито\nНожи и перчатки: {}\nТайное: {}\nЗасекреченное:'
                ' {}\nЗапрещённое: {}\nАрмейкое: {}\n',
                'Открыто кейсов всего: {}\nВыбито\nНожи и перчатки: {}\nТайное: {}\nЗасекреченное:'
                ' {}\nЗапрещённое: {}\nАрмейкое: {}\n']],
                "help": [['Топ', '']]
            },

    }
}

hello_first_dialog = DIALOGS_CONTENT["dialogs"]["hello_first"]
hello_dialog = DIALOGS_CONTENT["dialogs"]["hello"]
create_help_dialog = DIALOGS_CONTENT["dialogs"]["create_user"]["help"]
menu_help_dialog = DIALOGS_CONTENT["dialogs"]["menu"]["help"]
menu_phraz_dialog = DIALOGS_CONTENT["dialogs"]["menu"]["menu_phraz"]
open_help_dialog = DIALOGS_CONTENT["dialogs"]["open"]["help"]
top_help_dialog = DIALOGS_CONTENT["dialogs"]["top"]["help"]
exit_dialog = DIALOGS_CONTENT["dialogs"]["exit"]
can_dialog = DIALOGS_CONTENT["dialogs"]["can"]
none_name_dialog = DIALOGS_CONTENT["dialogs"]["create_user"]["none_name"]
statistics_phraz_dialog = DIALOGS_CONTENT["dialogs"]["statistics"]["menu_phraz"]
statistics_help_dialog = DIALOGS_CONTENT["dialogs"]["statistics"]["help"]
choose_case_help_dialog = DIALOGS_CONTENT["dialogs"]["choose_case"]["help"]

PATTERN_TOP_USER = "{}. {} : {}\n"
SIL = "sil <[{}]>"
KNIFE_SOUND = ['<speaker audio="alice-sounds-game-win-1.opus">',
               '<speaker audio="alice-sounds-game-win-2.opus">',
               '<speaker audio="alice-sounds-game-win-3.opus">']
CASES_LIST = deepcopy(DATA_WEAPONS_CASES['cases'])
CASES_IN_LIST = deepcopy(DATA_WEAPONS_CASES['cases_in'])
WEAPONS_LIST = deepcopy(DATA_WEAPONS_CASES['info'])
EMPTY_CARD = {
    "type": "ItemsList",
    "header": {
        "text": " "
    },
    "items": [

    ]
}
EMPTY_ITEM = {
    "image_id": " ",
    "title": " ",
    "button": {
        "text": " ",
        "payload": {
            "text": " "
        }
    }
}
BIG_IMAGE = {
    "type": "BigImage",
    "image_id": "",
    "title": "",
    "description": "",

}

HELPS_ALL = {State.CREATE_USER: {'help': create_help_dialog},
             State.MENU: {'help': menu_help_dialog},
             State.CHOOSE_OPEN_CASE: {'help': choose_case_help_dialog},
             State.OPEN: {'help': open_help_dialog},
             State.STATISTICS: {'help': statistics_help_dialog},
             State.TOP: {'help': top_help_dialog}
             }

PERSENT_INFO = {'army': {'min': 0, 'max': 7990},
                'prohibited': {'min': 7991, 'max': 9589},
                'classified': {'min': 9590, 'max': 9909},
                'secret': {'min': 9910, 'max': 9973},
                'contraband': {'min': 9974, 'max': 10000}
                }

QUALITY_INFO = {'army': "Армейское",
                'prohibited': "Запрещенное",
                'classified': "Засекреченное",
                'secret': "Тайное",
                'contraband': "Экстраординарного типа"
                }
