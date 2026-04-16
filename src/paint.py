import random
import math
from numpy import size
from numpy import size
import pygame



#To do: Create generated artwork using dots instead of lines that have different colors and positions

#Create Class for dots that will have reused properties such as position, size, and color.
#The dots will be created at specific positions and will have a lasting life span

# 1 function to generate the artwork and update properties such as color and position, 
#but dots will be static

# Main Function to create the window and run the program 

class Dot():
    def __init__(self, pos=(0,0), size =25, life = 1000):
        self.size = size
        self.pos = pos
        self.age = 0 #in milliseconds
        self.color = (255,0,0) #red color for the dots
        self.life = life #in milliseconds
        self.dead = False
        self.surface = self.update_surface()
        pygame.draw.circle(self.surface, self.color, (self.size//2, self.size//2), self.size//2, width=8)

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        return surf
    
    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            self.dead = True

    def draw(self, surface):
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)


#The function to generate the dots 
def generate_dots(num_dots, surface_size):
    dots = []
    #for loop to create the specified number of dots 
    for _ in range(num_dots):
        pos = (random.randint(0, surface_size[0]), random.randint(0, surface_size[1]))
        size = Dot.size
        life = random.randint(500, 2000) #random life span for the dots
        dot = Dot(pos, size, life)
        dots.append(dot)
    return dots

#main function to create the window and run the program
def main():
    #initialize pygame and create the window
    pygame.init()
    pygame.display.init()
    infoObject = pygame.display.Info() 
    resolution = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode(resolution)
    art = generate_dots(resolution)
    #main loop to keep the window open and update the dots
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        #update the dots and draw them on the screen
        screen.fill((0,0,0)) #fill the background with black
        for dot in art:
            dot.update(clock.get_time()) #update the dot
            if dot.dead:
                art.remove(dot) #remove the dead dot from the list
            else:
                dot.draw(screen) #draw the dot on the screen



if __name__ == "__main__":
    main()    