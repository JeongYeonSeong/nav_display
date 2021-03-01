from PIL import Image, ImageDraw, ImageFont
from lib_oled96 import ssd1306
from time import sleep
from smbus import SMBus

def texts(direction, text):
    i2cbus = SMBus(1)
    oled = ssd1306(i2cbus)
    
    file_name = ''
    if direction == '1':
        file_name = 'up_arr.png'
    elif direction == '2':
        file_name = 'left_arr.png'
    elif direction == '3':
        file_name = 'right_arr.png'

    img = Image.open(file_name)
    draw_text = text
    font = ImageFont.truetype("Car_Num.ttf", 45)
    draw = ImageDraw.Draw(img)
    draw.text((64, 0), draw_text, 'black', font)
    
    img.save('print.png')

    logo = img.resize((128,32)).convert('1')
    oled.canvas.bitmap((0,0), logo, fill = 1)
    logo = Image.open('pi_logo.png').resize((128,32)).convert('1')
    oled.canvas.bitmap((0,33), logo, fill = 1)


    for i in range(90):
        oled.display()

    oled.cls()
    
texts('2','13d1323')

