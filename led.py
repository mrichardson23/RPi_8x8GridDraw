import pygame
from pygame import gfxdraw
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


class LED():
    def __init__(self, pos=(0, 0), radius=25, lit=False):
       
       # Initializes the LED
        
        self.pos = pos
        self.lit = lit
        self.radius = radius
        self.screen = pygame.display.get_surface()
        self.color = [255, 255, 255]
        self.pos_x = int(self.pos[0] * (self.radius * 2 + 5)) + (self.radius) + 20
        self.pos_y = int(self.pos[1] * (self.radius * 2 + 5)) + (self.radius) + 20

    @property
    def color_name(self):
        return list(colours.keys())[list(colours.values()).index(self.color)]

    def draw(self):
        
        #Draws a circle, 
        w = []
        if self.lit: # has it been clicked?
            thickness = 0
        else:
            self.color = [255,255,255]
            thickness = 1

        gfxdraw.aacircle(self.screen, self.pos_x, self.pos_y, self.radius - 5, (255,255,255))

        # Draws a square
        pygame.draw.rect(self.screen,self.color,(self.pos_x-25, self.pos_y-25, 50,50),thickness)

    def clicked(self, colour):
        
        # what to do when clicked
        self.color = colour
        
        
        if self.lit:
            self.lit = False
        else:
            self.lit = True
        
