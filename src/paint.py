import random
import math
from tkinter import font
from numpy import size
from numpy import size
import pygame


class Particle():


    def __init__(self, pos=(0,0), size =25, life = 1000):
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
        particle = Particle(self.pos, size=self.size, life=self.life)
        self.particles.insert(0, particle) #places particle at the beginning of the list
        self._update_particles(dt)
        self._update_pos()
        

    def _update_particles(self, dt):
        for idx, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.dead:
                del self.particles[idx] #removes the particle from the list if it is dead

    def _update_pos(self):
        x, y = self.pos
        y += self.size + 3 #places the next particle below the previous one
        self.pos = (x,y)
        #TODO: add some randomness to the x position to make it look more natural, maybe a random offset of -5 to 5 pixels
        x += random.randint(-2, 2)
        self.pos = (x,y)


    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

class Rain():

    def __init__(self, screen_res):
        self.screen_res = screen_res
        self.particle_size = 15
        self.trails = [] #to start keeping track of particle trails
        self.birth_rate = 1 #trails per frame]
        self.trails = []


    def update(self, dt):
        self._birth_new_particles()
        for idx, trail in enumerate(self.trails):
            trail.update(dt)
            if self._trail_is_offscreen(trail):
                del self.trails[idx] #removes the trail from the list if it is offscreen


    def _trail_is_offscreen(self, trail):
        #TODO: check if last particle of trail is offscreen (last on the list)
        tail_is_offscreen_ = trail.particles[-1].pos[1] > self.screen_res[1]
        return tail_is_offscreen_


    def _birth_new_particles(self):
        for count in range(self.birth_rate):
            screen_width = self.screen_res[0]
            x = random.randrange(0, screen_width, self.particle_size)
            pos = (x,0)
            life = random.randrange(500,3000)
            trail = ParticleTrail(pos, self.particle_size, life)
            self.trails.insert(0, trail) #places the new trail at the beginning of the list

    def draw(self, surface):
        for trail in self.trails:
            trail.draw(surface)



def main(): 
    # Initialize Pygame and particles and clock
    pygame.init()
    pygame.display.init()
    #find a font I like
    #print(pygame.font.get_fonts())
    pygame.font.init()
    pygame.display.set_caption("Digital Rain")
    clock = pygame.time.Clock()
    dt = 0
    #need to display full screen, so we need to get the screen resolution
    infoObject = pygame.display.Info() 
    resolution = (infoObject.current_w, infoObject.current_h)
    screen = pygame.display.set_mode(resolution)
    rain = Rain(resolution)
    running = True
    while running:
        #Event loop
        for event in pygame.event.get():
            #need to add the close button back to window or let user exit with escape key
            #new and old particles avoid the mouse cursor
            mouse_pos = pygame.mouse.get_pos()
            for trail in rain.trails:
                for particle in trail.particles:
                    if (abs(particle.pos[0] - mouse_pos[0]) < 50) and (abs(particle.pos[1] - mouse_pos[1]) < 50):
                        #move the particle away from the mouse cursor by a random offset of 50 pixels
                        x_offset = random.randint(-50, 50)
                        y_offset = random.randint(-50, 50)
                        particle.pos = (particle.pos[0] + x_offset, particle.pos[1] + y_offset)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.QUIT:
                    running = False
        #for loop closes
        # TODO: some game logic
        rain.update(dt)
        # Render & Display faze
        black = pygame.Color(0,0,0)
        screen.fill(black)
        #pygame.Surface needs coordinates (blit) to appear on screen
        rain.draw(screen)
        pygame.display.flip()
        #print(particle.age)
        dt = clock.tick(12) #caps at 1 frames per second


    # quits the program once run
    pygame.quit()


if __name__ == "__main__":
    main()    