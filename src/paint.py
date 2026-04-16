import turtle

import pygame 


class Circle:
    def __init__(self, radius = 50, pos = (0,0)):
        self.radius = radius
        self.pos = pos
        self.surface = self.update_surface()

    def draw(self):
        turtle.penup()
        turtle.goto(self.pos)
        turtle.pendown()
        turtle.fillcolor("red")
        turtle.begin_fill()
        turtle.circle(self.radius)
        turtle.end_fill()

    def update_surface(self):
        self = pygame.Surface((self.radius, self.radius))
        return self
        
        
    def draw(self, surface):
        surface.blit(self.update_surface(), self.pos)

def main():
    #display screen
    pygame.init()
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    circle = Circle(resolution)
    running = True
    while running:
        #Event loop
        for event in pygame.event.get():
            #if user clicks close button, running = false
            if event.type == pygame.QUIT:
                running = False
        #for loop closes
        # Render & Display faze
        black = pygame.Color(0,0,0)
        screen.fill(black)
        #pygame.Surface needs coordinates (blit) to appear on screen
        Circle.draw(screen)
        pygame.display.flip()
        #print(particle.age)


    # quits the program once run
    pygame.quit()

if __name__ == "__main__":
    main()    