from bs4 import BeautifulSoup
import requests as req
from os.path import basename
import os, json

main_site = "https://csgohub.ru"


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
    try:
        os.mkdir(basename(knife_info[1]))
    except:
        pass

    for knife_soup in soup.find_all("div", class_='skins-tab center-block'):
        name_knife = knife_soup.find("div", 'top-skin-box').find("h3").get_text()
        img_src = knife_soup.find("div", 'main-image-block').find("a").get('href')
        with open(basename(knife_info[1]) + "/" + name_knife + ".png", "wb") as f:
            f.write(req.get(main_site + img_src).content)
        print(knife_info[1] + "/" + name_knife)
