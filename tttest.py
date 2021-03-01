from PIL import Image, ImageDraw, ImageFont
from lib_oled96 import ssd1306
from time import sleep
from smbus import SMBus

def texts(port, text1, text2=None):
    i2cbus = SMBus(port)
    oled = ssd1306(i2cbus)
    
    direction1 = text1[0]
    
    file_name = ''
    if direction1 == '1':
        file_name = 'left_arr.png'
    elif direction1 == '2':
        file_name = 'up_arr.png'
    elif direction1 == '3':
        file_name  = 'right_arr.png'

    img = Image.open(file_name)
    draw_text = text1[1]
    font = ImageFont.truetype("Car_Num.ttf", 45)
    draw = ImageDraw.Draw(img)
    draw.text((64, 0), draw_text, 'black', font)
    
    logo = img.resize((128,32)).convert('1')
    oled.canvas.bitmap((0,0), logo, fill = 1)
    
    if text2 != None:
        direction2 = text2[0]
        file_name = ''
        if direction1 == '1':
            file_name = 'up_arr.png'
        elif direction1 == '2':
            file_name = 'left_arr.png'
        elif direction1 == '3':
            file_name = 'right_arr.png'
            
        img = Image.open(file_name)
        draw_text = text2[1]
        font = ImageFont.truetype("Car_Num.ttf", 45)
        draw = ImageDraw.Draw(img)
        draw.text((64, 0), draw_text, 'black', font)
        
        
        logo = img.resize((128,32)).convert('1')
        oled.canvas.bitmap((0,32), logo, fill = 1)

    oled.display()
#         sleep(2)
    
texts(1, ['1', '37n9444', 3])