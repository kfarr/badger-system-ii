import badger_os
import badger2040
import time
import gc
from badger2040 import WIDTH

# for e.g. 2xAAA batteries, try max 3.4 min 3.0
MAX_BATTERY_VOLTAGE = 3.4
MIN_BATTERY_VOLTAGE = 3.0

font_table = {
  ' ': (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00 ), # 0x20    32    
  '!': (0x00,0x00,0x03,0x03,0x03,0x03,0x00,0x03,0x00,0x00 ), # 0x21    33    
  '"': (0x00,0x00,0x1B,0x1B,0x12,0x00,0x00,0x00,0x00,0x00 ), # 0x22    34    
  '#': (0x00,0x00,0x36,0x7F,0x36,0x36,0x7F,0x36,0x00,0x00 ), # 0x23    35    
  '$': (0x00,0x0C,0x3E,0x0F,0x1E,0x3C,0x3F,0x1E,0x0C,0x00 ), # 0x24    36    
  '%': (0x00,0x00,0x63,0x33,0x18,0x0C,0x66,0x63,0x00,0x00 ), # 0x25    37    
  '&': (0x00,0x00,0x1E,0x33,0x1E,0x3F,0x1B,0x3E,0x00,0x00 ), # 0x26    38    
  "'": (0x00,0x00,0x03,0x03,0x02,0x00,0x00,0x00,0x00,0x00 ), # 0x27    39    
  '(': (0x00,0x06,0x03,0x03,0x03,0x03,0x03,0x03,0x06,0x00 ), # 0x28    40    
  ')': (0x00,0x03,0x06,0x06,0x06,0x06,0x06,0x06,0x03,0x00 ), # 0x29    41    
  '*': (0x00,0x00,0x00,0x33,0x1E,0x1E,0x33,0x00,0x00,0x00 ), # 0x2A    42    
  '+': (0x00,0x00,0x0C,0x0C,0x3F,0x0C,0x0C,0x00,0x00,0x00 ), # 0x2B    43    
  ',': (0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x03,0x02,0x00 ), # 0x2C    44    
  '-': (0x00,0x00,0x00,0x00,0x3F,0x00,0x00,0x00,0x00,0x00 ), # 0x2D    45    
  '.': (0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x03,0x00,0x00 ), # 0x2E    46    
  '/': (0x00,0x40,0x60,0x30,0x18,0x0C,0x06,0x03,0x01,0x00 ), # 0x2F    47    
  '0': (0x00,0x00,0x1E,0x33,0x33,0x33,0x33,0x1E,0x00,0x00 ), # 0x30    48    
  '1': (0x00,0x00,0x06,0x07,0x06,0x06,0x06,0x0F,0x00,0x00 ), # 0x31    49    
  '2': (0x00,0x00,0x1E,0x33,0x30,0x1E,0x03,0x3F,0x00,0x00 ), # 0x32    50    
  '3': (0x00,0x00,0x1E,0x33,0x18,0x30,0x33,0x1E,0x00,0x00 ), # 0x33    51    
  '4': (0x00,0x00,0x18,0x1C,0x1E,0x1B,0x3F,0x18,0x00,0x00 ), # 0x34    52    
  '5': (0x00,0x00,0x3F,0x03,0x1F,0x30,0x33,0x1E,0x00,0x00 ), # 0x35    53    
  '6': (0x00,0x00,0x1E,0x03,0x1F,0x33,0x33,0x1E,0x00,0x00 ), # 0x36    54    
  '7': (0x00,0x00,0x3F,0x30,0x18,0x0C,0x0C,0x0C,0x00,0x00 ), # 0x37    55    
  '8': (0x00,0x00,0x1E,0x33,0x1E,0x33,0x33,0x1E,0x00,0x00 ), # 0x38    56    
  '9': (0x00,0x00,0x1E,0x33,0x33,0x3E,0x30,0x1E,0x00,0x00 ), # 0x39    57    
  ':': (0x00,0x00,0x00,0x03,0x03,0x00,0x03,0x03,0x00,0x00 ), # 0x3A    58    
  ';': (0x00,0x00,0x00,0x03,0x03,0x00,0x03,0x03,0x02,0x00 ), # 0x3B    59    
  '<': (0x00,0x18,0x0C,0x06,0x03,0x06,0x0C,0x18,0x00,0x00 ), # 0x3C    60    
  '=': (0x00,0x00,0x00,0x3F,0x00,0x3F,0x00,0x00,0x00,0x00 ), # 0x3D    61    
  '>': (0x00,0x03,0x06,0x0C,0x18,0x0C,0x06,0x03,0x00,0x00 ), # 0x3E    62    
  '?': (0x00,0x00,0x1E,0x33,0x18,0x0C,0x00,0x0C,0x00,0x00 ), # 0x3F    63    
  '@': (0x7E,0xC3,0x3B,0xEF,0xEF,0xFB,0xC3,0x7E,0x00,0x00 ), # 0x40    64    
  'A': (0x00,0x00,0x1E,0x33,0x33,0x3F,0x33,0x33,0x00,0x00 ), # 0x41    65    
  'B': (0x00,0x00,0x1F,0x33,0x1F,0x33,0x33,0x1F,0x00,0x00 ), # 0x42    66    
  'C': (0x00,0x00,0x1E,0x33,0x03,0x03,0x33,0x1E,0x00,0x00 ), # 0x43    67    
  'D': (0x00,0x00,0x1F,0x33,0x33,0x33,0x33,0x1F,0x00,0x00 ), # 0x44    68    
  'E': (0x00,0x00,0x3F,0x03,0x0F,0x03,0x03,0x3F,0x00,0x00 ), # 0x45    69    
  'F': (0x00,0x00,0x3F,0x03,0x0F,0x03,0x03,0x03,0x00,0x00 ), # 0x46    70    
  'G': (0x00,0x00,0x1E,0x33,0x03,0x3B,0x33,0x1E,0x00,0x00 ), # 0x47    71    
  'H': (0x00,0x00,0x33,0x33,0x3F,0x33,0x33,0x33,0x00,0x00 ), # 0x48    72    
  'I': (0x00,0x00,0x0F,0x06,0x06,0x06,0x06,0x0F,0x00,0x00 ), # 0x49    73    
  'J': (0x00,0x00,0x30,0x30,0x30,0x30,0x33,0x1E,0x00,0x00 ), # 0x4A    74    
  'K': (0x00,0x00,0x33,0x1B,0x0F,0x0F,0x1B,0x33,0x00,0x00 ), # 0x4B    75    
  'L': (0x00,0x00,0x03,0x03,0x03,0x03,0x03,0x3F,0x00,0x00 ), # 0x4C    76    
  'M': (0x00,0x00,0xC3,0xE7,0xFF,0xDB,0xC3,0xC3,0x00,0x00 ), # 0x4D    77    
  'N': (0x00,0x00,0x33,0x37,0x3F,0x3B,0x33,0x33,0x00,0x00 ), # 0x4E    78    
  'O': (0x00,0x00,0x1E,0x33,0x33,0x33,0x33,0x1E,0x00,0x00 ), # 0x4F    79    
  'P': (0x00,0x00,0x1F,0x33,0x33,0x1F,0x03,0x03,0x00,0x00 ), # 0x50    80    
  'Q': (0x00,0x00,0x1E,0x33,0x33,0x33,0x1B,0x36,0x00,0x00 ), # 0x51    81    
  'R': (0x00,0x00,0x1F,0x33,0x33,0x1F,0x1B,0x33,0x00,0x00 ), # 0x52    82    
  'S': (0x00,0x00,0x1E,0x03,0x1E,0x30,0x33,0x1E,0x00,0x00 ), # 0x53    83    
  'T': (0x00,0x00,0x3F,0x0C,0x0C,0x0C,0x0C,0x0C,0x00,0x00 ), # 0x54    84    
  'U': (0x00,0x00,0x33,0x33,0x33,0x33,0x33,0x1E,0x00,0x00 ), # 0x55    85    
  'V': (0x00,0x00,0x33,0x33,0x33,0x33,0x1E,0x0C,0x00,0x00 ), # 0x56    86    
  'W': (0x00,0x00,0xC3,0xDB,0xDB,0xDB,0xDB,0x7E,0x00,0x00 ), # 0x57    87    
  'X': (0x00,0x00,0x33,0x1E,0x0C,0x0C,0x1E,0x33,0x00,0x00 ), # 0x58    88    
  'Y': (0x00,0x00,0x33,0x33,0x33,0x1E,0x0C,0x0C,0x00,0x00 ), # 0x59    89    
  'Z': (0x00,0x00,0x3F,0x38,0x1C,0x0E,0x07,0x3F,0x00,0x00 ), # 0x5A    90    
  '[': (0x00,0x0F,0x03,0x03,0x03,0x03,0x03,0x03,0x0F,0x00 ), # 0x5B    91    
  '\\': (0x00,0x01,0x03,0x06,0x0C,0x18,0x30,0x60,0x40,0x00 ), # 0x5C    92    
  ']': (0x00,0x0F,0x0C,0x0C,0x0C,0x0C,0x0C,0x0C,0x0F,0x00 ), # 0x5D    93    
  '^': (0x00,0x00,0x0C,0x1E,0x33,0x00,0x00,0x00,0x00,0x00 ), # 0x5E    94    
  '_': (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3F,0x00 ), # 0x5F    95    
  '`': (0x00,0x00,0x03,0x03,0x02,0x00,0x00,0x00,0x00,0x00 ), # 0x60    96    
  'a': (0x00,0x00,0x00,0x1E,0x30,0x3E,0x33,0x3E,0x00,0x00 ), # 0x61    97    
  'b': (0x00,0x00,0x03,0x1F,0x33,0x33,0x33,0x1F,0x00,0x00 ), # 0x62    98    
  'c': (0x00,0x00,0x00,0x1E,0x33,0x03,0x33,0x1E,0x00,0x00 ), # 0x63    99    
  'd': (0x00,0x00,0x30,0x3E,0x33,0x33,0x33,0x3E,0x00,0x00 ), # 0x64    100   
  'e': (0x00,0x00,0x00,0x1E,0x33,0x1F,0x03,0x1E,0x00,0x00 ), # 0x65    101   
  'f': (0x00,0x00,0x0E,0x03,0x0F,0x03,0x03,0x03,0x00,0x00 ), # 0x66    102   
  'g': (0x00,0x00,0x00,0x3E,0x33,0x33,0x3E,0x30,0x1E,0x00 ), # 0x67    103   
  'h': (0x00,0x00,0x03,0x1F,0x33,0x33,0x33,0x33,0x00,0x00 ), # 0x68    104   
  'i': (0x00,0x00,0x03,0x00,0x03,0x03,0x03,0x03,0x00,0x00 ), # 0x69    105   
  'j': (0x00,0x00,0x06,0x00,0x06,0x06,0x06,0x06,0x03,0x00 ), # 0x6A    106   
  'k': (0x00,0x00,0x03,0x33,0x1B,0x0F,0x1B,0x33,0x00,0x00 ), # 0x6B    107   
  'l': (0x00,0x00,0x03,0x03,0x03,0x03,0x03,0x06,0x00,0x00 ), # 0x6C    108   
  'm': (0x00,0x00,0x00,0x7F,0xDB,0xDB,0xDB,0xDB,0x00,0x00 ), # 0x6D    109   
  'n': (0x00,0x00,0x00,0x1F,0x33,0x33,0x33,0x33,0x00,0x00 ), # 0x6E    110   
  'o': (0x00,0x00,0x00,0x1E,0x33,0x33,0x33,0x1E,0x00,0x00 ), # 0x6F    111   
  'p': (0x00,0x00,0x00,0x1F,0x33,0x33,0x33,0x1F,0x03,0x00 ), # 0x70    112   
  'q': (0x00,0x00,0x00,0x3E,0x33,0x33,0x33,0x3E,0x30,0x00 ), # 0x71    113   
  'r': (0x00,0x00,0x00,0x0E,0x03,0x03,0x03,0x03,0x00,0x00 ), # 0x72    114   
  's': (0x00,0x00,0x00,0x1E,0x03,0x1E,0x30,0x1F,0x00,0x00 ), # 0x73    115   
  't': (0x00,0x00,0x06,0x0F,0x06,0x06,0x06,0x0C,0x00,0x00 ), # 0x74    116   
  'u': (0x00,0x00,0x00,0x33,0x33,0x33,0x33,0x1E,0x00,0x00 ), # 0x75    117   
  'v': (0x00,0x00,0x00,0x33,0x33,0x33,0x1E,0x0C,0x00,0x00 ), # 0x76    118   
  'w': (0x00,0x00,0x00,0xC3,0xDB,0xDB,0xDB,0x7E,0x00,0x00 ), # 0x77    119   
  'x': (0x00,0x00,0x00,0x33,0x1E,0x0C,0x1E,0x33,0x00,0x00 ), # 0x78    120   
  'y': (0x00,0x00,0x00,0x33,0x33,0x33,0x3E,0x30,0x1E,0x00 ), # 0x79    121   
  'z': (0x00,0x00,0x00,0x3F,0x18,0x0C,0x06,0x3F,0x00,0x00 ), # 0x7A    122   
  '(': (0x00,0x0C,0x06,0x06,0x03,0x03,0x06,0x06,0x0C,0x00 ), # 0x7B    123   
  '|': (0x00,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x00 ), # 0x7C    124   
  ')': (0x00,0x03,0x06,0x06,0x0C,0x0C,0x06,0x06,0x03,0x00 ), # 0x7D    125   
  '~': (0x00,0x00,0x00,0x00,0x6E,0x3B,0x00,0x00,0x00,0x00 )  # 0x7E    126   
}

