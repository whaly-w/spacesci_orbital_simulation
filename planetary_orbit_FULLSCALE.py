import pygame
import math

pygame.init()

# Setup display
WIDTH, HEIGHT = 1600, 900
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')

# Colors
_white = (255, 255, 255)

# Setup Font
typer = pygame.font.SysFont('comicsans', 16)

class Planet():
    AU = 149.6e9 # unit in m
    G = 6.67428e-11
    SCALE = 100 / AU # -> 1AU = 100px
    TIMESTEP = 3600 * 24 # 1 day
    
    def __init__(self, x, y, radius, color, mass, shift_factor= (1, 1), scale_factor= 1, isSun= False):
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
    
    Sun = Planet(0, 0, 20, (252, 243, 0), 1.98892e30, isSun= True)
    
    Mercury = Planet(0.387 * Planet.AU, 0, 1.5, (128, 128, 128), 3.3e23)
    Mercury.y_vel = -47.4e3
    
    Venus = Planet(0.723 * Planet.AU, 0, 2, (255, 255, 224), 4.8685e24)
    Venus.y_vel = -35.03e3
    
    Earth = Planet(-1 * Planet.AU, 0, 6, (72, 149, 239), 5.9742e24)
    Earth.y_vel = 29.783e3
    
    Mars = Planet(-1.524 * Planet.AU, 0, 5, (220, 47, 2), 6.42e23)
    Mars.y_vel = 24.077e3
    
    Jupiter = Planet(5.2 * Planet.AU, 0, 15, (245, 222, 179), 1.898e27)
    Jupiter.y_vel = -13.07e3
    Jupiter.SCALE /= 2
    Jupiter.TIMESTEP *= 30
    
    Saturn = Planet(9.58 * Planet.AU, 0, 12, (205, 133, 63), 5.68e26)
    Saturn.y_vel = -9.69e3
    Saturn.SCALE /= 3
    Saturn.TIMESTEP *= 50
    
    Uranus = Planet(19.22 * Planet.AU, 0, 10, (173, 216, 230), 8.68e25)
    Uranus.y_vel = -6.81e3
    Uranus.SCALE /= 4.8
    Uranus.TIMESTEP *= 100
    
    Neptune = Planet(30 * Planet.AU, 0 , 10, (0, 0, 139), 1.02e26)
    Neptune.y_vel = -5.43e3
    Neptune.SCALE /= 6.2
    Neptune.TIMESTEP *= 100
    
    
    
    planets = [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]
    t_pos = 0
    t_scale = 1
    while run: 
        # clock.tick(360)
        win.fill((0, 0, 0))
        
        # setup background color
        # win.fill(_white)
            
        for event in pygame.event.get():
            if event.type == 771:
                run = False
                
        for planet in planets:
            planet.draw(win, shift_timestep= math.sin(t_pos), scale_timestep= t_scale)  
            # planet.update_position(planets)   
            planet.update_position_only_sun(Sun)   
        
        # t_pos += 0.05
        # t_scale += 0.01
        print(f'pos: {t_pos:.2f}, scale: {t_scale:.2f}')
        pygame.display.update()
                
                
    pygame.quit()
    
    
main()