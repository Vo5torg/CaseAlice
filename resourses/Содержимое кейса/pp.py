from PIL import Image, ImageDraw
import os

files = os.listdir(os.getcwd())

for file_name in files[1:]:
    ammo_img = Image.open(file_name)
    ammo_img = ammo_img.crop((220, 173, 1180, 640))
    ammo_img.save(file_name)

