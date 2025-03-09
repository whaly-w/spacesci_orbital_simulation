import math
import pygame
from Control.Planet import Planet
from .screen_setup import *

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
        self.planet_velocity = abs(target.y_vel)
        self.planet_distance_from_Sun = abs(target.distance_from_Sun)
        
        self.semi_major = (abs(origin.x) + abs(target.x))/2
        self.semi_minor = math.sqrt(abs(origin.x) * abs(target.x))
        self.T = math.sqrt((4 * math.pi**2 / (Sun.G * Sun.mass)) * (self.semi_major)**3) / 2
        self.T_day = self.T / 86400
        
        self.t = 0
        self.launch = False
    
    
    def update_hohmann_transfer(self, start, min_distance= 3e9):
        error_compensate = 14 if self.origin.distance_from_Sun / self.target.distance_from_Sun > 3 else 0
        # print((self.origin.theta_degree - self.target.theta_degree), 180 - int(math.degrees(self.planet_velocity * self.T /2 /self.planet_distance_from_Sun))%360)
        vel = math.sqrt(self.target.x_vel ** 2 + self.target.y_vel ** 2)
        if abs((self.origin.theta_degree - self.target.theta_degree) - 
               (180 - int(math.degrees(self.planet_velocity * self.T /2 /self.planet_distance_from_Sun))%360) + error_compensate) < 5 and start:
            # < 5 default
            self.launch = True
            
        if not self.launch:
            self.x = self.origin.x
            self.y = self.origin.y
            self.launch_theta = math.atan2(self.y, self.x)
        else:
            x = self.semi_major * math.cos(2 * math.pi * self.t / self.T_day + math.radians(180)) + self.offset
            y = self.semi_minor * math.sin(2 * math.pi * self.t / self.T_day + math.radians(180))
        
            self.x, self.y = self.transform_rotation(x, y, -1 * self.launch_theta) 
            self.t += 1  
            
            
        if self.euclidean_dist(self.target) < min_distance:
            return True
        else:
            return False
            

    def transform_rotation(self, x, y, angle):
        ''' angle: in radian '''
        return -1 * (x * math.cos(angle) - y * math.sin(angle)), x * math.sin(angle) + y * math.cos(angle)
    
    def euclidean_dist(self, planet, object= None):
        if object is None:
            return math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        else:
            return math.sqrt((object.x - planet.x)**2 + (object.y - planet.y)**2)