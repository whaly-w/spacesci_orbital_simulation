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


# Infinte loop
def main():
    run = True
    clock = pygame.time.Clock()
    
    Sun = Planet('Sun', 0, 0, 40, (252, 243, 0), 1.98892e30, img= r"Assets\the Sun GIF.gif", isSun= True)
    Mercury = Planet('Mercuty', 0.387 * Planet.AU, 0, 8, (128, 128, 128), 3.3e23, orbital_velocity= -47.4e3)
    Venus = Planet('Venus', 0.723 * Planet.AU, 0, 14, (255, 255, 224), 4.8685e24, orbital_velocity= -35.03e3)
    Earth = Planet('Earth', -1 * Planet.AU, 0, 16, (72, 149, 239), 5.9742e24, orbital_velocity= 29.783e3)
    Mars = Planet('Mars', -1.524 * Planet.AU, 0, 12, (220, 47, 2), 6.42e23, orbital_velocity= 24.077e3)
    
    # Jupiter = Planet(5.2 * Planet.AU, 0, 15, (245, 222, 179), 1.898e27)
    # Jupiter.y_vel = -13.07e3
    # Jupiter.SCALE /= 2
    # Jupiter.TIMESTEP *= 30
    
    # Saturn = Planet(9.58 * Planet.AU, 0, 12, (205, 133, 63), 5.68e26)
    # Saturn.y_vel = -9.69e3
    # Saturn.SCALE /= 3
    # Saturn.TIMESTEP *= 50
    
    # Uranus = Planet(19.22 * Planet.AU, 0, 10, (173, 216, 230), 8.68e25)
    # Uranus.y_vel = -6.81e3
    # Uranus.SCALE /= 4.8
    # Uranus.TIMESTEP *= 100
    
    # Neptune = Planet(30 * Planet.AU, 0 , 10, (0, 0, 139), 1.02e26)
    # Neptune.y_vel = -5.43e3
    # Neptune.SCALE /= 6.2
    # Neptune.TIMESTEP *= 100
    
    spaceJ = Satellite(0, 0, 12, (255, 255, 255), 5e5) # 5
    # spaceJ.hohmann_transfer(Mercury, Mars, Sun)
    # spaceJ.hohmann_transfer(Mars, Mercury, Sun)
    
    # spaceJ.hohmann_transfer(Mercury, Venus, Sun)
    # spaceJ.hohmann_transfer(Mercury, Earth, Sun)
    # spaceJ.hohmann_transfer(Mercury, Mars, Sun)
    
    # spaceJ.hohmann_transfer(Venus, Mercury, Sun)
    spaceJ.hohmann_transfer(Venus, Earth, Sun)
    # spaceJ.hohmann_transfer(Venus, Mars, Sun)
    
    # spaceJ.hohmann_transfer(Earth, Mercury, Sun)
    # spaceJ.hohmann_transfer(Earth, Venus, Sun)
    # spaceJ.hohmann_transfer(Earth, Mars, Sun)
    
    # spaceJ.hohmann_transfer(Mars, Mercury, Sun)
    # spaceJ.hohmann_transfer(Mars, Venus, Sun)
    # spaceJ.hohmann_transfer(Mars, Earth, Sun)
    
    
    
    planets = [Sun, Mercury, Venus, Earth, Mars]
    state = 1
    
    # t_pos = 0
    # t_scale = 1
    c_frame = 0 # 1 frame = 1 day
    stop = False
    pause = False
    start = False
    t = 0
    arrived = False
    while run: 
        ####################################### Setup
        # Screen setup
        clock.tick(60)
        win.fill((0, 0, 0))
        
        # Exit when press 'Q'
        for event in pygame.event.get():
            if event.type == 771:
                run = False
                
              
        ###################################### State Manuever
        if state == 1 and True:
            state = 2
            c_frame = 0
        elif state == 2 and arrived:
            state = 3
          

                
        
        ###################################### State Operation
        # Planet Orbit
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