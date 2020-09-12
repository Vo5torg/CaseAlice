from base_skill.skill import *
from .state import State
from .mechanics import *
from .database import User

handler = CommandHandler()


class CaseSimulator(BaseSkill):
    name = 'case_simulator_skill'
    command_handler = handler


"""-----------------Create_user_commands-------------------"""


@handler.undefined_command(states=State.CREATE_USER)
@save_previous_session_info
def undefined_create_user(req, res, session):
    if (2 <= len(req.text) <= 15) and not req.dangerous:
        session['state'] = State.MENU
        User.add_new_user(req.text, req.user_id)
        res.text, res.tts = choice(menu_phraz_dialog)
        res.text = "Запомнила. " + res.text
        res.tts = "Запомнила. " + res.tts
        res.buttons = [create_button(i) for i in BUTTONS[session['state']]]
    else:
        res.text, res.tts = choice(none_name_dialog)


"""-----------------All_room_commands-------------------"""


@handler.hello_command
@save_previous_session_info
@default_buttons
def hello(req, res, session):
    user = User.get_user(req.user_id)
    if not user:
        session['state'] = State.CREATE_USER
        res.text, res.tts = choice(hello_first_dialog)

    else:
        res.text, res.tts = choice(hello_dialog)
        menu_phraz = choice(menu_phraz_dialog)
        res.text += " " + menu_phraz[0]
        res.tts += " " + menu_phraz[1]
        session['state'] = State.MENU


@handler.command(words=WORDS['exit'], states=State.ALL)
@save_previous_session_info
def to_exit(req, res, session):
    res.text, res.tts = choice(exit_dialog)
    res.end_session = True


@handler.command(words=WORDS['can'], states=State.ALL)
@save_previous_session_info
def what_can_you_do(req, res, session):
    res.text, res.tts = choice(can_dialog)
    if session.get("buttons"):
        res.buttons = session["buttons"]


@handler.command(words=WORDS['help'], states=State.ALL)
@default_buttons
def help_(req, res, session):
    res.text, res.tts = choice(HELPS_ALL[session['state']]['help'])
    if State.CHOOSE_OPEN_CASE:
        res.buttons.append(create_button('Меню'))


@handler.command(words=WORDS['menu'], states=State.AFTER_REG)
@save_previous_session_info
def go_menu_(req, res, session):
    session['state'] = State.MENU
    res.text, res.tts = choice(menu_phraz_dialog)
    res.buttons = [create_button(i) for i in BUTTONS[State.MENU]]


@handler.command(words=WORDS['repeat'], states=State.ALL)
def repeat_(req, res, session):
    res.text, res.tts = "", ""


"""-----------------MENU_commands-------------------"""


@handler.command(words=WORDS['choose'], states=State.AFTER_REG)
@save_previous_session_info
def go_choose_case(req, res, session):
    session['list_cases'] = copy(CASES_LIST)
    session['state'] = State.CHOOSE_OPEN_CASE
    session['list_nums'] = 0
    list_case_now = get_cases_list(session['list_cases'], session['list_nums'])
    res.text = SIL.format(350).join([x["name"] for x in list_case_now])
    res.card = get_cases_card(deepcopy(EMPTY_CARD), list_case_now)
    res.buttons = get_buttons_next_back(session['list_cases'], session['list_nums'])
    res.buttons.append(create_button('Меню'))


@handler.command(words=WORDS['top'], states=State.AFTER_REG)
@save_previous_session_info
@default_buttons
def go_top(req, res, session):
    session['state'] = State.TOP
    res.text, num = create_top_list(req)
    res.tts = choice(top_menu_phraz_dialog)[1].format(num)


@handler.command(words=WORDS['statistics'], states=State.AFTER_REG)
@save_previous_session_info
@default_buttons
def go_statistics(req, res, session):
    session['state'] = State.STATISTICS
    res.text = choice(statistics_phraz_dialog)[0].format(*User.get_statistics(User.get_user(req.user_id)))


@handler.undefined_command(states=State.MENU)
@default_buttons
def undefined_menu(req, res, session):
    res.text, res.tts = choice(HELPS_ALL[session['state']]['help'])


"""-----------------CHOOSE_OPEN_CASE_commands-------------------"""