def reverse_mask(x):
    x = ((x & 0x55) << 1) | ((x & 0xAA) >> 1)
    x = ((x & 0x33) << 2) | ((x & 0xCC) >> 2)
    x = ((x & 0x0F) << 4) | ((x & 0xF0) >> 4)
    return x

def get_char(c):
    try:
        char = font_table[c]
    except KeyError:
        print(f"Unrecognized char: {c}")
        char = font_table[" "]
    return char
            
def plength(para):
    # This could be precalculated, but I am lazy
    total = 0
    for c in para:
        char = get_char(c)
        width = sum(1 for i in [sum(1 for i in [x & mask for x in char] if i > 0) for mask in [128, 64, 32, 16, 8, 4, 2, 1]] if i > 0)
        total += 5 if width == 0 else width + 1
    return total

def pprint(display, para, x, y, col):
    offset = 0
    display.thickness(1)

    if col == 0:
        display.pen(15)
    else:
        display.pen(0)

    for c in para:
        if col == 1:
            char = [~x & 0xFF for x in get_char(c)]
        else:
            char = get_char(c)
            
        display.image(bytearray([reverse_mask(x) for x in char]), 8, 10, x + offset, y)
        display.rectangle(x + offset - 1, y, 1, 10)

        offset += plength(c)
        
