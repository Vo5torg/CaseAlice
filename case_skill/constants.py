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
    'choose': "выбрать/выберу/выбиру",
    'top': "топ/топы/топе",
    'statistics': "статистика/статистика/статистику",
    'back': "назад",
    'next': "вперёд/далее",
    'open': "открыть",
    'drop': "дроп/вещи"

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
        "hello": [["Здравствуй!", "Здравствуй!"], ['Привет!', 'Привет!']],
        "hello_first": [["Привет! Назови свой никнейм.", "Привет! Назови свой никнэйм."]],
        "can": [["Этот навык может симулировать открытие кейсов.", "Этот навык может симулировать открытие кейсов."]],
        "create_user":
            {"help": [['Назови свой никнейм. Длина никнейма должна быть больше'
                       ' двух и меньше шестндцати символов. Также ник не должен'
                       ' содержать оскорбительные слова.',
                       'Назови свой никнэйм. Длина никнэйма должна быть больше'
                       ' двух и меньше шестндцати символов. Также ник не должен'
                       ' содержать оскорбительные слова.']],
             "none_name": [[
                 'Длина никнейма должна быть больше 2 и меньше 16 символов. Также ник не должен'
                 ' содержать оскорбительные слова.',
                 'Длина никнейма должна быть больше двух и меньше шестндцати символов.'
                 ' Также ник не должен содержать оскорбительные слова.']]
             },
        "menu":
            {
                "menu_phraz": [['В твоих возможностях:\nВыбрать кейс.'
                                '\nПосмотреть своё место в топе.\nПосмотреть статистику.',
                                'В твоих возможностях: Выбрать кейс.'
                                'Посмотреть своё место в топе. Посмотреть статистику.']],
                "help": [['Если хочешь выбрать кейс, скажи "Выбрать кейс".'
                          ' Чтобы открыть топ, скажи "Топ". Чтобы открыть статистику,'
                          ' произнеси "Статистика". Чтобы повторить предыдущую фразу скажи "Повторить".',
                          'Если хочешь выбрать кейс, скажи "Выбрать кейс".'
                          ' Чтобы открыть топ, скажи "Топ". Чтобы открыть статистику,'
                          ' произнеси "Статистика". Чтобы повторить предыдущую фразу скажи "Повторить".']],
            },
        "choose_case":
            {
                "help": [
                    [
                        'Выбери кейс, который хочешь открыть. Чтобы пролисать список кейсов дальше, скажите "Дальше".'
                        ' Чтобы вернуться в меню, скажи "Меню".',
                        'Выбери кейс, который хочешь открыть. Чтобы пролисать список кейсов дальше, скажите "Дальше".'
                        ' Чтобы вернуться в меню, скажи "Меню".']],
            },
        "open":
            {"menu_phraz": [['открой', '']],
             "help": [['Чтобы открыть кейс, скажи "Открыть". Чтобы посмотреть дроп из кейса, нажмите'
                       ' на кнопку "Дроп". Чтобы вернуться в меню, скажи "Меню".',
                       'Чтобы открыть кейс, скажи "Открыть". Чтобы посмотреть дроп из кейса, нажмите'
                       ' на кнопку "Дроп". Чтобы вернуться в меню, скажи "Меню".']]
             },
        "top":
            {"menu_phraz": [['Твоё место в топе {}.', 'Твоё место в топе sil <[300]> {}.']],
             "help": [['Место в топе определяется количеством '
                       'выпавших ножей или перчаток. Чтобы вернуться в меню, скажи "Меню". ',
                       'Место в топе определяется количеством '
                       'выпавших ножей или перчаток. Чтобы вернуться в меню, скажи "Меню". ']]
             },
        "statistics":
            {"menu_phraz": [[
                'Открыто кейсов всего: {}\nВыбито\nНожи и перчатки: {}\nТайное: {}\nЗасекреченное:'
                ' {}\nЗапрещённое: {}\nАрмейское: {}\n',
                'Открыто кейсов всего: {}\nВыбито\nНожи и перчатки: {}\nТайное: {}\nЗасекреченное:'
                ' {}\nЗапрещённое: {}\nАрмейское: {}\n']],
                "help": [['Чтобы вернуться в меню, скажи "Меню".', 'Чтобы вернуться в меню, скажи "Меню".']]
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
top_menu_phraz_dialog = DIALOGS_CONTENT["dialogs"]["top"]["menu_phraz"]
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

SOUND_WEAPON = {
    "Револьвер R8": "револьвер",
    "Five-SeveN": "файв севен",
    "P2000": "пи две тясячи",
    "ПП-19 Бизон": "пэ пэ 19 бизон",
    "SG 553": "эс джи 553",
    "XM1014": "экс эм 1014",
    "MAG-7": "маг 10",
    "Glock-18": "глок 18",
    "Negev": "негев",
    "Nova": "н+ова",
    "UMP-45": "ю эм пи 45",
    "USP-S": "ю эс пи",
    "AUG": "ауг",
    "AWP": "авп",
    "MP7": "эм п 7",
    "M4A1-S": "эм 4 а 4 эс",
    "M4A4": "эм 4 а 4",
    "Sawed-Off": "савд офф",
    "Tec-9": "тэк 9",
    "G3SG1": "джи 3 эс джи 1",
    "CZ75-Auto": "цэ зэ 75",
    "MP9": "эм пэ 9",
    "AK-47": "а ка 47",
    "P250": "пэ 250",
    "Galil AR": "галил ар",
    "Dual Berettas": "дуал беретс",
    "SSG 08": "эс эс джи 08",
    "MP5-SD": "эм пэ 5 эс дэ",
    "P90": "пи 90",
}
