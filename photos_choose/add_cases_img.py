import os, json
import requests

url = "https://dialogs.yandex.net/api/v1/skills/a4bc31fe-10fe-4259-9b4c-fcd692272554/images"

os.chdir("../resourses/Кейсы_")
print(os.getcwd())
with open("data_file.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)
data['cases'] = []
for file_name in os.listdir(os.getcwd()):
    gog = True
    for i in data['cases_name']:
        files = {"file": open(file_name, "rb")}
        if i in file_name[:-4]:

            a = requests.post(url, headers={"Authorization": "OAuth AQAAAAAbmj-UAAT7o2_k9MfXh00huVG9-nCl1zg"},
                              files=files)
            data['cases'].append({'name': i})
            if a.status_code == 201:
                id = a.json()["image"]["id"]
                data['cases'][-1]['src'] = id
                gog = False
            break
    if gog:
        print(file_name)

with open("data_file.json", "w", encoding='utf-8') as write_file:
    json.dump(data, write_file, ensure_ascii=False)
