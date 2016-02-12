# -*- coding: utf-8 -*-

# bookmarks http://www.one-tab.com/page/Ds6dSsBoSX24cD8OSxqKcA
import pygame
import sys
import math
from pygame.locals import *
from led import LED
from buttons import Button
#import png # pypng
from sense_hat import AstroPi
import copy, time
import subprocess

saved = True
warning = False
animation_process = None
pygame.init()
pygame.font.init()

ap=AstroPi()
screen = pygame.display.set_mode((540, 550), 0, 32)
pygame.display.set_caption('Sense HAT Grid Editor')
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((80, 80, 80))
colour = (255,0,0) # Set default colour to red
rotation = 0
frame_number  = 1
fps = 4

def setColourRed():
	global colour 
	colour = (255,0,0)

def setColourBlue():
	global colour 
	colour = (0,0,255)

def setColourGreen():
	global colour 
	colour = (0,255,0)

def setColourPurple():
	global colour 
	colour = (102,0,204)

def setColourPink():
	global colour 
	colour = (255,0,255)

def setColourYellow():
	global colour 
	colour = (255,255,0)

def setColourOrange():
	global colour 
	colour = (255,128,0)

def setColourWhite():
	global colour 
	colour = (255,255,255)

def setColourCyan():
	global colour 
	colour = (0,255,255)

def clearGrid(): # Clears the pygame LED grid and sets all the leds.lit back to False
	for led in leds:
		led.lit = False

def buildGrid(): # Takes a grid and builds versions for exporting (png and text)

	e = [0,0,0]
	e_png = (0,0,0)

	grid = [
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e
	]
	#png_grid =[]

	png_grid = ['blank','blank','blank','blank','blank','blank','blank','blank']
	for led in leds:
		if led.lit:
			val = led.pos[0] + (8 * led.pos[1])
			#print val
			grid[val] = [led.color[0], led.color[1], led.color[2]]
			if png_grid[led.pos[0]] == 'blank':
				png_grid[led.pos[0]] = (led.color[0], led.color[1], led.color[2])
			else:
				png_grid[led.pos[0]] = png_grid[led.pos[0]] + (led.color[0], led.color[1], led.color[2])
		else: 
			if png_grid[led.pos[0]] == 'blank':
				png_grid[led.pos[0]] = (0,0,0)
			else:
				png_grid[led.pos[0]] = png_grid[led.pos[0]] + (0,0,0)
	return (grid, png_grid)

def piLoad(): # Loads image onto AstroPi matrix
	grid, grid_png = buildGrid()
	ap.set_pixels(grid)

def exportCons(): # Writes raw list to console

	grid, png_grid = buildGrid()
	print(grid)

def handleClick():
   
	global saved
	global warning
	pos = pygame.mouse.get_pos()
	led = findLED(pos, leds)
	if led:
		#print 'led ' + str(led) + ' clicked'
		led.clicked(colour)
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
			#print 'hit led'
	return None


def drawEverything():
	
	global warning
	screen.blit(background, (0, 0))
	#draw the leds
	for led in leds:
		led.draw()
	for button in buttons:
		button.draw(screen)
	font = pygame.font.Font(None,26)
	
	frame_text = 'Frame ' + str(frame_number) 
	text = font.render(frame_text,1,(255,255,255))
	screen.blit(text, (20,460))
	font = pygame.font.Font(None,18)
	pygame.draw.circle(screen,colour,(500,375),20,0)
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
	#print(frame_number)
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
	#print(frame_number)
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

def start_animation():
	global animation_process
	global saved
	FILE=open('/home/pi/RPi_8x8GridDraw/animation8x8.py','wb')
	FILE.write('from sense_hat import AstroPi\n')
	FILE.write('import time\n')
	FILE.write('ap=AstroPi()\n')
	FILE.write('FRAMES = [\n')
	global leds
	global frame_number
	animation[frame_number] = copy.deepcopy(leds)
	#print 'length of ani is ' + str(len(animation))
	for playframe in range(1,(len(animation)+1)):
		#print(playframe) 
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
		
		FILE.write(str(grid))
		FILE.write(',\n')
	FILE.write(']\n')
	FILE.write('while True:\n')
	FILE.write('\tfor x in FRAMES:\n')
	FILE.write('\t\tap.set_pixels(x)\n')
	FILE.write('\t\ttime.sleep('+ str(1.0/fps) + ')\n')
	FILE.close()
	saved = True
	if animation_process is not None:
		animation_process.terminate()
	animation_process = subprocess.Popen(["python", "/home/pi/RPi_8x8GridDraw/animation8x8.py"])

