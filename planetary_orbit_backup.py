import pygame
import math
from Planet import Planet
from screen_setup import *
import copy
from time import sleep as delay

pygame.init()

# Setup display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')


class Satellite(Planet):
    TIMESTEP = 3600 * 24
    
    def __init__(self, x, y, size, color, mass, shift_factor= (1, 1), scale_factor= 1):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.vertices = [(size * math.cos(i * 2*math.pi/3), size * math.sin(i * 2*math.pi/3)) for i in range(0, 3)]
        
        self.x_vel = 0
        self.y_vel = 0
        
        self.shift_factor = shift_factor
        self.scale_factor = scale_factor
        
        self.offset = 0
        self.orbit_position = (0, 0)
        self.target_planet = None
        self.orbit = []
        
        self.count= 0
        
    def draw(self, win, shift_timestep= 0, scale_timestep= 1):
        pygame.draw.polygon(win, self.color, [(
            x  + (self.x + self.orbit_position[0]) * self.SCALE + WIDTH/2, 
            y  + (self.y + self.orbit_position[1]) * self.SCALE + HEIGHT/2
            ) for (x,y) in self.vertices])
           
    
    def orbit_setup(self, planet, distance_from_planet):
        self.x = distance_from_planet
        self.target_planet = planet
        self.orbit_position = (planet.x, planet.y)
        
        self.y_vel = math.sqrt(Planet.G * planet.mass / abs(distance_from_planet))
        print(self.y_vel)
        
    def update_orbit(self):
        fx, fy = self.attraction(self.target_planet)
        total_fx = fx
        total_fy = fy
            
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        self.orbit.append((self.x, self.y))
        
        
    def hohmann_transfer(self, origin, target, Sun):
        self.origin = origin
        self.target = target
        self.offset = (abs(target.x) - abs(origin.x))/2
        
        self.semi_major = (abs(origin.x) + abs(target.x))/2
        self.semi_minor = math.sqrt(abs(origin.x) * abs(target.x))
        self.T = math.sqrt((4 * math.pi**2 / (Sun.G * Sun.mass)) * (self.semi_major)**3) / 2
        self.T_day = self.T / 86400
        
        self.t = 0
        self.launch = False
    
    
    def update_hohmann_transfer(self, start):
        
        
        # if self.t >= self.T_day/2:
        #     return True
        
        # vel = math.sqrt(self.target.x_vel ** 2 + self.target.y_vel ** 2)
        # # print('target angle', math.degrees(47.4e3 * self.T / self.target.distance_to_sun))
        # print(self.T)
        # # print('angel', (self.origin.theta_degree - self.target.theta_degree), 180 + math.degrees(vel * self.T / self.target.distance_to_sun))
        # if abs((self.origin.theta_degree - self.target.theta_degree) - (180 - int(vel * (self.T /self.target.distance_to_sun))%360)) < 2 and start:
        #     self.launch = True
            
    

        if self.launch:
            self.x = self.origin.x
            self.y = self.origin.y
            self.launch_theta = math.atan2(self.y, self.x)
        else:
            x = self.semi_major * math.cos(2 * math.pi * self.t / self.T_day + math.radians(180)) + self.offset
            y = self.semi_minor * math.sin(2 * math.pi * self.t / self.T_day + math.radians(180))
        
            # self.x, self.y = self.transform_rotation(x, y, -1 * self.launch_theta) 
            self.x, self.y = self.transform_rotation(x, y, 0) 
        # self.launch_theta = math.atan2(self.y, self.x)
            self.t += 1  
            
            
            
        return False
            
            
        
    def transform_rotation(self, x, y, angle):
        ''' angle: in radian '''
        return -1 * (x * math.cos(angle) - y * math.sin(angle)), x * math.sin(angle) + y * math.cos(angle)
        
        
        

# Infinte loop
def main():
    run = True
    clock = pygame.time.Clock()
    
    Sun = Planet('Sun', 0, 0, 40, (252, 243, 0), 1.98892e30, isSun= True)
    
    Mercury = Planet('Mercuty', 0.387 * Planet.AU, 0, 8, (128, 128, 128), 3.3e23)
    Mercury.y_vel = -47.4e3
    
    Venus = Planet('Venus', 0.723 * Planet.AU, 0, 14, (255, 255, 224), 4.8685e24)
    Venus.y_vel = -35.03e3
    
    Earth = Planet('Earth', -1 * Planet.AU, 0, 16, (72, 149, 239), 5.9742e24)
    Earth.y_vel = 29.783e3
    # Earth.theta = math.pi / 2
    
    Mars = Planet('Mars', -1.524 * Planet.AU, 0, 12, (220, 47, 2), 6.42e23)
    Mars.y_vel = 24.077e3
    
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
    spaceJ.hohmann_transfer(Earth, Mercury, Sun)
    # spaceJ.orbit_setup(Earth, 1)
    # mission = HahmannTransfer(spaceJ, Earth, Mercury, Sun)
    
    
    
    
    
    planets = [Sun, Mercury, Venus, Earth, Mars]
    # t_pos = 0
    # t_scale = 1
    c_frame = 0 # 1 frame = 1 day
    stop = False
    pause = False
    start = False
    t = 0
    while run: 
        clock.tick(60)
        win.fill((0, 0, 0))
        
        # setup background color
        # win.fill(_white)
            
        for event in pygame.event.get():
            if event.type == 771:
                run = False
                
        for planet in planets:
            # planet.draw(win, shift_timestep= math.sin(t_pos), scale_timestep= t_scale)  
            planet.draw(win)
            planet.update_position(Sun)  
             
        spaceJ.draw(win)
        stat = spaceJ.update_hohmann_transfer(start)
        # print(math.degrees(Earth.theta))
        # if c_frame >= 240 and abs(math.degrees(abs(Earth.theta - Mercury.theta)) - 180) < 1:
        # if not pause and spaceJ.launch:
        #     print(spaceJ.x, spaceJ.y)
        #     # print(math.degrees(spaceJ.launch_theta))
        #     # delay(2)
        #     t+= 1
        if c_frame > spaceJ.T_day/2:
            stat = True
        
        
        
        if spaceJ.launch and not pause:
            pause = True
            print(math.degrees(Earth.theta), math.degrees(Mercury.theta))
            delay(2)

            
        # if math.sqrt(()**2 + ()**2) 
        

        
        # t_pos += 0.05
        # t_scale += 0.01
        # print(f'pos: {t_pos:.2f}, scale: {t_scale:.2f}')
        c_frame+= 1
        # if not stop: pygame.display.update()
        
        # if t < 3: 
        if not stat: 
            pygame.display.update()
                
                
    pygame.quit()
    
    
main()