@handler.command(words=WORDS['next'], states=State.CHOOSE_OPEN_CASE)
@save_previous_session_info
def next_list_(req, res, session):
    if get_cases_list(session['list_cases'], session['list_nums'] + 1):
        session['list_nums'] += 1
    list_case_now = get_cases_list(session['list_cases'], session['list_nums'])
    res.text = SIL.format(300).join([x["name"] for x in list_case_now])
    res.card = get_cases_card(deepcopy(EMPTY_CARD), list_case_now)
    res.buttons = get_buttons_next_back(session['list_cases'], session['list_nums'])
    res.buttons.append(create_button('Меню'))


@handler.command(words=WORDS['back'], states=State.CHOOSE_OPEN_CASE)
@save_previous_session_info
def back_list_(req, res, session):
    if session['list_nums'] >= 1:
        session['list_nums'] -= 1
    list_case_now = get_cases_list(session['list_cases'], session['list_nums'])
    res.text = SIL.format(300).join([x["name"] for x in list_case_now])
    res.card = get_cases_card(deepcopy(EMPTY_CARD), list_case_now)
    res.buttons = get_buttons_next_back(session['list_cases'], session['list_nums'])
    res.buttons.append(create_button('Меню'))


@handler.undefined_command(states=State.CHOOSE_OPEN_CASE)
def undefined_choose_case(req, res, session):
    case = search_cases(req.text, session['list_cases'])
    if case:
        session["cases_name"] = case['name']
        session['state'] = State.OPEN
        list_text = [x['name'] for x in get_weapons_in_case(session["cases_name"])]
        res.card = copy(BIG_IMAGE)
        res.text, res.card['image_id'] = "Открыть. Меню. Помощь.", case['src_in']
        res.buttons = [create_button(i) for i in BUTTONS[session['state']]]
        res.buttons[1]['url'] = search_cases(session["cases_name"], session['list_cases'])['url']
    else:
        session['list_cases'] = copy(CASES_LIST)
        res.text = 'Повторите ещё раз'
        session['state'] = State.CHOOSE_OPEN_CASE
        list_case_now = get_cases_list(session['list_cases'], session['list_nums'])
        res.card = get_cases_card(deepcopy(EMPTY_CARD), list_case_now)
        res.buttons = get_buttons_next_back(session['list_cases'], session['list_nums'])
        res.buttons.append(create_button('Меню'))


"""-----------------OPEN_commands-------------------"""


@handler.command(words=WORDS['open'], states=State.OPEN)
@save_previous_session_info
def open_(req, res, session):
    quality_weapon_ru, quality_weapon = open_case(session["cases_name"])
    weapon = search_weapon(session["cases_name"], quality_weapon_ru)
    update_statistics(quality_weapon, req)
    res.card = copy(BIG_IMAGE)
    res.text, res.card['title'], res.card['image_id'], \
    res.card['description'] = weapon['name'], weapon['name'], weapon['src'], weapon['type']
    res.tts = res.text[:]
    for i in SOUND_WEAPON.keys():
        if i in weapon['name']:
            res.tts = weapon['name'].replace(i, SOUND_WEAPON[i]) + SIL.format(300) + quality_weapon_ru
    if quality_weapon_ru == "Экстраординарного типа" and weapon.get('quality', {}) == "knife":
        res.card['description'] = "Тайное"
    if quality_weapon_ru == "Экстраординарного типа":
        res.tts = choice(KNIFE_SOUND) + res.tts
    res.buttons = [create_button(i) for i in BUTTONS[session['state']]]
    res.buttons[1]['url'] = search_cases(session["cases_name"], session['list_cases'])['url']


@handler.undefined_command(states=State.OPEN)
def undefined_open_case(req, res, session):
    res.text, res.tts = choice(HELPS_ALL[session['state']]['help'])
    res.buttons = [create_button(i) for i in BUTTONS[session['state']]]
    res.buttons[1]['url'] = search_cases(session["cases_name"], session['list_cases'])['url']


"""-----------------STATISTICS_commands-------------------"""


@handler.undefined_command(states=State.STATISTICS)
@default_buttons
def undefined_statistics(req, res, session):
    res.text, res.tts = choice(HELPS_ALL[session['state']]['help'])
    if State.CHOOSE_OPEN_CASE:
        res.buttons.append(create_button('Меню'))


"""-----------------TOP_commands-------------------"""


@handler.undefined_command(states=State.TOP)
@default_buttons
def undefined_top(req, res, session):
    res.text, res.tts = choice(HELPS_ALL[session['state']]['help'])
    if State.CHOOSE_OPEN_CASE:
        res.buttons.append(create_button('Меню'))
