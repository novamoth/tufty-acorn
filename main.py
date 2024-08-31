# A retro badge with photo and QR code.
# Copy your image to your Tufty alongside this example - it should be a 120 x 120 jpg.

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import time
import jpegdec
import qrcode
import json

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
button_c = Button(9, invert=False)

WIDTH, HEIGHT = display.get_bounds()

f = open("system.json")
system = json.load(f)
f.close()

# Lava-GB color palette by Aero - https://lospec.com/palette-list/lava-gb
color_text = None
color_system_text = None
color_bg = None
color_system_bg = None
CCB_GREEN = display.create_pen(58, 181, 74)
CCB_YELLOW = display.create_pen(255, 240, 4)
CCB_RED = display.create_pen(238, 27, 36)
CCB_FILLING = display.create_pen(0, 0, 0)

# Change your badge and QR details here!
SYSTEM_NAME = system['name']
alterName = None
alterPronouns = None
alterDesc = None
imageName = None

# Some constants we'll use for drawing
PADDING = 6
COMPANY_HEIGHT = 40
# Removed since dynamic sizing makes it harder for users to know what to do
# IMAGE_SIZE = int((HEIGHT - COMPANY_HEIGHT - PADDING*3) / 2) # Resolves to 90
IMAGE_SIZE = 90

def hex_to_rgb(hexa):
    if hexa[0] == "#":
        hexa = hexa[1:7]
    return tuple(int(hexa[i:i+2], 16)  for i in (0, 2, 4))

def set_default_palette():
    global color_text
    global color_system_text
    global color_bg
    global color_system_bg
    # Lava-GB color palette by Aero - https://lospec.com/palette-list/lava-gb
    color_text = display.create_pen(255, 142, 128)
    color_system_text = display.create_pen(197, 58, 157)
    color_bg = display.create_pen(74, 36, 128)
    color_system_bg = display.create_pen(5, 31, 57)

def set_alter_values(alterIndex):
    global alterName
    global alterPronouns
    global alterDesc
    global imageName
    global color_text
    global color_system_text
    global color_bg
    global color_system_bg
    alterName = system["members"][alterIndex]["name"] or "Placeholder"
    alterPronouns = system["members"][alterIndex]["pronouns"] or "Placeholder"
    alterDesc = system["members"][alterIndex]["description"] or "Placeholder description! This alter does not have a description."
    try:
        with open(system["members"][alterIndex]["id"] + ".jpg", 'rb') as f:
            print("success!")
            imageName = system["members"][alterIndex]["id"] + ".jpg"
            f.close()
    except:
        print("No ID, falling back to name")
        try:
            with open(system["members"][alterIndex]["name"] + ".jpg", 'rb') as f:
                print("success with name!")
                imageName = system["members"][alterIndex]["name"] + ".jpg"
                f.close()
        except:
            print("failure with name, trying with all lowercase")
            try:
                with open(system["members"][alterIndex]["name"].lower() + ".jpg", 'rb') as f:
                    print("success with lowercase name!")
                    imageName = system["members"][alterIndex]["name"].lower() + ".jpg"
                    f.close()
            except:
                print("No icon provided, defaulting to placeholder")
                imageName = "placeholder.jpg"
    palette = None
    try:
        palette = system["members"][alterIndex]["palette"]
    except:
        set_default_palette()
        return
    if not palette:
        set_default_palette()
        return
    print(palette)
    rgbTuple = hex_to_rgb(palette["color_text"])
    color_text = display.create_pen(rgbTuple[0], rgbTuple[1], rgbTuple[2])
    palette = system["members"][alterIndex]["palette"]
    rgbTuple = hex_to_rgb(palette["color_system_text"])
    color_system_text = display.create_pen(rgbTuple[0], rgbTuple[1], rgbTuple[2])
    palette = system["members"][alterIndex]["palette"]
    rgbTuple = hex_to_rgb(palette["color_bg"])
    color_bg = display.create_pen(rgbTuple[0], rgbTuple[1], rgbTuple[2])
    palette = system["members"][alterIndex]["palette"]
    rgbTuple = hex_to_rgb(palette["color_system_bg"])
    color_system_bg = display.create_pen(rgbTuple[0], rgbTuple[1], rgbTuple[2])

def draw_badge():
    # draw background
    display.set_pen(color_bg)
    display.rectangle(0, 0, WIDTH, HEIGHT)

    # draw company box
    display.set_pen(color_system_bg)
    display.rectangle(0, 0, WIDTH, COMPANY_HEIGHT)

    # draw company text
    display.set_pen(color_system_text)
    display.set_font("bitmap6")
    display.text(SYSTEM_NAME, PADDING, PADDING, WIDTH, 3)

    # draw name text
    display.set_pen(color_text)
    display.set_font("bitmap8")
    display.text(alterName, PADDING * 3 + IMAGE_SIZE, PADDING*2 + COMPANY_HEIGHT, WIDTH, 5)
    
    # draw pronoun text
    display.set_pen(color_text)
    display.set_font("bitmap6")
    display.text(alterPronouns, PADDING * 3 + IMAGE_SIZE, PADDING*3 + COMPANY_HEIGHT + 8*5, WIDTH, 3)

    # draws the alter's description
    display.set_pen(color_text)
    display.text(alterDesc, PADDING * 3 + IMAGE_SIZE, PADDING*4 + COMPANY_HEIGHT + 8*5 + 3*6, 190, 2)


