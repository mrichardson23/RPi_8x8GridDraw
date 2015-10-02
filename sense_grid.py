# bookmarks http://www.one-tab.com/page/Ds6dSsBoSX24cD8OSxqKcA
import pygame
import sys
import math
from pygame.locals import *
from led import LED
from buttons import Button
import png # pypng
from sense_hat import AstroPi
import copy, time

saved = True
warning = False
pygame.init()
pygame.font.init()

ap=AstroPi()
screen = pygame.display.set_mode((500, 530), 0, 32)
pygame.display.set_caption('Sense HAT Grid Editor')
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 51, 25))
colour = (255,0,0) # Set default colour to red
rotation = 0
frame_number  = 1
fps = 4

colours = dict(
r = (255,0,0),
o = (255,128,0),
y = (255,255,0),
g = (0,255,0),
c = (0,255,255),
b = (0,0,255),
p = (102,0,204),
f = (255,0,255),
w = (255,255,255),
e = (0,0,0)
)

def setColourRed():
        global colour
        colour = (colours['r'])

def setColourBlue():
        global colour
        colour = (colours['b'])

def setColourGreen():
        global colour
        colour = (colours['g'])

def setColourPurple():
        global colour
        colour = (colours['p'])

        
def setColourPink():
	global colour 
	colour = (colours['f'])

def setColourYellow():
	global colour 
	colour = (colours['y'])

def setColourOrange():
	global colour 
	colour = (colours['o'])

def setColourWhite():
	global colour 
	colour = (colours['w'])

def setColourCyan():
	global colour 
	colour = (colours['c'])

def clearGrid(): # Clears the pygame LED grid and sets all the leds.lit back to False
	
	for led in leds:
		led.lit = False

def buildGrid(): # Takes a grid and builds versions for exporting (png and text)
    grid_letter=[]
    grid_rgb=[]

    for pos in range(64):
            grid_letter.append('e')
            grid_rgb.append((0,0,0))

    for led in leds:
        
        if led.lit:
                val = led.pos[0] + (8 * led.pos[1])
                grid_letter[val] = led.color_name
                grid_rgb[val] = (led.color)
    return (grid_letter, grid_rgb)



def piLoad(): # Loads image onto AstroPi matrix
	grid_letter, grid_rgb = buildGrid()
	ap.set_pixels(grid_rgb)

def exportGrid(): # Writes png to file

	global saved
	grid, png_grid = buildGrid()
	FILE=open('image8x8.png','wb')
	w = png.Writer(8,8)
	w.write(FILE,png_grid)
	FILE.close()
	saved = True

def rotate(): #Rotates image on AstroPi LED matrix
	global rotation
	if rotation == 270:
		rotation = 0
	else:
		rotation = rotation + 90
	ap.set_rotation(rotation)



def handleClick():
    
    global saved
    global warning
    
    pos = pygame.mouse.get_pos()
    led = findLED(pos, leds)
    if led:
        led.clicked(colour,colours)
        
        saved = False
    for butt in buttons:
        if butt.rect.collidepoint(pos):
            butt.click()
            #print 'button clicked'
    if warning:
        for butt in buttons_warn:
            if butt.rect.collidepoint(pos):
                butt.click()
				
 
def findLED(clicked_pos, leds): # reads leds and checks if clicked position is in one of them
	
	x = clicked_pos[0]
	y = clicked_pos[1]
	for led in leds:
		if math.hypot(led.pos_x - x, led.pos_y - y) <= led.radius:
			return led
			
	return None


