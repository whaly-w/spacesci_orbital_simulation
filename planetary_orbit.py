import pygame
import math

pygame.init()

# Setup display
WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')

# Colors
_white = (255, 255, 255)

# Setup Font
typer = pygame.font.SysFont('comicsans', 16)

class Planet():
    AU = 149.6e9 # unit in m
    G = 6.67428e-11
    SCALE = 200 / AU # -> 1AU = 100px
    TIMESTEP = 3600 * 24 # 1 day
    
    def __init__(self, x, y, radius, color, mass, isSun= False):
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
        
    def draw(self, win):
        x = self.x * self.SCALE + HEIGHT/2
        y = self.y * self.SCALE + WIDTH/2
        
        if len(self.orbit) > 2:
            scaled_points = []
            for point in self.orbit:
                x_orbit, y_orbit = point
                x_orbit = x_orbit * self.SCALE + WIDTH/2
                y_orbit = y_orbit * self.SCALE + HEIGHT/2
                scaled_points.append((x_orbit, y_orbit))
                
            pygame.draw.lines(win, self.color, False, scaled_points)
        pygame.draw.circle(win, self.color, (x, y), self.raduis)
        
        if not self.isSun:
            distance_text = typer.render(f'{int(self.distance_to_sun/1000)} km', 1, _white)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
            
        
    def attraction(self, other_planet):
        other_x, other_y = other_planet.x, other_planet.y
        dist_x = other_x - self.x
        dist_y = other_y - self.y
        dist_total = math.sqrt(dist_x**2 + dist_y**2)
        
        if other_planet.isSun:
            self.distance_to_sun = dist_total
        
        force = self.G * self.mass * other_planet.mass / dist_total**2
        theta = math.atan2(dist_y, dist_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y        
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        self.orbit.append((self.x, self.y))
        
    
    def update_position_only_sun(self, Sun):
        if self == Sun:
            return
            
        fx, fy = self.attraction(Sun)
            
        self.x_vel += fx / self.mass * self.TIMESTEP
        self.y_vel += fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        self.orbit.append((self.x, self.y))
        


# Infinte loop
def main():
    run = True
    clock = pygame.time.Clock()
    
    Sun = Planet(0, 0, 30, (252, 243, 0), 1.98892e30, isSun= True)
    
    Earth = Planet(-1 * Planet.AU, 0, 16, (72, 149, 239), 5.9742e24)
    Earth.y_vel = 29.783e3
    
    Mars = Planet(-1.524 * Planet.AU, 0, 12, (220, 47, 2), 6.39e23)
    Mars.y_vel = 24.077e3
    
    Mercury = Planet(0.387 * Planet.AU, 0, 8, (108, 117, 125), 3.3e23)
    Mercury.y_vel = -47.4e3
    
    Venus = Planet(0.723 * Planet.AU, 0, 14, (255, 255, 255), 4.8685e24)
    Venus.y_vel = -35.03e3
    
    
    
    
    planets = [Sun, Mercury, Venus, Earth, Mars]
    
    while run: 
        clock.tick(60)
        win.fill((0, 0, 0))
        
        # setup background color
        # win.fill(_white)
            
        for event in pygame.event.get():
            if event.type == 771:
                run = False
                
        for planet in planets:
            planet.draw(win)  
            # planet.update_position(planets)   
            planet.update_position_only_sun(Sun)   
    
        pygame.display.update()
                
                
    pygame.quit()
    
    
main()