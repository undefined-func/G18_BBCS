#----Snippet for OLED----
from microbit import i2c, Image

OLED_ADDR = 0x3c
oled_screen = bytearray('b\x40') + bytearray(512)

def oled_initialize():
    for c in ([0xae], [0xa4], [0xd5, 0xf0], [0xa8, 0x3f], [0xd3, 0x00], [0 | 0x0], [0x8d, 0x14], [0x20, 0x00], [0x21, 0, 127], [0x22, 0, 63], [0xa0 | 0x1], [0xc8], [0xda, 0x12], [0x81, 0xcf], [0xd9, 0xf1], [0xdb, 0x40], [0xa6], [0xd6, 1], [0xaf]):
        i2c.write(OLED_ADDR, b'\x00' + bytearray(c))

def oled_set_pos(col=0, page=0):
    i2c.write(OLED_ADDR, b'\x00' + bytearray([0xb0 | page]))
    c1, c2 = col * 2 & 0x0F, col >> 3
    i2c.write(OLED_ADDR, b'\x00' + bytearray([0x00 | c1]))
    i2c.write(OLED_ADDR, b'\x00' + bytearray([0x10 | c2]))

def oled_clear_screen(c=0):
    global oled_screen
    oled_set_pos()
    for i in range(1, 513):
        oled_screen[i] = 0
    oled_draw_screen()

def oled_draw_screen():
    global oled_screen
    oled_set_pos()
    i2c.write(OLED_ADDR, oled_screen)

def oled_add_text(x, y, text):
    global oled_screen
    for i in range(0, min(len(text), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                p = Image(text[i]).get_pixel(c, r - 1)
                col = col | (1 << r) if (p != 0) else col
            ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
            oled_screen[ind], oled_screen[ind + 1] = col, col
    oled_set_pos(x * 5, y)
    ind0 = x * 10 + y * 128 + 1
    i2c.write(OLED_ADDR, b'\x40' + oled_screen[ind0 : (ind+1)])

oled_initialize()
oled_clear_screen()
oled_add_text(0,0,"Start")

#----My Code----
from microbit import *

def control(x): #user-defined function to set the brightness of LED display light
    light=[x for i in range (5)]
    img=((''.join(light)+":")*5)[0:-1]
    img=Image(img)
    display.show(img)
   
mode=0 
while True:
    mode +=button_a.get_presses() # odd = manual, even = auto
    if mode%2==0: #mode=auto
        oled_clear_screen()
        oled_add_text(0,0,'Automatic')
        reading_photoresistor=pin2.read_analog()//114 #floor division to make into int
        reading_motion=pin1.read_digital()
        brightness=9-reading_photoresistor
        if reading_motion==0 and brightness > 5: #no motion
            brightness=5 #cap brightness at 5 if there is no motion
    else: #mode=manual
        oled_clear_screen()
        oled_add_text(0,1,'Manual')
        reading_potentiometer=pin0.read_analog()
        brightness=reading_potentiometer//114 #floor division to make into int
    brightness=str(brightness)
    control(brightness)
        
   
