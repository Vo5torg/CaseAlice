from bs4 import BeautifulSoup
import requests as req
from os.path import basename
import os

types_ammo = {"армейское": 'army',
              "запрещённое": 'prohibited',
              "засекреченное": 'classified',
              "тайное": 'secret',
              "особо": 'vrare'}


def delete_sign(name_case):
    for i in [":"]:
        name_case = name_case.replace(i, "")
    return name_case


info = {
    [{
        'name': '',
        'type': '',
        'case': '',
        'src': '',
        }
    ]
}
main_site = "https://csgohub.ru"

main_resp = req.get(main_site + "/cases.html")

soup = BeautifulSoup(main_resp.text, 'lxml')

for case_block in soup.find_all("div", class_='skins-tab-case-section center-block'):
    case_src = case_block.find('a').get('href')

    print(case_src)
    case_resp = req.get(main_site + case_src)
    soup_case = BeautifulSoup(case_resp.text, 'lxml')
    name_case = delete_sign(soup_case.find("h1", class_='margin-top-sm').get_text())
    try:
        os.mkdir(basename(name_case))
    except:
        pass

    for i in soup_case.find_all("div", class_='skins-tab center-block'):
        try:
            img_src = i.find("div", class_='main-image-block').find('a').get('href')
            name = i.find("div", class_='top-skin-box').find("h3").get_text().replace("|", "-")
            print(name)
            # ammo_type = types_ammo[
            #     [type_ for type_ in types_ammo.keys() if type_ in i.find("div", class_='quality').get("p").get_text()][0]]

            with open(basename(name_case) + "/" + name + ".png", "wb") as f:
                f.write(req.get(main_site + img_src).content)
        except:
            pass