def show_photo():
    global imageName
    print(imageName)
    j = jpegdec.JPEG(display)

    # Open the JPEG file
    j.open_file(imageName)

    # Decode the JPEG
    j.decode(PADDING, COMPANY_HEIGHT + PADDING)
    #display.set_pen(color_text)
    #display.rectangle(PADDING, COMPANY_HEIGHT + PADDING, IMAGE_SIZE, IMAGE_SIZE)
    
def draw_ccb_green():
    # Draw CCB Color box
    display.set_pen(CCB_GREEN)
    display.rectangle(PADDING, HEIGHT - PADDING - IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE)
    
    # Draw CCB Symbol
    display.set_pen(CCB_FILLING)
    display.circle(PADDING + int(IMAGE_SIZE/2), HEIGHT - PADDING - int(IMAGE_SIZE/2), int(IMAGE_SIZE/2.5))
    
    # Draw interior symbol
    # display.set_pen(CCB_GREEN)
    # display.circle(PADDING + int(IMAGE_SIZE/2), HEIGHT - PADDING - int(IMAGE_SIZE/2), int(IMAGE_SIZE/3.5))
    
    
def draw_ccb_yellow():
    # Draw CCB Color box
    display.set_pen(CCB_YELLOW)
    display.rectangle(PADDING, HEIGHT - PADDING - IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE)
    
    # Draw CCB Symbol
    display.set_pen(CCB_FILLING)
    display.triangle(PADDING + int(IMAGE_SIZE/10), HEIGHT - PADDING - int(IMAGE_SIZE/10),
                     PADDING + int(IMAGE_SIZE/10*9), HEIGHT - PADDING - int(IMAGE_SIZE/10),
                     PADDING + int(IMAGE_SIZE/2), HEIGHT - PADDING - int(IMAGE_SIZE/10*9))
    
    # Draw interior symbol
#     display.set_pen(CCB_YELLOW)
#     display.triangle(PADDING + int(IMAGE_SIZE/5), HEIGHT - PADDING - int(IMAGE_SIZE/5),
#                      PADDING + int(IMAGE_SIZE/5*4), HEIGHT - PADDING - int(IMAGE_SIZE/5),
#                      PADDING + int(IMAGE_SIZE/2), HEIGHT - PADDING - int(IMAGE_SIZE/5*4))
    
def draw_ccb_red():
    # Draw CCB Color box
    display.set_pen(CCB_RED)
    display.rectangle(PADDING, HEIGHT - PADDING - IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE)
    
    # Draw CCB Symbol
    display.set_pen(CCB_FILLING)
    display.rectangle(PADDING + int(IMAGE_SIZE/6), HEIGHT - PADDING - IMAGE_SIZE + int(IMAGE_SIZE/6), int((IMAGE_SIZE / 3) *2 ), int((IMAGE_SIZE / 3) * 2))
    
    # Draw interior symbol
#     display.set_pen(CCB_RED)
#     display.rectangle(PADDING + int(IMAGE_SIZE/4), HEIGHT - PADDING - IMAGE_SIZE + int(IMAGE_SIZE/4), int(IMAGE_SIZE / 2), int(IMAGE_SIZE/2))

def draw_ccb(ccb):
    if ccb == "green":
        draw_ccb_green()
    elif ccb == "yellow":
        draw_ccb_yellow()
    elif ccb == "red":
        draw_ccb_red()

def redrawAll(ccb, alterIndex):
    set_alter_values(alterIndex)
    draw_badge()
    show_photo()
    draw_ccb(ccb)
    display.update()
    
# Default values
ccb = "green"
alterIndex = 0 # begin at the first alter
# draw the badge for the first time
redrawAll(ccb, alterIndex)

while True:
    if button_up.is_pressed:
        alterIndex-=1
        if(alterIndex < 0):
            alterIndex = len(system["members"])-1
        redrawAll(ccb,alterIndex)
        time.sleep(1)
    if button_down.is_pressed:
        alterIndex+=1
        if(len(system["members"]) <= alterIndex):
            alterIndex = 0
        redrawAll(ccb,alterIndex)
        time.sleep(1)
    if button_c.is_pressed:
        if ccb == "green":
            ccb = "yellow"
        elif ccb == "yellow":
            ccb = "red"
        elif ccb == "red":
            ccb = "green"
        draw_ccb(ccb)
        display.update()
        time.sleep(1)

