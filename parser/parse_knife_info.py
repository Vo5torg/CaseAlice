from bs4 import BeautifulSoup
import requests as req
from os.path import basename
import os, json

main_site = "https://csgohub.ru"
with open("data_file.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)
knifes_src = \
    [
        ('/weapons/weapon_bayonet.html', 'Штык-нож'),
        ("/weapons/weapon_knife_flip.html", 'Складной нож'),
        ('/weapons/weapon_knife_gut.html', 'Нож с лезвием-крюком'),
        ("/weapons/weapon_knife_karambit.html", 'Керамбит'),
        ("/weapons/weapon_knife_m9_bayonet.html", 'Штык-нож M9'),
        ('/weapons/weapon_knife_tactical.html', 'Охотничий нож'),
        ("/weapons/weapon_knife_butterfly.html", 'Нож-бабочка'),
        ('/weapons/weapon_knife_falchion.html', 'Фальшион'),
        ('/weapons/weapon_knife_push.html', 'Тычковые ножи'),
        ("/weapons/weapon_knife_survival_bowie.html", 'Нож Боуи'),
        ('/weapons/weapon_knife_navaja.html', 'Наваха'),
        ("/weapons/weapon_knife_stiletto.html", 'Стилет'),
        ('/weapons/weapon_knife_talon.html', 'Коготь'),
        ('/weapons/weapon_knife_ursus.html', 'Медвежий нож'),
        ('/weapons/weapon_knife_classic.html', 'Классический нож'),
        ('/weapons/weapon_knife_cord.html', 'Паракорд-нож'),
        ('/weapons/weapon_knife_canis.html', 'Нож выживания'),
        ('/weapons/weapon_knife_skeleton.html', 'Скелетный нож'),
        ("/weapons/weapon_knife_outdoor.html", 'Нож «Бродяга»')
    ]

for knife_info in knifes_src:
    resp = req.get(main_site + knife_info[0])
    soup = BeautifulSoup(resp.text, 'lxml')

    for knife_soup in soup.find_all("div", class_='skins-tab center-block'):
        name_knife = knife_info[1] + " - " + knife_soup.find("div", 'top-skin-box').find("h3").get_text()
        type_ = knife_soup.find("div", class_='quality').find("p").get_text().split()[1]
        st = knife_soup.find("div", class_='stattrak').find("p").get_text()

        if st == 'StatTrak доступен':
            st = True
        else:
            st = False

        data['info'].append({
            'name': name_knife,
            'type': type_,
            'case': ' ',
            'src': ' ',
            'st': st
        })

with open("data_file.json", "w", encoding='utf-8') as write_file:
    json.dump(data, write_file, ensure_ascii=False)
