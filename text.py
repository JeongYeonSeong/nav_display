from PIL import Image, ImageDraw, ImageFont
from lib_oled96 import ssd1306
from time import sleep
from smbus import SMBus
import socket

class display:
    def __init__(self):
        self.host = '192.168.0.32'
        self.port = 5001        
        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))
        self.text_queue1 = []
        self.text_queue2 = []
        self.delete_id = []
        self.connection()
        while 1:
            self.get_message()
            sleep(1)
        
    def connection(self):
        msg = '00'
        self.client_socket.send(msg.encode())
    
    def get_message(self):
        data = self.client_socket.recv(1024).decode()
        if not data:
            return
        data = data.split('/', 10)
        print(data)
        if data[0] == '':
            return False
        
        for i in data:
            print('datas :', i)
        
#         if data[2] == '9A':
#             self.text_queue1.append(data[0:2])
#         elif data[2] == '9B':
#             self.text_queue2.append(data[0:2])
        if data[0] == '0' and len(self.text_queue1) != 0:
            self.delete_id.append(data[1])
            data = self.text_queue1[0]
        else:
            checks = 0
            for count, i in enumerate(self.text_queue1):
                if i[1] == data[1]:
                    self.text_queue1[count] = data
                    checks = 1
                    break
            if checks == 0:            
                self.text_queue1.append(data)
        print(self.text_queue1)
            
        if len(self.text_queue1) >= 2:
            self.texts(int(1), self.text_queue1[0], self.text_queue1[0])
        elif len(self.text_queue1) == 1:
            text1 = self.text_queue1[0]
            print(text1)
            self.texts(int(1), text1)# self.text_queue1.pop(0))
        else:
            return False

        if len(self.text_queue2) >= 2:
            self.texts(2, self.text_queue2.pop(0), self.text_queue2[0])
        elif len(self.text_queue2) == 1:
            self.texts(2, self.text_queue2.pop(0))
        else:
            return False

    def texts(self, port, text1, text2=None):
        i2cbus = SMBus(port)
        oled = ssd1306(i2cbus)
        
        direction1 = text1[0]
        
        file_name = 'left_arr.png'
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
            if direction2 == '1':
                file_name = 'up_arr.png'
            elif direction2 == '2':
                file_name = 'left_arr.png'
            elif direction2 == '3':
                file_name = 'right_arr.png'
                
            img = Image.open(file_name)
            draw_text = text2[1]
            font = ImageFont.truetype("Car_Num.ttf", 45)
            draw = ImageDraw.Draw(img)
            draw.text((64, 0), draw_text, 'black', font)
                
            logo = img.resize((128,32)).convert('1')
            oled.canvas.bitmap((0,32), logo, fill = 1)
        else:
            img = Image.open('left_arr.png')
            draw_text = text1[2]
            
            if text1[1] in self.delete_id:
                self.text_queue1.pop(0)
                self.delete_id.remove(text1[1])
            print(self.text_queue1)
            font = ImageFont.truetype("Car_Num.ttf", 45)
            draw = ImageDraw.Draw(img)
            draw.text((64, 0), draw_text, 'black', font)
            
            logo = img.resize((128,32)).convert('1')
            oled.canvas.bitmap((0,32), logo, fill = 1)
        
        oled.display()
#         sleep(2)
    
program = display()