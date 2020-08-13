from bs4 import BeautifulSoup
import requests as req
from os.path import basename
import os, json

main_site = "https://csgohub.ru"
with open("data_file.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)
knifes_src = \
    [
        ("/gloves/gloves_specialist.html", 'Перчатки спецназа'),
        ("/gloves/gloves_moto.html", 'Мотоциклетные перчатки'),
        ('/gloves/gloves_hand_wraps.html', 'Обмотки рук'),
        ("/gloves/gloves_driver.html", 'Водительские перчатки'),
        ("/gloves/gloves_sport.html", 'Спортивные перчатки'),
        ("/gloves/gloves_bloodhound.html", 'Перчатки «Бладхаунд»'),
        ("/gloves/gloves_hydra.html", "Перчатки «Гидра»"),
    ]

for knife_info in knifes_src:
    resp = req.get(main_site + knife_info[0])
    soup = BeautifulSoup(resp.text, 'lxml')

    for knife_soup in soup.find_all("div", class_='skins-tab center-block'):
        name_knife = knife_info[1] + " - " + knife_soup.find("div", 'top-skin-box').find("h3").get_text()
        type_ = " ".join(knife_soup.find("div", class_='quality').find("p").get_text().split()[:2]).capitalize()
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
