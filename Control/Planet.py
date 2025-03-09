import math
import pygame
from .screen_setup import *
from .screen_setup import _white

class Planet():
    AU = 149.6e9 # unit in m
    G = 6.67428e-11
    SCALE = 250 / AU # -> 1AU = 100px
    TIMESTEP = 3600 * 24 # 1 day
    
    def __init__(self, name, distance_from_Sun, radius, actual_radius, mass, orbital_velocity= 0, isSun= False, color= _white, img= None):
        self.name = name
        self.x = distance_from_Sun
        self.y = 0
        self.radius = radius
        self.actual_radius = actual_radius
        self.color = color
        self.mass = mass
        self.initial_setup = Coordinate(distance_from_Sun, 0, 1)
        
        if img is not None:
            self.img = pygame.image.load(img)
        else:
            self.img = None
            
        self.orbit = []
        self.isSun = isSun
        self.distance_from_Sun = abs(distance_from_Sun)
        
        self.x_vel = 0
        self.y_vel = orbital_velocity
        self.theta = 0
        self.theta_degree = 0
        
        self.scale_factor = 1
        self.transition_success = False
        self.transition = {
            'x': None,
            'y': None,
            'scale': None,
            'target': None
        }
        
            
        
    # def draw(self, win, shift_timestep= 0, scale_timestep= 1):
    def draw(self, win):
        x = (self.x * self.SCALE) + WIDTH/2
        y = (self.y * self.SCALE) + HEIGHT/2
        
        if len(self.orbit) > 2:
            scaled_points = []
            for point in self.orbit:
                x_orbit, y_orbit = point
                x_orbit = (x_orbit * self.SCALE * self.scale_factor) + WIDTH/2
                y_orbit = (y_orbit * self.SCALE * self.scale_factor) + HEIGHT/2
                scaled_points.append((x_orbit, y_orbit))
                
            pygame.draw.lines(win, self.color, False, scaled_points)
        if self.img is None:    
            pygame.draw.circle(win, self.color, (x, y), self.radius * self.scale_factor)
        else:
            diameter = self.radius * 2 * self.scale_factor
            scaled_img = pygame.transform.scale(self.img, (diameter, diameter))
            image_rect = scaled_img.get_rect()
            image_rect.center = (x, y)
            win.blit(scaled_img, image_rect)
        
        if not self.isSun:
            # distance_text = typer.render(f'{int(self.distance_to_sun/1000)} km', 1, _white)
            name_text = typer.render(self.name, 1, _white)
            # win.blit(name_text, (x - name_text.get_width()/2, y - name_text.get_height()/2 + self.radius))
            
        
    def attraction(self, other_planet):
        other_x, other_y = other_planet.x, other_planet.y
        dist_x = other_x - self.x
        dist_y = other_y - self.y
        dist_total = math.sqrt(dist_x**2 + dist_y**2)
        
        if other_planet.isSun:
            self.distance_from_Sun = dist_total
        
        force = self.G * self.mass * other_planet.mass / dist_total**2
        self.theta = math.atan2(dist_y, dist_x)
        self.theta_degree = (math.degrees(math.atan2(dist_y, dist_x)) + 360) % 360
        
        force_x = math.cos(self.theta) * force
        force_y = math.sin(self.theta) * force
        
        return force_x, force_y        
    

    def update_position(self, Sun):
        if self == Sun:
            return
            
        fx, fy = self.attraction(Sun)
            
        self.x_vel += fx / self.mass * self.TIMESTEP
        self.y_vel += fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        self.orbit.append((self.x, self.y))
        
        
    def transition_setup(self, start, end, T= 60):
        self.transition_success = False
        self.orbit = []
        self.transition['x'] = (end.x - start.x) / T
        self.transition['y'] = (end.y - start.y) / T
        self.transition['target'] = end
        
        try:
            self.transition['scale_factor'] = (end.scale_factor - start.scale_factor) / T
        except:
            self.transition['scale_factor'] = None
        
        
        
    def update_transition(self, error = 10e9):
        self.x = self.transition['target'].x if abs(self.x - self.transition['target'].x) < error else self.x + self.transition['x']
        self.y = self.transition['target'].y if abs(self.y - self.transition['target'].y) < error else self.y + self.transition['y']
        
        if self.transition['scale_factor'] is not None:
            self.scale_factor = self.transition['target'].scale_factor if abs(self.scale_factor - self.transition['target'].scale_factor) < 0.5 else self.scale_factor + self.transition['scale_factor']
        
        if self.x == self.transition['target'].x and self.y == self.transition['target'].y and self.scale_factor == self.transition['target'].scale_factor:
            self.transition_success = True
    

class Coordinate():
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.scale_factor = scale
    
    def show(self):
        print(f'({self.x}, {self.y}) => {self.scale_factor}')