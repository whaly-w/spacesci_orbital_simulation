import pygame
import math
from Control.Planet import Planet
from Control.Satellite import Satellite
from Control.screen_setup import *
import copy
from time import sleep as delay
import Assets

pygame.init()

# Setup display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')


class TextWriter():
    def __init__(self, font, font_size, color= (255, 255, 255)):
        self.typer = pygame.font.Font(font, font_size)
        self.color = color
        self.t = 1
        
    def reset(self):
        self.t = 1
        
    def write(self, msg, pos, win, c_frame, T= 60):
        ln = len(msg)
        freq = T // ln
        
        info = self.typer.render(msg[:self.t], 1, self.color)
        win.blit(info, (pos[0], pos[1]))
        
        self.t = self.t + 1 if ln > self.t and c_frame % freq == 0 else self.t
        
        
    

# Infinte loop
def main():
    run = True
    clock = pygame.time.Clock()
    
    Sun = Planet('Sun', 0, 40, None, 1.98892e30, img= r"Assets\theSun@3x.png", isSun= True)
    Mercury = Planet('Mercury', 0.387 * Planet.AU, 8, 2.439e6, 3.3e23, orbital_velocity= -47.4e3, img= r'Assets\Mercury@3x.png')
    Venus = Planet('Venus', 0.723 * Planet.AU, 15, 6.025e6, 4.8685e24, orbital_velocity= -35.03e3, img = r'Assets\Venus@3x.png')
    Earth = Planet('Earth', -1 * Planet.AU, 16, 6.371e6, 5.9742e24, orbital_velocity= 29.783e3, img= r'Assets\Earth@3x.png')
    Mars = Planet('Mars', -1.524 * Planet.AU, 11, 3.389e6, 6.42e23, orbital_velocity= 24.077e3, img= r'Assets\Mars@3x.png')
    

    spaceJ = Satellite(0, 0, 12, (255, 255, 255), 5e5) # 5
    
    
    global_typer = TextWriter('Assets\ROG_font.ttf', 32)
    

    # Target variable
    origin_planet = Mars
    target_planet = Mercury
    
    # spaceJ.hohmann_transfer(origin_planet, target_planet, Sun)
    
    # global variables
    planets = [Sun, Mercury, Venus, Earth, Mars]
    state = -1
    c_frame = 0 # 1 frame = 1 day
    txt_list = []
    
    # state 2 variables
    pause = False
    start = False
    arrived = False
    while run: 
        ####################################### Setup
        # Screen setup
        clock.tick(60)
        win.fill((0, 0, 0))
        
        # Exit when press 'Q'
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                c_frame = 1e9
                
                
              
        ###################################### State Setup & Manuever
        if state == -1:
            state = 0
            c_frame = 0
            
            spaceJ.orbit_setup(origin_planet)
            vel = math.sqrt(Planet.G * spaceJ.target.mass / (1.5e6 + spaceJ.target.actual_radius))
            # vel = f'{int(vel):,}' if vel > 1000 else f'{vel:.2f}'
            txt_list = [f'Initial Velocity: {vel/1000:.2f} km/s',
                        f'Orbital Period: {int(spaceJ.T):,} s']
            
        if state == 0 and c_frame > 60 * 10:
            state = 1
            c_frame = 0

            spaceJ.transition_setup(spaceJ, spaceJ.target.initial_setup)
            origin_planet.transition_setup(origin_planet, spaceJ.target.initial_setup)
            
            for planet in planets:
                if planet == origin_planet:
                    continue
                planet.x = Planet.AU * -10 * spaceJ.target.initial_setup.x / abs(spaceJ.target.initial_setup.x)
                planet.scale_factor = spaceJ.target.scale_factor
                planet.transition_setup(planet, planet.initial_setup)
                
        if state == 1 and spaceJ.transition_success:
            state = 2
            c_frame = 0
            spaceJ.hohmann_transfer(origin_planet, target_planet, Sun)
            
        elif state == 2 and arrived:
            state = 3
          

                
        
        ###################################### State Operation
        # Planet Orbit
        if state == 0:
            global_typer.write(txt_list[0], (WIDTH/20, HEIGHT/10), win, c_frame)
            global_typer.write(txt_list[1], (WIDTH/20, HEIGHT/10 + 50), win, c_frame)
            spaceJ.target.draw(win)
            spaceJ.draw(win)
            spaceJ.update_orbit()
            
        # Transition
        if state == 1:
            for planet in planets:
                if planet == origin_planet:
                    continue
                planet.update_transition()
                planet.draw(win)
            # Sun.x = Planet.AU
            Sun.draw(win)
                
            origin_planet.update_transition()
            spaceJ.update_transition()
            origin_planet.draw(win)
            spaceJ.draw(win)
            
            

        if state == 2:
            for planet in planets:
                # planet.draw(win, shift_timestep= math.sin(t_pos), scale_timestep= t_scale)  
                planet.draw(win)
                planet.update_position(Sun)  
                
            spaceJ.draw(win)
            arrived = spaceJ.update_hohmann_transfer(start)

            if c_frame > 60:
                start = True
        
            if spaceJ.launch and not pause:
                pause = True
                print(math.degrees(spaceJ.origin.theta), math.degrees(spaceJ.target.theta))
                delay(1)
                
        
        if state == 3:
            for planet in planets:
                planet.draw(win)
                
            spaceJ.draw(win)
        
        
        
        c_frame+= 1
        pygame.display.update()
                
                
    pygame.quit()
    
    
main()