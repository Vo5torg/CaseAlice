from bs4 import BeautifulSoup
import requests as req
from os.path import basename
import os, json

main_site = "https://csgohub.ru"


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