def ppara(display, para, x, y, width, col):
    line = ""
    base_x = x
    length = 0
    for c in para:
        clength = plength(c)
        if clength + length > width:
            pprint(display, line, x, y, col)
            y += 10
            length = 0
            x = base_x
            line = ""

        length += clength
        line += c

    pprint(display, line, x, y, col)

def ptitle(display, para, x, y, col):
    pprint(display, para, x, y, 0)
    
    display.thickness(2)
    display.pen(0)
    display.line(x, y + 10, x + plength(para), y + 10)

def draw_background(display):
    display.pen(0)
    display.thickness(1)

    for y in range(11, 63):
        for x in range(1, 147, 2):
            display.rectangle(x * 2 + (2 if y % 2 == 0 else 0), y * 2, 2, 2)

#     image = bytearray(int(296 * 128 / 8))
#     open("images/{}".format("background.bin"), "r").readinto(image)
#     display.image(image, 296, 128, 0, 0)

def draw_menu(display, selected):
    menu = "Badge    QR    Special    About"

    # logo
    display.pen(0)
    display.thickness(1)
    
    # logo
    image = bytearray(int(16 * 16 / 8))
    open("images/{}".format("vimeo16.bin"), "r").readinto(image)
    display.image(image, 16, 16, 9, 3)    

    x = 40
    pprint(display, menu, x, 6, 0)
    
    # selected
    display.pen(0)
    offset = plength(menu.split(selected)[0])
    display.rectangle(x + offset - 7, 3, plength(selected) + 13, 17)
    pprint(display, selected, x + offset, 6, 1)
   
    display.pen(0)
    display.thickness(2)
    display.line(1, 21, 295, 21)
    