def drawEverything():
	
	global warning
	screen.blit(background, (0, 0))
	#draw the leds
	for led in leds:
		led.draw()
	for button in buttons:
		button.draw(screen)
	font = pygame.font.Font(None,16)
	
	frame_text = 'Frame ' + str(frame_number) 
	text = font.render(frame_text,1,(255,255,255))
	screen.blit(text, (445,370))
	fps_text = 'Frame rate= ' + str(fps) +' fps' 
	text = font.render(fps_text,1,(255,255,255))
	screen.blit(text, (343,440))
	font = pygame.font.Font(None,18)
	export_text = 'Animation'
	text = font.render(export_text,1,(255,255,255))
	screen.blit(text, (30,440))
	export_text = 'Single Frame'
	text = font.render(export_text,1,(255,255,255))
	screen.blit(text, (130,440))
	pygame.draw.circle(screen,colour,(470,345),20,0)
	#flip the screen
	if warning:
		for button in buttons_warn:
			button.draw(screen)
	pygame.display.flip()

def load_leds_to_animation():

	global frame_number
	global leds
	for saved_led in animation[frame_number]:
				if saved_led.lit:
					for led in leds:
						if led.pos == saved_led.pos:
							led.color = saved_led.color
							led.lit = True

def nextFrame():
	
	global frame_number
	global leds
	animation[frame_number] = copy.deepcopy(leds)
	#clearGrid()
	frame_number+=1
	if frame_number in animation:
		leds =[]
		for x in range(0, 8):
			for y in range(0, 8):
				led = LED(pos=(x, y))
				leds.append(led)
		load_leds_to_animation()
			
	

def prevFrame():

	global frame_number
	global leds
	
	animation[frame_number] = copy.deepcopy(leds)
	clearGrid()
	if frame_number != 1:
		frame_number-=1
	if frame_number in animation:
		leds =[]
		for x in range(0, 8):
			for y in range(0, 8):
				led = LED(pos=(x, y))
				leds.append(led)
		load_leds_to_animation()

def delFrame():
	global frame_number
	
	if len(animation) > 1:
		animation[frame_number] = copy.deepcopy(leds)
		del animation[frame_number]
		prevFrame()		
		for shuffle_frame in range(frame_number+1,len(animation)):
			animation[shuffle_frame] = animation[shuffle_frame+1]
		del animation[len(animation)]
		


def getLitLEDs():

	points = []
	for led in leds:
		if led.lit:
			points.append(led.pos)
	return points

# Main program body - set up leds and buttons

leds = []
for x in range(0, 8):
	for y in range(0, 8):
		led = LED(pos=(x, y))
		leds.append(led)
buttons = []
buttons_warn = []
animation={}
#global frame_number

def play():
	
	global leds
	global frame_number
	animation[frame_number] = copy.deepcopy(leds)
	#print 'length of ani is ' + str(len(animation))
	for playframe in range(1,(len(animation)+1)):
		
		leds =[]
		for x in range(0, 8):
			for y in range(0, 8):
				led = LED(pos=(x, y))
				leds.append(led)
			for saved_led in animation[playframe]:
				if saved_led.lit:
					for led in leds:
						if led.pos == saved_led.pos:
							led.color = saved_led.color
							led.lit = True
		piLoad()
		time.sleep(1.0/fps)
		
def exportAni():
    global saved
    output=[]
    demo = ['## This demo program will show each frame for 1 second ##\n']
    
    output.extend(['from sense_hat import SenseHat\n','from time import sleep\n','sense=SenseHat()\n\n'])
    
    for color,name in zip(colours.keys(), colours.values()):
        output.append(str(color) + " = " + str(name)+"\n")
    output.append('\n\n\n')
    global leds
    global frame_number
    animation[frame_number] = copy.deepcopy(leds)
    for playframe in range(1,(len(animation)+1)):
        demo.append('sense.set_pixels(frame{0})\n'.format(playframe))
        demo.append('sleep(1)\n\n')
        
        output.append("frame{0} = [".format(playframe))
        leds =[]
        for x in range(0, 8):
            for y in range(0, 8):
                led = LED(pos=(x, y))
                leds.append(led)
            for saved_led in animation[playframe]:
                if saved_led.lit:
                    for led in leds:
                        if led.pos == saved_led.pos:
                            led.color = saved_led.color
                            led.lit = True
        grid, png_grid = buildGrid()
        output.append(",".join(str(value) for value in grid))
        output.append(']\n\n')
    output.extend(demo)
    output.append("\nsense.clear()")

    with open("sense_frames.py",mode="w") as f:
        for line in output:
                f.write(line)
    saved = True

