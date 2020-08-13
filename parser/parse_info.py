from bs4 import BeautifulSoup
import requests as req
from os.path import basename
import os, json


def delete_sign(name_case):
    for i in [":"]:
        name_case = name_case.replace(i, "")
    return name_case


data = {'info': [
]}

with open("data_file.json", "r") as read_file:
    data = json.load(read_file)

main_site = "https://csgohub.ru"

main_resp = req.get(main_site + "/cases.html")

soup = BeautifulSoup(main_resp.text, 'lxml')

for case_block in soup.find_all("div", class_='skins-tab-case-section center-block'):
    case_src = case_block.find('a').get('href')

    print(case_src)
    case_resp = req.get(main_site + case_src)
    soup_case = BeautifulSoup(case_resp.text, 'lxml')
    name_case = delete_sign(soup_case.find("h1", class_='margin-top-sm').get_text())

    for i in soup_case.find_all("div", class_='skins-tab center-block'):
        try:
            img_src = i.find("div", class_='main-image-block').find('a').get('href')
            name = i.find("div", class_='top-skin-box').find("h3").get_text().replace("|", "-")
            type_ = i.find("div", class_='quality').find("p").get_text().split()[0]
            st = i.find("div", class_='stattrak').find("p").get_text()
            case = name_case
            if st == 'StatTrak доступен':
                st = True
            else:
                st = False

            data['info'].append({
                'name': name,
                'type': type_,
                'case': case,
                'src': ' ',
                'st': st
            })
        except:
            pass

with open("data_file.json", "w", encoding='utf-8') as write_file:
    json.dump(data, write_file,ensure_ascii=False)