def draw_border(display):
    display.pen(0)
    display.thickness(2)
    
    display.line(1,   1,   295, 1)
    display.line(1,   1,   1,   127)
    display.line(1,   127, 295, 127)
    display.line(295, 1,   295, 127)
    display.image(bytearray((0xff, 0xff, 0xfc, 0xf8, 0xf0, 0xe0, 0xc0, 0xc0)), 8, 8, 0, 0)
    display.image(bytearray((0xff, 0xff, 0x3f, 0x1f, 0x0f, 0x07, 0x03, 0x03)), 8, 8, 288, 0)
    display.image(bytearray((0x03, 0x03, 0x07, 0x0f, 0x1f, 0x3f, 0xff, 0xff)), 8, 8, 288, 120)
    display.image(bytearray((0xc0, 0xc0, 0xe0, 0xf0, 0xf8, 0xfc, 0xff, 0xff)), 8, 8, 0, 120)

def map_value(input, in_min, in_max, out_min, out_max):
    return (((input - in_min) * (out_max - out_min)) / (in_max - in_min)) + out_min

def draw_battery(display, x, y):
    vbat = badger_os.get_battery_level()
    level = int(map_value(vbat, MIN_BATTERY_VOLTAGE, MAX_BATTERY_VOLTAGE, 0, 4))
    
    # Outline
    display.thickness(1)
    display.pen(15)
    display.rectangle(x, y, 19, 10)
    
    # Terminal
    display.rectangle(x + 19, y + 3, 2, 4)
    display.pen(0)
    display.rectangle(x + 1, y + 1, 17, 8)
    if level < 1:
        display.pen(0)
        display.line(x + 3, y, x + 3 + 10, y + 10)
        display.line(x + 3 + 1, y, x + 3 + 11, y + 10)
        display.pen(15)
        display.line(x + 2 + 2, y - 1, x + 4 + 12, y + 11)
        display.line(x + 2 + 3, y - 1, x + 4 + 13, y + 11)
        return
        
    # Battery Bars
    display.pen(15)
    for i in range(4):
        if level / 4 > (1.0 * i) / 4:
            display.rectangle(i * 4 + x + 2, y + 2, 3, 6)

