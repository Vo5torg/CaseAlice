from PIL import Image, ImageDraw
import os, json

background_old = Image.open('../resourses/Эффекты/background.jpg')
background = background_old.copy()
effect = Image.open("Армейское-эффект.png")
ammo_img = Image.open("AWP - Фобос.png")
ammo_img = ammo_img.resize((int(ammo_img.size[0] * 1.6), int(ammo_img.size[1] * 1.6)))
background.paste(effect, (450, 230), effect)
background.paste(ammo_img, (805, 470), ammo_img)
background = background.crop((730, 440, 1670, 1110))

background.save("хоп.jpg")
