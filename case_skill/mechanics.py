from .constants import *
from base_skill.skill import create_button
from random import randint, choice
from .database import User


def save_previous_session_info(func):
    def wrapper(req, res, session):
        func(req, res, session)
        session["text"] = res.text
        session["tts"] = res.tts
        session["buttons"] = res.buttons
        session["card"] = res.card if res.card else None

    return wrapper


def return_previous_info(func):
    def wrapper(req, res, session):
        func(req, res, session)
        res.text = res.text + " " + session["text"]
        res.tts = res.tts + " sil <[300]> " + session["tts"]
        res.buttons = session["buttons"]
        if session["card"]:
            res.card = session["card"]

    return wrapper


def default_buttons(func):
    def wrapper(req, res, session):
        func(req, res, session)
        if session['state'] not in BUTTONS:
            return

        if len(res.buttons) == 0:
            res.buttons = [create_button(x) for x in btn(BUTTONS.get(session['state'], []))]
        else:
            for x in btn(BUTTONS.get(session['state'], [])):
                res.buttons.append(create_button(x))

    return wrapper


def get_buttons_next_back(full_list, nums):
    buttons = []
    if nums > 0:
        buttons.append('Назад')
    if 4 > nums:
        buttons.append('Далее')
    return [create_button(i) for i in buttons]


def get_cases_list(full_list, nums):
    return deepcopy(full_list)[nums * 5:(nums + 1) * 5]


def get_cases_card(card, list_case):
    for i in list_case:
        item_case = deepcopy(EMPTY_ITEM)
        item_case["image_id"], item_case["title"] = i["src"], i["name"]
        item_case["button"]["text"] = i["name"]
        item_case["button"]['payload']["text"] = i["name"]
        card['items'].append(item_case)
    return card


def search_cases(text, cases_list):
    for i in cases_list:
        if i['name'].lower() == text.lower():
            return i['name'].strip()
    return None


def open_case(case_name):
    num = randint(0, 10000)
    for i in PERSENT_INFO.keys():
        if PERSENT_INFO[i]['min'] <= num <= PERSENT_INFO[i]['max']:
            return QUALITY_INFO[i], i
    return None, None


def search_weapon(case_name, quality_weapon):
    list_weapons_now = list(
        filter(lambda x: x["type"] == quality_weapon.strip() and x["case"] == case_name.strip(), WEAPONS_LIST))
    return choice(list_weapons_now)


def update_statistics(quality_weapon, req):
    user = User.get_user(req.user_id)
    user.update_quality(user, quality_weapon)


def create_top_list(req):
    top_list = User.get_top()
    user = User.get_user(req.user_id)
    text = ""
    for users, n in enumerate(top_list[10:]):
        text += PATTERN_TOP_USER.format(n, users.name, users.сontraband)
    if not (user in top_list):
        text += "\n" * 2
        text += PATTERN_TOP_USER.format(top_list.index(user), user.name, user.сontraband)
    return text.strip('\n')