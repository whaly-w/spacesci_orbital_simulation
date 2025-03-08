import math
import pygame
from screen_setup import *
from screen_setup import _white

class Planet():
    AU = 149.6e9 # unit in m
    G = 6.67428e-11
    SCALE = 250 / AU # -> 1AU = 100px
    TIMESTEP = 3600 * 24 # 1 day
    
    def __init__(self, name, x, y, radius, color, mass, shift_factor= (1, 1), scale_factor= 1, isSun= False):
        self.name = name
        self.x = x
        self.y = y
        self.raduis = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.isSun = isSun
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
        self.theta = 0
        self.theta_degree = 0
        
        self.shift_factor = shift_factor
        self.scale_factor = scale_factor
        
    def draw(self, win, shift_timestep= 0, scale_timestep= 1):
        x_shift, y_shift = self.shift_factor[0] * shift_timestep, self.shift_factor[1] * shift_timestep 
        x_zoom, y_zoom = scale_timestep * self.scale_factor, scale_timestep * self.scale_factor
        
        
        x = (self.x * self.SCALE * x_zoom) + WIDTH/2 + x_shift
        y = (self.y * self.SCALE * y_zoom) + HEIGHT/2 + y_shift
        
        if len(self.orbit) > 2:
            scaled_points = []
            for point in self.orbit:
                x_orbit, y_orbit = point
                x_orbit = (x_orbit * self.SCALE * x_zoom) + WIDTH/2 + x_shift
                y_orbit = (y_orbit * self.SCALE * y_zoom) + HEIGHT/2 + y_shift
                scaled_points.append((x_orbit, y_orbit))
                
            pygame.draw.lines(win, self.color, False, scaled_points)
        pygame.draw.circle(win, self.color, (x, y), self.raduis * scale_timestep * self.scale_factor)
        
        if not self.isSun:
            # distance_text = typer.render(f'{int(self.distance_to_sun/1000)} km', 1, _white)
            name_text = typer.render(self.name, 1, _white)
            win.blit(name_text, (x - name_text.get_width()/2, y - name_text.get_height()/2 + self.raduis))
            
        
    def attraction(self, other_planet):
        other_x, other_y = other_planet.x, other_planet.y
        dist_x = other_x - self.x
        dist_y = other_y - self.y
        dist_total = math.sqrt(dist_x**2 + dist_y**2)
        
        if other_planet.isSun:
            self.distance_to_sun = dist_total
        
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