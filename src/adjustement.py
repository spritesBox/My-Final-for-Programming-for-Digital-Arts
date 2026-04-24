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
    def __init__(self, pos=(0,0), step_x=25, step_y=25, color =(255,0,0)):
        self.step_x = step_x
        self.step_y = step_y
        self.pos = pos
        self.age = 0 #in milliseconds
        self.color = color
        self.dead = False
        self.surface = pygame.Surface((self.step_x, self.step_y), pygame.SRCALPHA)
        self.alpha = 255

        pygame.draw.rect(self.surface, self.color, (0, 0, self.step_x, self.step_y))

    def update_surface(self):
        surf = pygame.Surface((self.step_x, self.step_y), pygame.SRCALPHA)
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
    #dots need to match size of step

    new_width = (resolution[0] // grid_size) * grid_size
    new_height = (resolution[1] // grid_size) * grid_size
    image = image.resize((new_width, new_height))
    resolution = (new_width, new_height)
    
    #make steps equal in size to make square pixels no matter the resolution of the image without distorting the image, so find the smaller step size and use that for both x and y

    step = resolution[0] // grid_size #pixel width
    step_x = step
    step_y = step
    
    cols = grid_size
    rows = resolution[1] // step
   
    dots = []
    for i in range(cols):
        for j in range(rows):
            x_start = i * step
            y_start = j * step
            x_end = x_start + step
            y_end = y_start + step
            #crop the image to get the section for this dot
            box = (x_start, y_start, x_end, y_end)
            section = image.crop(box)
            pixels = list(section.getdata())
            size =min(step_x, step_y)


            #avg the color of the section
            r = sum([pixel[0] for pixel in pixels]) // len(pixels)
            g = sum([pixel[1] for pixel in pixels]) // len(pixels)
            b = sum([pixel[2] for pixel in pixels]) // len(pixels)
            avg_color = (r, g, b)


            #create a dot with the avg color and position it at the center of the section
            pos = (x_start, y_start)
            dot = Dot(pos, step_x=step_x, step_y=step_y, color=avg_color)
            dots.append(dot)
    return dots, resolution

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
    #full screen resolution
    resolution = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode(resolution)

    #process image to dots and displays size of the image
    dots, img_res = process_image(image_path, grid_size=20)

    art = Art()
    art.dots = dots

    dot_surface = pygame.Surface(img_res, pygame.SRCALPHA)

    offset_x = (screen.get_width() - img_res[0]) // 2
    offset_y = (screen.get_height() - img_res[1]) // 2 #calculate the offset to center the image on the screen

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
        dot_surface.fill((0,0,0,0)) #clear the dot surface with transparency

        for dot in art.dots[:]:
            dot.update(dt)
            dot.draw(dot_surface)
        screen.blit(dot_surface, (offset_x, offset_y))

        pygame.display.flip()



if __name__ == "__main__":
    main()    