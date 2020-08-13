
import os, json
import requests

url = "https://dialogs.yandex.net/api/v1/skills/a4bc31fe-10fe-4259-9b4c-fcd692272554/images"


with open("../resourses/Содержимое кейса/data_file.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)
data['cases_in'] = []
for file_name in os.listdir(os.getcwd())[2:]:
    files = {"file": open(file_name, "rb")}
    a = requests.post(url, headers={"Authorization": "OAuth AQAAAAAbmj-UAAT7o2_k9MfXh00huVG9-nCl1zg"},
                      files=files)
    data['cases_in'].append({'name': file_name[:-4]})
    if a.status_code == 201:
        id = a.json()["image"]["id"]
        data['cases_in'][-1]['src'] = id


with open("../resourses/Содержимое кейса/data_file.json", "w", encoding='utf-8') as write_file:
    json.dump(data, write_file, ensure_ascii=False)
