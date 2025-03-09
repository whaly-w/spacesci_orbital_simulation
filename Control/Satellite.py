import math
import pygame
from Control.Planet import Planet
from .screen_setup import *
from .screen_setup import _yellow

class Satellite(Planet):
    TIMESTEP = 3600 * 24
    
    def __init__(self, x, y, size, color, mass, img= None, shift_factor= (1, 1), scale_factor= 1):
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.vertices = [(size * math.cos(i * 2*math.pi/3), size * math.sin(i * 2*math.pi/3)) for i in range(0, 3)]
        # self.size = size
        
        if img is not None:
            self.img = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (size *2, size *2))
        else:
            self.img = None
        
        self.shift_factor = shift_factor
        self.scale_factor = scale_factor
        
        self.offset = 0
        self.orbit_position = (0, 0)
        self.target_planet = None
        self.orbit = []
        
        self.t= 0
        self.transition = {
            'x': None,
            'y': None,
            'scale': None,
            'target': None
        }
        
        
    def draw(self, win, shift_timestep= 0, scale_timestep= 1):
        if self.img is None:
            pygame.draw.polygon(win, self.color, [(
                x  + (self.x) * self.SCALE + WIDTH/2, 
                y  + (self.y) * self.SCALE + HEIGHT/2
                ) for (x,y) in self.vertices])
        else:
            image_rect = self.img.get_rect()
            image_rect.center = ((self.x) * self.SCALE + WIDTH/2, 
                                 (self.y) * self.SCALE + HEIGHT/2)
            win.blit(self.img, image_rect)
            
                
        if len(self.orbit) > 2:
            scaled_points = []
            for point in self.orbit:
                x_orbit, y_orbit = point
                x_orbit = (x_orbit * self.SCALE) + WIDTH/2
                y_orbit = (y_orbit * self.SCALE) + HEIGHT/2
                scaled_points.append((x_orbit, y_orbit))
            
            pygame.draw.lines(win, _yellow, False, scaled_points)
           
    
    def orbit_setup(self, planet):
        # Planet setup
        self.target = planet
        self.target.scale_factor = HEIGHT/70 #HEIGHT /5 /self.target.radius 
        self.target.x = 0
        
        # Satellite setup
        self.orbit_position = (-1.4 * self.target.radius * self.target.scale_factor /planet.SCALE)
        self.x = self.orbit_position
        # self.orbit_position = 1500  # for calculation

        self.t = 0
        self.T = 2 * math.pi *  math.sqrt((1.5e6 + self.target.actual_radius)**3 / (Planet.G * self.target.mass))
        self.T_day = self.T / 60    # 60 seconds per frame -> scale 1s/1h
 
    def update_orbit(self):
        # print(self.x, self.y)
        self.x = self.orbit_position * math.cos(2 * math.pi * self.t / self.T_day)
        self.y = self.orbit_position * math.sin(2 * math.pi * self.t / self.T_day)
        
        self.orbit.append((self.x, self.y))
        self.t += 1
        
        
        
    def hohmann_transfer(self, origin, target, Sun):
        self.origin = origin
        self.target = target
        self.offset = (abs(target.x) - abs(origin.x))/2
        self.planet_velocity = abs(target.y_vel)
        self.planet_distance_from_Sun = abs(target.distance_from_Sun)
        error_compensate = 0.99 if self.origin.distance_from_Sun / self.target.distance_from_Sun > 2 else 1
        
        self.semi_major = (abs(origin.x) + abs(target.x))/2 * error_compensate
        self.semi_minor = math.sqrt(abs(origin.x) * abs(target.x))
        self.T = math.sqrt((4 * math.pi**2 / (Sun.G * Sun.mass)) * (self.semi_major)**3) / 2
        self.T_day = self.T / 86400
        
        self.t = 0
        self.launch = False
        self.orbit = []
    
    def update_hohmann_transfer(self, start, min_distance= 3e9):
        error_compensate = 14 if self.origin.distance_from_Sun / self.target.distance_from_Sun > 3  or self.target.mass / self.origin.mass < 0.06 else 0
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
            self.orbit.append((self.x, self.y))
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