def draw_window(display, x, y, width, height, title):
    display.thickness(1)
    
    # borders
    display.pen(15)
    display.rectangle(x, y, width, height)
    
    display.pen(0)
    display.line(x, y, x + width - 1, y)
    display.line(x, y, x, y + height - 1)
    display.line(x, y + height - 1, x + width - 1, y + height - 1)
    display.line(x + width - 1, y, x + width - 1, y + height - 1)
    
    # shadow
    display.line(x, y + height, x + width + 1, y + height)
    display.line(x + width, y, x + width, y + height + 1)
    display.line(x + 1, y + height + 1, x + width + 1, y + height + 1)
    display.line(x + width + 1, y + 1, x + width + 1, y + height + 1)

    # title
    display.line(x + 4, y + 3, x + width - 4, y + 3)
    display.line(x + 4, y + 5, x + width - 4, y + 5)
    display.line(x + 4, y + 7, x + width - 4, y + 7)

    display.line(x, y + 11, x + width, y + 11)
    display.line(x, y + 11, x + width, y + 11)
    
    pprint(display, title, (x + x + width - plength(title)) // 2, y + 1, 0)        
    
def wait_for_user_to_release_buttons(display):
    pr = display.pressed
    while pr(badger2040.BUTTON_A) or pr(badger2040.BUTTON_B) or pr(badger2040.BUTTON_C) or pr(badger2040.BUTTON_UP) or pr(badger2040.BUTTON_DOWN):
        time.sleep(0.01)

def launch_app(display, file):
    wait_for_user_to_release_buttons(display)

    for k in locals().keys():
        if k not in ("gc", "file", "badger_os"):
            del locals()[k]
    gc.collect()
    badger_os.launch(file)

def button(display, pin):
    if not display.pressed(badger2040.BUTTON_USER):  # User button is NOT held down
        if pin == badger2040.BUTTON_A:
            launch_app(display, "_badge_app")
        if pin == badger2040.BUTTON_B:
            launch_app(display, "_qr_app")
        if pin == badger2040.BUTTON_C:
            launch_app(display, "_fortune_app")
            
def draw_ui(display, selected):
    draw_border(display)
    draw_menu(display, selected)
    draw_background(display)
    draw_battery(display, WIDTH - 28, 6)