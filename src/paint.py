from itertools import count
import random
import math
from numpy import size
from numpy import size
import pygame
import time



#To do: Create generated artwork using dots instead of lines that have different colors and positions

#Create Class for dots that will have reused properties such as position, size, and color.
#The dots will be created at specific positions and will have a lasting life span

# 1 function to generate the artwork and update properties such as color and position, 
#but dots will be static

# Main Function to create the window and run the program 

#Basic structure for the dot class
class Dot():
    def __init__(self, pos=(0,0), size =25):
        self.size = size
        self.pos = pos
        self.age = 0 #in milliseconds
        self.color = (255,0,0) #red color for the dots
        self.dead = False
        self.surface = self.update_surface()
        self.alpha = 255
        pygame.draw.circle(self.surface, self.color, (self.size//2, self.size//2), self.size//2, width=8)

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        return surf
    
    def update(self, dt):
        self.age += dt
        #want dot to fade in but stay static, so alpha value increases until reaches 255 and stays there
        if self.age <1000: #fade in for the first second
            self.alpha = 255 * (self.age / 1000)
        

    def draw(self, surface):
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)


#The function to generate the dots 
class Art():
    def __init__(self, pos, size = 25):
        self.dots = []
        self.time_interval = 1000
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, self.time_interval)
        self.pos = pos
        self.size = size

    def generate_dots(self, num_dots, surface_size):
    #create surface area for dots to be generated, maybe 1/4 of screen
    #1. get resoultion of screen 
    #2. create surface size based on resolution
    #3. dvide surface by 4
        infoObject = pygame.display.Info()
        resolution = (infoObject.current_w, infoObject.current_h)
        surface_size = (resolution[0]//4, resolution[1]//4)
    #for loop to create the specified number of dots in random positions within surface_size
        for circles in range(num_dots):
            pos = (random.randint(0, surface_size[0]), random.randint(0, surface_size[1]))
            size = self.size
            dot = Dot(pos, size)
            self.dots.append(dot) #add the dot to the list of dots in the artwork
        return self.dots
        

    def update(self, dt):
        for dot in self.dots:
            dot.update(dt) #update the properties of each dot in the artwork
            if dot.dead:
                self.dots.remove(dot) #remove the dot from the list if it is dead
      

    def draw(self, surface):
            for dot in self.dots:
                dot.draw(surface)

#main function to create the window and run the program
def main():
    #initialize pygame and create the window
    pygame.init()
    pygame.display.init()
    infoObject = pygame.display.Info() 
    resolution = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode(resolution)
    art = Art(resolution)
    art.generate_dots(100, resolution) #generate 100 dots for the artwork
    #main loop to keep the window open and update the dots
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == art.timer_event:
                art.dots.append(art.generate_dots(1, resolution)) #generate a new dot every time the timer event is triggered
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        #update the dots and draw them on the screen
        screen.fill((0,0,0)) #fill the background with black
        #art.update(clock.get_time()) #update the artwork
        for dot in art.dots:
            dot.update(clock.get_time()) #update each dot in the artwork
            art.draw(screen) #draw the artwork on the screen
        pygame.display.flip() #update the display
        dt = clock.tick(60) #limit the frame rate to 60 FPS



if __name__ == "__main__":
    main()    