def prog_exit():
	print('exit clicked')
	global warning
	warning = False
	clearGrid()
	if animation_process is not None:
		animation_process.terminate()
	pygame.quit()
	sys.exit()

def start_over():
	global leds
	global frame_number
	global animation
	animation = None
	animation={}
	frame_number  = 1
	leds = None
	leds = []
	for x in range(0, 8):
		for y in range(0, 8):
			led = LED(pos=(x, y))
			leds.append(led)

def save_it():
	print('save clicked')
	global warning
	exportAni()
	warning = False

def stop_animation():
	global animation_process
	if animation_process is not None:
		animation_process.terminate()
		animation_process = None

RedButton = Button('', action=setColourRed, size=(50,30), pos=(475, 20),hilight=(0, 200, 200),color=(255,0,0))
buttons.append(RedButton)
OrangeButton = Button('', action=setColourOrange, size=(50,30), pos=(475, 55),hilight=(0, 200, 200),color=(255,128,0))
buttons.append(OrangeButton)
YellowButton = Button('', action=setColourYellow, size=(50,30), pos=(475, 90),hilight=(0, 200, 200),color=(255,255,0))
buttons.append(YellowButton)
GreenButton = Button('', action=setColourGreen, size=(50,30), pos=(475, 125),hilight=(0, 200, 200),color=(0,255,0))
buttons.append(GreenButton)
CyanButton = Button('', action=setColourCyan, size=(50,30), pos=(475, 160),hilight=(0, 200, 200),color=(0,255,255))
buttons.append(CyanButton)
BlueButton = Button('', action=setColourBlue, size=(50,30), pos=(475, 195),hilight=(0, 200, 200),color=(0,0,255))
buttons.append(BlueButton)
PurpleButton = Button('', action=setColourPurple, size=(50,30), pos=(475, 230),hilight=(0, 200, 200),color=(102,0,204))
buttons.append(PurpleButton)
PinkButton = Button('', action=setColourPink, size=(50,30), pos=(475, 265),hilight=(0, 200, 200),color=(255,0,255))
buttons.append(PinkButton)
WhiteButton = Button('', action=setColourWhite, size=(50,30), pos=(475, 300),hilight=(0, 200, 200),color=(255,255,255))
buttons.append(WhiteButton)

PrevFrameButton = Button(u'←', action=prevFrame, size=(40,40), pos=(20, 485), color=(150,150,150), fontsize=30)
buttons.append(PrevFrameButton)
NextFrameButton = Button(u'→', action=nextFrame, size=(40,40), pos=(65, 485), color=(150,150,150), fontsize=30)
buttons.append(NextFrameButton)
startAnimationButton = Button('PLAY', action=start_animation,  size=(80,40), pos=(180, 485), color=(0,200,0))
buttons.append(startAnimationButton)
stopAnimationButton = Button('STOP', action=stop_animation, size=(80,40), pos=(270, 485), color=(200,0,0))
buttons.append(stopAnimationButton)
startOverButton = Button('Start Over', action=start_over, size=(100,40),  pos=(415, 485), color=(150,150,150))
buttons.append(startOverButton)

saveButton = Button('Save', action=save_it, size=(60,50), pos=(150, 180),hilight=(200, 0, 0),color=(255,255,0))
buttons_warn.append(saveButton)
QuitButton = Button('Quit', action=prog_exit, size=(60,50), pos=(260, 180),hilight=(200, 0, 0),color=(255,255,0))
buttons_warn.append(QuitButton)


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

	#update the display
	drawEverything()

