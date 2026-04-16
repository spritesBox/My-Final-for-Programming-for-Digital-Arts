import turtle
import random
import pygame 
from numpy import size


class Circle():


    def __init__(self, pos=(0,0), size =100, life = 1000):
        #at a specific paremeter, the particle will be created 
        # at a specific position
        # this variable has the property/position of the 
        # particle and will be saved for future instances
        self.pos = pos
        self.size = size
        #add different colors for the particles, maybe randomize them
        self.age = 0 #in milliseconds
        self.life = life #in milliseconds
        self.dead = False
        self.alpha = 255
        self.color = pygame.Color(random.randint(0,255), random.randint(0, 255), random.randint(0, 255))
        self.surface = self.update_surface()
    
        pygame.draw.circle(self.surface, self.color, (self.size//2, self.size//2), self.size//2, width=8)

        #replce the surface with text, maybe a random character from the matrix code
        #self.font = pygame.font.SysFont("wingdings3", self.size, bold = True) #find a font I like and make it bold for better visibility
    

    def update(self, dt): #for updating the particle's properties
        self.age += dt
        if self.age > self.life:
            #print("Particle is dead")
            self.dead = True
        #makes the particle fade in and out by changing the alpha value based on age
        self.alpha = 255 * (1-(self.age / self.life))
        #Make particles spread out the newer they are by adding a random offset to the x position based on age
        x_offset = random.randint(-1, 1) * (1 - (self.age / self.life)) * self.size * 0.5 
        self.pos = (self.pos[0] + x_offset, self.pos[1])
        #when space key is pressed, a random area of particles will change color
        

        #update the surface to be text instead of a solid color
        #char = chr(random.randint(33,126)) #chr is 
        #self.surface = self.font.render(char, True, self.color) #display the character and colors

        
        
        

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        return surf
        
    
    def draw(self, surface):
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)

class ParticleTrail():

    def __init__(self, pos, size, life):
        self.pos = pos
        self.size = size
        self.life = life
        self.particles = []

    def update(self, dt):
        particle = Circle(self.pos, size=self.size, life=self.life)
        self.particles.insert(0, particle) #places particle at the beginning of the list
        self._update_particles(dt)
        self._update_pos()
        

    def _update_particles(self, dt):
        for idx, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.dead:
                del self.particles[idx] #removes the particle from the list if it is dead

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)


        
def main():
    #display screen
    pygame.init()
    pygame.display.init()
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
        circle.draw(screen)
        pygame.display.flip()
        #print(particle.age)


    # quits the program once run
    pygame.quit()

if __name__ == "__main__":
    main()    