from PIL import Image, ImageDraw
import os, json

os.chdir('../resourses/Кейсы')
files = os.listdir(os.getcwd())
for file_name in files:
    case_img = Image.open(file_name).convert("RGBA")

    background = Image.new('RGB', (case_img.size[0] + 100, case_img.size[1] + 100), (255, 255, 255))
    background.paste(case_img, (50, 0), case_img)
    background.save('../Кейсы_/' + file_name[:-4] + '.png')
