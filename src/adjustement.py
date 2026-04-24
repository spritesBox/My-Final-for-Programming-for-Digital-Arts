import random
import math
from numpy import size
from numpy import size
import pygame
import time 
from PIL import Image
from tkinter import Tk, filedialog



#User uploads image file
#The image is processed into a grid by finding resolution
#dividing the resolution by how many steps
#1 step = 1 dot
#avg the colors in each step
#note middle position of each step to place the dot by its center
#avg the color of each step
#replace each step with a dot of that avg color and position
#the dots will appear 1 by 1 in a random order
#the dots stay static


#Basic structure for the dot class
class Dot():
    def __init__(self, pos=(0,0), size =25, color =(255,0,0)):
        self.size = size
        self.pos = pos
        self.age = 0 #in milliseconds
        self.color = color
        self.dead = False
        self.surface = self.update_surface()
        self.alpha = 255
        pygame.draw.circle(self.surface, self.color, (self.size//2, self.size//2), self.size//2)

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
    def __init__(self):
        self.dots = []

    def generate_dots(self, num_dots, surface_size):
    #create surface area for dots to be generated, maybe 1/4 of screen
    #1. get resoultion of screen and //4 to get the area for the dots to be generated
        infoObject = pygame.display.Info()
        resolution = (infoObject.current_w, infoObject.current_h)
        surface_size = (resolution[0]//4, resolution[1]//4)
        num_dots = 25
    #for loop to create the specified number of dots 
        for _ in range(num_dots):
            pos = (random.randint(0, surface_size[0]), random.randint(0, surface_size[1]))
            size = 25
            dot = Dot(pos, size)
            self.dots.append(dot)
        return self.dots

    def draw(self, surface):
            for dot in self.dots:
                dot.draw(surface)


#Function for user to upload image, maybe use tkinter for this and PIL
def upload_image():
    root = Tk()
    root.withdraw() #hide the root window
    file_path = filedialog.askopenfilename(
        title = "Select an image file",
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    ) #open file dialog to select image
    root.destroy() #destroy the root window after file is selected
    return file_path
    #so far does not save the file path

#function to process the image into a grid and avg the colors in each step
def process_image(image_path, grid_size):
    image = Image.open(image_path)
    resolution = image.size
    surface_size = (resolution[0]//4, resolution[1]//4)
    step_x = surface_size[0] // grid_size
    step_y = surface_size[1] // grid_size
    #want size of dot to be based on the step size, maybe 80% of the step size
    size =min(step_x, step_y)
    dots = []
    for i in range(grid_size):
        for j in range(grid_size):
            x_start = i * step_x
            y_start = j * step_y
            x_end = x_start + step_x
            y_end = y_start + step_y
            #crop the image to get the section for this dot
            box = (x_start, y_start, x_end, y_end)
            section = image.crop(box)
            pixels = list(section.getdata())


            #avg the color of the section
            r = sum([pixel[0] for pixel in pixels]) // len(pixels)
            g = sum([pixel[1] for pixel in pixels]) // len(pixels)
            b = sum([pixel[2] for pixel in pixels]) // len(pixels)
            avg_color = (r, g, b)


            #create a dot with the avg color and position it at the center of the section
            pos = (x_start + step_x//2, y_start + step_y//2)
            dot = Dot(pos, size, color=avg_color)
            dots.append(dot)
    return dots

#main function to create the window and run the program
def main():
    #ask user for image
    image_path = upload_image()
    if not image_path:
        print("No image selected. Exiting.")
        return
    
    #load the image with Pillow
    image = Image.open(image_path)

    #initialize pygame and create the window
    pygame.init()
    pygame.display.init()
    infoObject = pygame.display.Info() 
    resolution = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode(resolution)

    #process image to dots
    dots = process_image(image_path, grid_size=10)
    art = Art()
    art.dots = dots

    #main loop to keep the window open and update the dots
    running = True
    clock = pygame.time.Clock()
    limit = 25 #limit the number of dots on the screen to 25
    count = 0
    flag = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill((0,0,0))

        for dot in art.dots[:]:
            dot.update(dt)
            dot.draw(screen)

        pygame.display.flip()



if __name__ == "__main__":
    main()    