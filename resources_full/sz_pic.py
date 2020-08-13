import requests
import json
import os
from PIL import Image

with open("../resourses/Содержимое кейса/data_file.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)

url = "https://dialogs.yandex.net/api/v1/skills/a4bc31fe-10fe-4259-9b4c-fcd692272554/images"

for dir_name in [x[0] for x in os.walk(os.getcwd())][1:]:

    os.chdir(dir_name)

    for file_name in os.listdir(os.getcwd()):
        image = Image.open(file_name)

        image = image.resize((int(image.size[0]*0.5), int(image.size[1]*0.5)), Image.ANTIALIAS)
        image.save(file_name, quality=95, optimize=True)

    os.chdir('../')


# for i in data['info']:
#     gog = False
#     for dir_name in [x[0] for x in os.walk(os.getcwd())][1:]:
#         os.chdir(dir_name)
#         for file_name in os.listdir(os.getcwd()):
#             if i['name'] in file_name[:-4]:
#                 gog = True
#                 break
#
#         os.chdir('../')
#
#     if not gog:
#
#         print(i['name'] )
#         data['info'].remove(i)


# with open("data_file.json", "w", encoding='utf-8') as write_file:
#     json.dump(data, write_file, ensure_ascii=False)