def prog_exit():
	clearGrid()
	pygame.quit()
	sys.exit()





exportAniButton = Button('Export to py', action=exportAni,  pos=(10, 460), color=(153,0,0))
buttons.append(exportAniButton)

RotateButton = Button('Rotate LEDs', action=rotate,  pos=(230, 460), color=(205,255,255))
buttons.append(RotateButton)
clearButton = Button('Clear Grid', action=clearGrid,  pos=(230, 495), color=(204,255,255))
buttons.append(clearButton)

PlayButton = Button('Play on LEDs', action=play,  pos=(340, 495), color=(184,138,0))
buttons.append(PlayButton)

RedButton = Button('', action=setColourRed, size=(50,30), pos=(445, 10),hilight=(0, 200, 200),color=(255,0,0))
buttons.append(RedButton)
OrangeButton = Button('', action=setColourOrange, size=(50,30), pos=(445, 45),hilight=(0, 200, 200),color=(255,128,0))
buttons.append(OrangeButton)
YellowButton = Button('', action=setColourYellow, size=(50,30), pos=(445, 80),hilight=(0, 200, 200),color=(255,255,0))
buttons.append(YellowButton)
GreenButton = Button('', action=setColourGreen, size=(50,30), pos=(445, 115),hilight=(0, 200, 200),color=(0,255,0))
buttons.append(GreenButton)
CyanButton = Button('', action=setColourCyan, size=(50,30), pos=(445, 150),hilight=(0, 200, 200),color=(0,255,255))
buttons.append(CyanButton)
BlueButton = Button('', action=setColourBlue, size=(50,30), pos=(445, 185),hilight=(0, 200, 200),color=(0,0,255))
buttons.append(BlueButton)
PurpleButton = Button('', action=setColourPurple, size=(50,30), pos=(445, 220),hilight=(0, 200, 200),color=(102,0,204))
buttons.append(PurpleButton)
PinkButton = Button('', action=setColourPink, size=(50,30), pos=(445, 255),hilight=(0, 200, 200),color=(255,0,255))
buttons.append(PinkButton)
WhiteButton = Button('', action=setColourWhite, size=(50,30), pos=(445, 290),hilight=(0, 200, 200),color=(255,255,255))
buttons.append(WhiteButton)

PrevFrameButton = Button('<-', action=prevFrame, size=(25,25), pos=(442, 385), color=(184,138,0))
buttons.append(PrevFrameButton)
NextFrameButton = Button('->', action=nextFrame, size=(25,25), pos=(472, 385), color=(184,138,0))
buttons.append(NextFrameButton)

DelFrame = Button('Delete', action=delFrame, size=(50,25), pos=(445, 415), color=(184,138,0))
buttons.append(DelFrame)

#saveButton = Button('Save', action=save_it, size=(60,50), pos=(150, 180),hilight=(200, 0, 0),color=(255,255,0))
#buttons_warn.append(saveButton)
#QuitButton = Button('Quit', action=prog_exit, size=(60,50), pos=(260, 180),hilight=(200, 0, 0),color=(255,255,0))
#buttons_warn.append(QuitButton)


def nosave_warn():
	global warning
	warning = True
	font = pygame.font.Font(None,48)
	frame_text = 'Unsaved Frames ' 
	
	for d in range(5):
		text = font.render(frame_text,1,(255,0,0))
		screen.blit(text, (100,100))
		pygame.display.flip()
		time.sleep(0.1)
		text = font.render(frame_text,1,(0,255,0))
		screen.blit(text, (100,100))
		pygame.display.flip()
		time.sleep(0.1)
	drawEverything()
# Main prog loop


while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			if saved == False:
				nosave_warn()
			else:
				prog_exit()
		
		if event.type == MOUSEBUTTONDOWN:
			handleClick()

	#update the displayco
	drawEverything()

