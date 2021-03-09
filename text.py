from Adafruit_GPIO import I2C
from lib_oled96 import ssd1306
from time import sleep
from smbus import SMBus
from PIL import Image, ImageDraw, ImageFont
import socket

class Display:
    def __init__(self):
        self.host = '192.168.0.32'
        self.port = 5001
        self.client_socket = socket.socket()
        while 1:
            try:
                print('trying connecting to server')
                self.client_socket.connect((self.host, self.port))
                break
            except:
                sleep(3)

        self.connection()
        # init disp connecting
        self.init_tca()
        while 1:
            
            self.get_message()
            break
            

    def tca_select(self, channel):
        if channel > 7:
            return
        self.tca.writeRaw8(1 << channel)
        
    def tca_set(self, mask):
        if mask > 0xff:
            return
        self.tca.writeRaw8(mask)

    def init_tca(self):
        self.tca = I2C.get_i2c_device(address=0x70)
        
        self.tca_select(0)
        self.tca_select(1)
        
        
        self.select_disp('all disp mobilize')
        self.texts([1,'fuck'])

    def select_disp(self, disp_num):
        if disp_num == 1:
            self.tca_set(0b00000001)
        elif disp_num == 2:
            self.tca_set(0b00000010)
        elif disp_num == 3:
            self.tca_set(0b00000100)
        elif disp_num == 4:
            self.tca_set(0b00001000)
        elif disp_num == 5:
            self.tca_set(0b00010000)
        elif disp_num == 6:
            self.tca_set(0b00100000)
        else:
            self.tca_set(0b00111111)

    def connection(self):
        msg = '00'
        self.client_socket.send(msg.encode())

    def get_message(self):
        data = self.client_socket.recv(1024).decode()
        if not data:
            return
        
        data = data.split('/', 10)
        print(data)
        
        #disp1
#         if data[0] == '':
#             return False
#         if data[2] == '3A':
#             self.tca_set(1)
#         elif data[2] == '3B':
#             self.tca_set(2)
#         elif data[2] == '9A':
#             self.tca_set(3)
#         elif data[2] == '9B':
#             self.tca_set(4)
#         elif data[2] == '11A':
#             self.tca_set(5)
#         elif data[2] == '11B':
#             self.tca_set(6)

        # disp 2
        if data[0] == '':
            return False
        if data[2] == '13A':
            self.tca_set(1)
        elif data[2] == '13B':
            self.tca_set(2)
        elif data[2] == '19A':
            self.tca_set(3)
        elif data[2] == '19B':
            self.tca_set(4)
            
        if data[0] == '0':
        # 0 two times => delete oled
            pass
        else:
        # displaying
            self.texts(data)

    def texts(self, text1, text2=None):
        self.i2cbus2 = SMBus(1)
        self.oled = ssd1306(self.i2cbus2)
        
        direction1 = str(text1[0])
        file_name = 'left_arr.png'
        if direction1 == '1':
            file_name = 'left_arr.png'
        elif direction1 == '2':
            file_name = 'up_arr.png'
        elif direction1 == '3':
            file_name = 'right_arr.png'
        
        img = Image.open(file_name)
        draw_text = str(text1[1])
        font = ImageFont.truetype("Car_Num.ttf", 45)
        draw = ImageDraw.Draw(img)
        draw.text((64, 0), draw_text, 'black', font)
        
        flip1 = img.transpose(Image.FLIP_LEFT_RIGHT)
        result = flip1.transpose(Image.FLIP_TOP_BOTTOM)

        img.save('fuck.png')

        displaying = result.resize((128,32)).convert('1')
        self.oled.canvas.bitmap((0,32), displaying, fill = 1)
        self.oled.display()

display = Display()
