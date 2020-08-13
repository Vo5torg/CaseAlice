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
    if (4 <= len(req.text) <= 15) and not req.dangerous:
        session['state'] = State.MENU
        User.add_new_user(req.text, req.user_id)
        res.text, res.tts = choice(menu_phraz_dialog)
        res.buttons = [create_button(i) for i in BUTTONS[session['state']]]
    else:
        res.text, res.tts = choice(none_name_dialog)


"""-----------------All_room_commands-------------------"""


@handler.hello_command
@default_buttons
def hello(req, res, session):
    user = User.get_user(req.user_id)
    if not user:
        session['state'] = State.CREATE_USER
        res.text, res.tts = choice(hello_first_dialog)

    else:
        res.text, res.tts = choice(hello_dialog)
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
    res.buttons = session["buttons"]


@handler.command(words=WORDS['help'], states=State.ALL)
@default_buttons
def help_(req, res, session):
    res.text, res.tts = choice(HELPS_ALL[session['state']]['help'])


@handler.command(words=WORDS['menu'], states=State.ALL)
@save_previous_session_info
def go_menu_(req, res, session):
    session['state'] = State.MENU
    res.text, res.tts = choice(menu_phraz_dialog)
    res.buttons = [create_button(i) for i in BUTTONS[State.MENU]]


"""-----------------MENU_commands-------------------"""


@handler.command(words=WORDS['choose'], states=State.MENU)
@save_previous_session_info
def go_choose_case(req, res, session):
    session['list_cases'] = copy(CASES_LIST)
    res.text = 'выбрать кейс'
    session['state'] = State.CHOOSE_OPEN_CASE
    session['list_nums'] = 0
    list_case_now = get_cases_list(session['list_cases'], session['list_nums'])
    res.card = get_cases_card(deepcopy(EMPTY_CARD), list_case_now)
    res.buttons = get_buttons_next_back(session['list_cases'], session['list_nums'])
    res.buttons.append(create_button('Меню'))


@handler.command(words=WORDS['top'], states=State.MENU)
@save_previous_session_info
@default_buttons
def go_top(req, res, session):
    session['state'] = State.TOP
    res.text = create_top_list(req)


@handler.command(words=WORDS['statistics'], states=State.MENU)
@save_previous_session_info
@default_buttons
def go_statistics(req, res, session):
    session['state'] = State.STATISTICS
    res.text = choice(statistics_phraz_dialog)[0].format(*User.get_statistics(User.get_user(req.user_id)))


@handler.undefined_command(states=State.CHOOSE_OPEN_CASE)
@default_buttons
def undefined_menu(req, res, session):
    res.text = 'топ'


"""-----------------CHOOSE_OPEN_CASE_commands-------------------"""


@handler.command(words=WORDS['next'], states=State.CHOOSE_OPEN_CASE)
@save_previous_session_info
def next_list_(req, res, session):
    res.text = ' открыть'
    if get_cases_list(session['list_cases'], session['list_nums'] + 1):
        session['list_nums'] += 1
    list_case_now = get_cases_list(session['list_cases'], session['list_nums'])
    res.card = get_cases_card(deepcopy(EMPTY_CARD), list_case_now)
    res.buttons = get_buttons_next_back(session['list_cases'], session['list_nums'])
    res.buttons.append(create_button('Меню'))


@handler.command(words=WORDS['back'], states=State.CHOOSE_OPEN_CASE)
@save_previous_session_info
def back_list_(req, res, session):
    res.text = ' открыть'
    if session['list_nums'] >= 1:
        session['list_nums'] -= 1
    list_case_now = get_cases_list(session['list_cases'], session['list_nums'])
    res.card = get_cases_card(deepcopy(EMPTY_CARD), list_case_now)
    res.buttons = get_buttons_next_back(session['list_cases'], session['list_nums'])
    res.buttons.append(create_button('Меню'))


@handler.undefined_command(states=State.CHOOSE_OPEN_CASE)
@default_buttons
def undefined_choose_case(req, res, session):
    session["cases_name"] = search_cases(req.text, session['list_cases'])
    session['state'] = State.OPEN
    res.card = BIG_IMAGE
    res.text, res.card['title'], res.card['image_id'] = "апапа", "аапап", CASES_IN_LIST[session["cases_name"]]


"""-----------------OPEN_commands-------------------"""


@handler.command(words=WORDS['open'], states=State.OPEN)
@save_previous_session_info
@default_buttons
def open_(req, res, session):
    quality_weapon_ru, quality_weapon = open_case(session["cases_name"])

    weapon = search_weapon(session["cases_name"], quality_weapon_ru)
    update_statistics(quality_weapon, req)
    res.card = BIG_IMAGE
    res.text, res.card['title'], res.card['image_id'], \
    res.card['description'] = weapon['name'], weapon['name'], weapon['src'], weapon['type']
    if quality_weapon_ru == "Экстраординарного типа" and weapon.get('quality', {}) == "knife":
        res.card['description'] = "Тайное"


@handler.command(words=WORDS['drop'], states=State.OPEN)
@save_previous_session_info
@default_buttons
def drop_(req, res, session):
    res.card = BIG_IMAGE
    res.text, res.card['title'], res.card['image_id'] = "апапа", "аапап", CASES_IN_LIST[session["cases_name"]]


@handler.undefined_command(states=State.OPEN)
@default_buttons
def undefined_open_case(req, res, session):
    res.text = 'чвсв'


"""-----------------STATISTICS_commands-------------------"""


@handler.undefined_command(states=State.STATISTICS)
@default_buttons
def undefined_statistics(req, res, session):
    res.text = 'чвсв'


"""-----------------TOP_commands-------------------"""


@handler.undefined_command(states=State.TOP)
@default_buttons
def undefined_top(req, res, session):
    res.text = 'чвсв'
