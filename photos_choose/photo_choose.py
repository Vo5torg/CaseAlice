from PIL import Image, ImageDraw
import os, json

with open("../case_skill/data_file.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)
secret_effect = Image.open('../resourses/Эффекты/Тайное-эффект.png')
prom_effect = Image.open('../resourses/Эффекты/Промышленное-эффект.png')
contr_effect = Image.open('../resourses/Эффекты/Контрабандное-эффект.png')
army_effect = Image.open('../resourses/Эффекты/Армейское-эффект.png')
zapr_effect = Image.open('../resourses/Эффекты/Запрещённое-эффект.png')
zasecr_effect = Image.open('../resourses/Эффекты/Засекреченное-эффект.png')

typess = {
    'Экстраординарного типа': contr_effect,
    'Запрещенное': zapr_effect,
    'Засекреченное': zasecr_effect,
    'Армейское': army_effect,
    'Тайное': secret_effect,
    'Промышленное': prom_effect,
}

background_old = Image.open('../resourses/Эффекты/background.jpg')

path_full = "C:/Users/ilyam/PycharmProjects/CaseAlice/resources_full/"
os.chdir('../resourses')

for i in [x[0] for x in os.walk(os.getcwd())][1:]:
    if 'Кейсы' in i or "Эффекты" in i:
        continue
    os.chdir(i)
    files = os.listdir(os.getcwd())
    direct_name = os.path.basename(i)
    print(direct_name)
    try:
        for file_name in files:
            ammo_img = Image.open(file_name)
            for ammo in data['info']:
                if file_name[:-4] in ammo['name']:
                    background = background_old.copy()
                    effect = typess[ammo["type"]]
                    ammo_img = ammo_img.resize((int(ammo_img.size[0] * 1.4), int(ammo_img.size[1] * 1.4)))
                    background.paste(effect, (615, 370), effect)
                    background.paste(ammo_img, (970, 650), ammo_img)
                    # background = background.crop((730, 440, 1670, 1110))
                    background = background.crop((860, 570, 1800, 1240))
                    print(file_name)
                    background.save(path_full + direct_name + "/" + file_name)



    except FileExistsError:
        continue
