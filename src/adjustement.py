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
def process_image(image_path, num_dots):
    image = Image.open(image_path)
    resolution = image.size
    surface_size = (resolution[0]//4, resolution[1]//4)
    step_x = surface_size[0] // num_dots
    step_y = surface_size[1] // num_dots
    dots = []
    for i in range(num_dots):
        for j in range(num_dots):
            x_start = i * step_x
            y_start = j * step_y
            x_end = x_start + step_x
            y_end = y_start + step_y
            #crop the image to get the section for this dot
            box = (x_start, y_start, x_end, y_end)
            section = image.crop(box)
            #avg the color of the section
            avg_color = section.resize((1,1)).getpixel((0,0))
            #create a dot with the avg color and position it at the center of the section
            pos = (x_start + step_x//2, y_start + step_y//2)
            dot = Dot(pos, size=25)
            dot.color = avg_color
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

    time_interval = 1 # 200 milliseconds == 0.2 seconds
    next_object_time = 0

    #initialize pygame and create the window
    pygame.init()
    pygame.display.init()
    infoObject = pygame.display.Info() 
    resolution = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode(resolution)
    art = process_image()
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

        current_time = pygame.time.get_ticks()
        if current_time > next_object_time and flag:
            next_object_time += time_interval

            pos = (random.randint(0, resolution[0]//4),
                random.randint(0, resolution[1]//4))

            art.dots.append(Dot(pos, 25,))
            count += 1
            if count >= limit:
                flag = False

        screen.fill((0,0,0))

        for dot in art.dots[:]:
            dot.update(dt)
            dot.draw(screen)

        pygame.display.flip()



if __name__ == "__main__":
    main()    