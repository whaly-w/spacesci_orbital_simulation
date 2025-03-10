import pygame
import math
from Control.Planet import Planet, Coordinate
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
        self._color = [int(255/20 * c) for c in range(0, 21)]
        self._color = self._color + [self._color[i] for i in range(19, 0, -1)]
        print(self._color)
        
    def reset(self):
        self.t = 1
        
    def just_write(self, msg, pos, win, align= 0):
        ''' align: 0-left, 1-center, 2-right'''
        info = self.typer.render(msg, 1, self.color)
        if align == 0:
            win.blit(info, (pos[0], pos[1]))
        elif align == 1:
            win.blit(info, (pos[0] - info.get_width()/2, pos[1]))
        else:
            win.blit(info, (pos[0] - info.get_width(), pos[1]))        
        
    def write(self, msg, pos, win, c_frame, T= 60):
        ln = len(msg)
        freq = T // ln
        
        info = self.typer.render(msg[:self.t], 1, self.color)
        win.blit(info, (pos[0], pos[1]))
        
        self.t = self.t + 1 if ln > self.t and c_frame % freq == 0 else self.t
        
    def write_pulsing(self, msg, pos, win, c_frame, freq= 5):
        txt_color = [self._color[int(c_frame/freq) % len(self._color)] for _ in range(3)]
        print(txt_color)
        info = self.typer.render(msg, 1, txt_color)
        win.blit(info, (pos[0] - info.get_width()/2, pos[1]))
        
        
        
        
    

# Infinte loop
def main():
    run = True
    clock = pygame.time.Clock()
    
    Sun = Planet('Sun', 0, 40, None, 1.98892e30, img= r"Assets\theSun@3x.png", isSun= True)
    Mercury = Planet('Mercury', 0.387 * Planet.AU, 8, 2.439e6, 3.3e23, orbital_velocity= -47.4e3, img= r'Assets\Mercury@3x.png', color= (128, 128, 128))
    Venus = Planet('Venus', 0.723 * Planet.AU, 15, 6.025e6, 4.8685e24, orbital_velocity= -35.03e3, img = r'Assets\Venus@3x.png', color= (208, 108, 40))
    Earth = Planet('Earth', -1 * Planet.AU, 16, 6.371e6, 5.9742e24, orbital_velocity= 29.783e3, img= r'Assets\Earth@3x.png', color= (72, 149, 239))
    Mars = Planet('Mars', -1.524 * Planet.AU, 11, 3.389e6, 6.42e23, orbital_velocity= 24.077e3, img= r'Assets\Mars@3x.png', color= (220, 47, 2))
    

    spaceJ = Satellite(0, 0, 12, (255, 255, 255), 5e5, img= r'Assets\SpaceCraft@3x.png') # 5
    
    
    txt_url = r'Assets\ROG_font.ttf'
    global_typer = TextWriter(txt_url, 32)
    position_typer = TextWriter(txt_url, 12)
    

    # Target variable
    origin_planet = Venus
    target_planet = Earth
    
    # spaceJ.hohmann_transfer(origin_planet, target_planet, Sun)
    
    # global variableserror_compensate
    planets = [Sun, Mercury, Venus, Earth, Mars]
    state = -1 
    # state = 2
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
            txt_list = [f'Initial Velocity: {spaceJ.get_first_cosmic_speed()/1000:.2f} km/s',
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
            all_success = True
            for planet in planets:
                if not planet.transition_success:
                    all_success = False
            if all_success:
                state = 2
                c_frame = 0
                spaceJ.hohmann_transfer(origin_planet, target_planet, Sun)
                
                global_typer.reset()
                txt_list = [f'Planet Orbital Velocity: {abs(int(target_planet.initial_setup.orbital_velocity/1000)):,} km/s',
                            f'Transfer Velocity: {spaceJ.get_hohmann_speed(Sun)/1000:.2f} km/s',
                            f'Transfer Period: {int(spaceJ.T_day):,} days']
            
        elif state == 2 and arrived:
            c_frame = 0
            state = 3
            
        elif state == 3 and c_frame > 60 * 10:
            state = 4
            c_frame = 0
            
            spaceJ.orbit_setup(target_planet, move= False)
            spaceJ.transition_setup(spaceJ, Coordinate(spaceJ.orbit_position, 0, None, None))
            target_planet.transition_setup(target_planet, Coordinate(0, 0, spaceJ.orbit_scale, None))
            
        elif state == 4 and spaceJ.transition_success and target_planet.transition_success:
            state = 5
            c_frame = 0
            
            spaceJ.orbit_setup(target_planet)
            txt_list = [f'Final Velocity: {spaceJ.get_first_cosmic_speed()/1000:.2f} km/s',
                        f'Orbital Period: {int(spaceJ.T):,} s']
            
            
                
        
        ###################################### State Operation
        # Planet Orbit
        if state == 0 or state == 5:
            global_typer.write(txt_list[0], (WIDTH/20, HEIGHT/10), win, c_frame)
            global_typer.write(txt_list[1], (WIDTH/20, HEIGHT/10 + 50), win, c_frame)
            spaceJ.target.draw(win)
            spaceJ.draw(win)
            spaceJ.update_orbit()
            
            if state == 5 or True:
                global_typer.write_pulsing('Press ENTER to continue...', (WIDTH/2, HEIGHT/1.12), win, c_frame, freq=3)
            
        # Transition
        elif state == 1:
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
            
        # Hohmann Transition
        elif state == 2:
            if not pause:
                global_typer.write(txt_list[0], (WIDTH/20, HEIGHT/10), win, c_frame)
            else:
                global_typer.just_write(txt_list[0], (WIDTH/20, HEIGHT/10), win)
                global_typer.write(txt_list[1], (WIDTH/20, HEIGHT/10 + 50), win, c_frame)
                global_typer.write(txt_list[2], (WIDTH/20, HEIGHT/10 + 100), win, c_frame)
                
            # global_typer.write(txt_list[1], (WIDTH/20, HEIGHT/10 + 50), win, c_frame)
            
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
                global_typer.reset()
                print()
                position_typer.just_write('Launch Position', 
                                          (origin_planet.x * target_planet.SCALE + WIDTH/2, origin_planet.y * target_planet.SCALE + HEIGHT/2 + 20), 
                                          win, align= 1)
                pygame.display.update()
                delay(3)    
                  
        # Pause and wait
        elif state == 3:
            for planet in planets:
                planet.draw(win)
            spaceJ.draw(win)
            global_typer.just_write(txt_list[0], (WIDTH/20, HEIGHT/10), win)
            global_typer.just_write(txt_list[1], (WIDTH/20, HEIGHT/10 + 50), win)
            global_typer.just_write(txt_list[2], (WIDTH/20, HEIGHT/10 + 100), win)
        
         # Transition
        elif state == 4:
            target_planet.update_transition()
            spaceJ.update_transition()
            
            target_planet.draw(win)
            spaceJ.draw(win)
            
            
            
        
      
            
        
        
        
        c_frame+= 1
        pygame.display.update()
                
                
    pygame.quit()
    
    
main()
