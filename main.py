import pygame, sys
from button import Button
from Planet import Planet, Coordinate
from Satellite import Satellite
from screen_setup import *
from Utilities import TextWriter
from time import sleep as delay

pygame.init()

# Setup display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')

# Image Setup
BG = pygame.image.load("assets/bg.jpg")
BG1 = pygame.image.load("assets/bg1.jpg")
galaxyBG = pygame.image.load("assets/galaxy.jpg")
galaxy2 = pygame.image.load("assets/galaxy2.jpg")
arrow = pygame.image.load("assets/arrow.png")

PLANET_IMAGES = {
    "Earth": "assets/earth.png",
    "Venus": "assets/venus.png",
    "Mars": "assets/mars.png",
    "Jupiter": "assets/jupyter.png",
    "Saturn": "assets/saturn.png",
    "Mercury": "assets/mercury.png",
    "Uranus": "assets/uranus.png",
    "Neptune": "assets/neptune.png",
    "Sun": "assets/sun.png"
}

# Globale Varibles
initial_velocity = 0
initial_velocity_Sun = 0
transfer_velocity = 0
final_velocity = 0
final_velocity_Sun = 0

# Planets with rings that need special scaling
RINGED_PLANETS = ["Saturn", "Uranus"]

# Load planet images
planet_image_surfaces = {}
try:
    for planet, img_path in PLANET_IMAGES.items():
        original_img = pygame.image.load(img_path)
        
        # Handle ringed planets differently to preserve aspect ratio
        if planet in RINGED_PLANETS:
            # Get original dimensions
            orig_width, orig_height = original_img.get_size()
            # Calculate aspect ratio
            aspect_ratio = orig_width / orig_height
            
            # For ringed planets, scale by height while preserving aspect ratio
            new_height = 150
            new_width = int(new_height * aspect_ratio)
            
            # Scale the image
            planet_image_surfaces[planet] = pygame.transform.scale(original_img, (new_width, new_height))
        else:
            # Regular planets can be scaled normally to 150x150
            planet_image_surfaces[planet] = pygame.transform.scale(original_img, (150, 150))
            
except pygame.error as e:
    print(f"Warning: Could not load some planet images: {e}")
    # Create placeholder images for missing planets
    for planet in PLANET_IMAGES:
        if planet not in planet_image_surfaces:
            # Create a colored circle as a placeholder
            surf = pygame.Surface((150, 150), pygame.SRCALPHA)
            color = (255, 0, 0) if planet == "Mars" else (
                    (255, 255, 0) if planet == "Venus" else (
                    (222, 184, 135) if planet == "Mercury" else (
                    (255, 140, 0) if planet == "Jupiter" else (
                    (210, 180, 140) if planet == "Saturn" else (0, 0, 255)))))
            pygame.draw.circle(surf, color, (75, 75), 70)
            planet_image_surfaces[planet] = surf

def get_font(size):  # Returns font in the desired size
    return pygame.font.Font("assets/ROG_font.ttf", size)

# Add new calculate function to display the final calculations
def calculate(origin_planet, target_planet, spacecraft, sun):
    global initial_velocity, initial_velocity_Sun, transfer_velocity, final_velocity, final_velocity_Sun
    running = True
    c_frame = 0
    clock = pygame.time.Clock()
    
    # Set up the calculation display
    txt_url = r'Assets\ROG_font.ttf'
    calc_typer = TextWriter(txt_url, 20)
    title_typer = TextWriter(txt_url, 45)
    
 
    
    # Get velocity information from the spacecraft
    # initial_velocity = spacecraft.get_first_cosmic_speed() / 1000  # Convert to km/s
    # transfer_velocity = spacecraft.get_hohmann_speed(sun) / 1000  # Convert to km/s
    # final_velocity = spacecraft.get_first_cosmic_speed() / 1000  # Convert to km/s
    arrival_speed = spacecraft.get_first_cosmic_speed() / 1000  # Convert to km/s
    
    while running:
        clock.tick(60)
        win.fill((0, 0, 0))
        
        # Display background
        win.blit(BG1, (0, 0))
        
        # Display title
        title_typer.just_write("MISSION CALCULATIONS", (WIDTH/2, HEIGHT/8), win, align=1)
        
        # Display origin and destination planets with arrows
        origin_img = planet_image_surfaces.get(origin_planet.name)
        if origin_img:
            origin_img_rect = origin_img.get_rect(center=(WIDTH/4, HEIGHT/3))
            win.blit(origin_img, origin_img_rect)
            
        target_img = planet_image_surfaces.get(target_planet.name)
        if target_img:
            target_img_rect = target_img.get_rect(center=(3*WIDTH/4, HEIGHT/3))
            win.blit(target_img, target_img_rect)
        
        # Draw arrow from origin to destination
        arrow_img = pygame.transform.scale(arrow, (500, 300))
        arrow_rect = arrow_img.get_rect(center=(WIDTH/2, HEIGHT/3))
        win.blit(arrow_img, arrow_rect)
        
        # Display planet names
        calc_typer.just_write(origin_planet.name, (WIDTH/4, HEIGHT/3 + 100), win, align=1)
        calc_typer.just_write(target_planet.name, (3*WIDTH/4, HEIGHT/3 + 100), win, align=1)
        

        
        # Add the velocity information
        calc_typer.just_write(f"Initial Velocity: ", (380, HEIGHT/2 + 40), win, align=0)
        calc_typer.just_write(f"Transfer Velocity: ", (380, HEIGHT/2 + 120), win, align=0)
        calc_typer.just_write(f"Final Velocity: ", (380, HEIGHT/2 + 160), win, align=0)
        
        calc_typer.just_write(f"{initial_velocity_Sun} km/s", (625, HEIGHT/2 + 40), win, align=0)
        calc_typer.just_write(f"{initial_velocity} km/s (rel to Planet)", (625, HEIGHT/2 + 70), win, align=0)
        calc_typer.just_write(f"{transfer_velocity} km/s", (625, HEIGHT/2 + 120), win, align=0)
        calc_typer.just_write(f"{final_velocity_Sun} km/s", (625, HEIGHT/2 + 160), win, align=0)
        calc_typer.just_write(f"{final_velocity} km/s (rel to the Planet)", (625, HEIGHT/2 + 190), win, align=0)
        
        # Instructions for returning
        calc_typer.write_pulsing("Press ESC to return to main menu", (WIDTH/2, HEIGHT - 80), win, c_frame, freq= 3)
   
 
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                    running = False
                    
        
        c_frame += 1
        pygame.display.update()

def main(origin_planet_name=None, destination_planet_name=None):
    global initial_velocity, initial_velocity_Sun, transfer_velocity, final_velocity, final_velocity_Sun
    run = True
    clock = pygame.time.Clock()
    
    Sun = Planet('Sun', 0, 40, None, 1.98892e30, img= r"Assets\theSun@3x.png", isSun= True)
    Mercury = Planet('Mercury', 0.387 * Planet.AU, 8, 2.439e6, 3.3e23, orbital_velocity= -47.87e3, img= r'Assets\Mercury@3x.png', color= (128, 128, 128))
    Venus = Planet('Venus', 0.723 * Planet.AU, 15, 6.052e6, 4.8685e24, orbital_velocity= -35.02e3, img = r'Assets\Venus@3x.png', color= (208, 108, 40))
    Earth = Planet('Earth', -1 * Planet.AU, 16, 6.378e6, 5.9742e24, orbital_velocity= 29.78e3, img= r'Assets\Earth@3x.png', color= (72, 149, 239))
    Mars = Planet('Mars', -1.524 * Planet.AU, 11, 3.396e6, 6.42e23, orbital_velocity= 24.077e3, img= r'Assets\Mars@3x.png', color= (220, 47, 2))
    
    #Add planet dict
    planet_dict = {
        "Mercury": Mercury,
        "Venus": Venus,
        "Earth": Earth, 
        "Mars": Mars,
        "Sun": Sun
    }
    
    # set origin and target planet
    if origin_planet_name and destination_planet_name and origin_planet_name in planet_dict and destination_planet_name in planet_dict:
        origin_planet = planet_dict[origin_planet_name]
        target_planet = planet_dict[destination_planet_name]


    spaceJ = Satellite(0, 0, 12, (255, 255, 255), 5e5, img= r'Assets\SpaceCraft@3x.png') # 5
    
    txt_url = r'Assets\ROG_font.ttf'
    global_typer = TextWriter(txt_url, 28)
    position_typer = TextWriter(txt_url, 12)
    
    # global variables
    planets = [Sun, Mercury, Venus, Earth, Mars]
    state = -1 
    c_frame = 0 # 1 frame = 1 day
    delay_time = 15
    txt_list = []
    
    # state 2 variables
    pause = False
    start = False
    arrived = False
    
    # Track if space was pressed to show calculations
    show_calculations = False
    
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
                if state == 5:  # Only trigger calculation if in final state
                    show_calculations = True
                else:
                    c_frame = 1e9
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
                
        # Check if we should show the calculation screen
        if show_calculations:
            calculate(origin_planet, target_planet, spaceJ, Sun)
            continue
                
        ###################################### State Setup & Manuever
        if state == -1:
            state = 0
            c_frame = 0
            
            spaceJ.orbit_setup(origin_planet)
            initial_velocity = round(spaceJ.get_first_cosmic_speed()/1000, 2)
            initial_velocity_Sun = round(initial_velocity + abs(origin_planet.initial_setup.orbital_velocity)/1000, 2)
            
            txt_list = [f'Initial Velocity: {initial_velocity} km/s',
                        f'Orbital Period: {int(spaceJ.T_day):,} min']
            
        if state == 0 and c_frame > 60 * delay_time:
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
                transfer_velocity = round(spaceJ.get_hohmann_speed(Sun)/1000, 2)
                txt_list = [f'Planet Orbital Velocity: {abs(round(target_planet.initial_setup.orbital_velocity/1000, 2)):,} km/s',
                            f'Transfer Velocity: {transfer_velocity} km/s',
                            f'Transfer Period: {int(spaceJ.T_day):,} days']
            
        elif state == 2 and arrived:
            c_frame = 0
            state = 3
            print(target_planet.x)
            
        elif state == 3 and c_frame > 60 * delay_time:
            state = 4
            c_frame = 0
            
            spaceJ.orbit_setup(target_planet, move= False)
            sign = -1 if target_planet.x > 0 else 1
            spaceJ.transition_setup(spaceJ, Coordinate(sign * spaceJ.orbit_position, 0, None, None))
            target_planet.transition_setup(target_planet, Coordinate(0, 0, spaceJ.orbit_scale, None))
            
        elif state == 4 and spaceJ.transition_success and target_planet.transition_success:
            state = 5
            c_frame = 0
            
            print(spaceJ.x)
            spaceJ.orbit_setup(target_planet,  position= -1 if spaceJ.x < 0 else 1, direction= -1)
            final_velocity = round(spaceJ.get_first_cosmic_speed()/1000, 2)
            final_velocity_Sun = round(final_velocity_Sun + abs(target_planet.initial_setup.orbital_velocity/1000), 2)
            txt_list = [f'Final Velocity: {final_velocity} km/s',
                        f'Orbital Period: {int(spaceJ.T_day):,} min']
            
        ###################################### State Operation
        # Planet Orbit
        if state == 0 or state == 5:
            global_typer.write(txt_list[0], (WIDTH/20, HEIGHT/12), win, c_frame)
            global_typer.write(txt_list[1], (WIDTH/20, HEIGHT/12 + 50), win, c_frame)
            spaceJ.target.draw(win)
            spaceJ.draw(win)
            spaceJ.update_orbit()
            
            if state == 5:
                global_typer.write_pulsing('Press SPACE to see detailed calculations', (WIDTH/2, HEIGHT/1.12), win, c_frame, freq=3)
            elif state == 0:
                global_typer.write_pulsing('Press SPACE to continue...', (WIDTH/2, HEIGHT/1.12), win, c_frame, freq=3)
            
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
                global_typer.write(txt_list[0], (WIDTH/20, HEIGHT/12), win, c_frame)
            else:
                global_typer.just_write(txt_list[0], (WIDTH/20, HEIGHT/12), win)
                global_typer.write(txt_list[1], (WIDTH/20, HEIGHT/12 + 50), win, c_frame)
                global_typer.write(txt_list[2], (WIDTH/20, HEIGHT/12 + 100), win, c_frame)
                
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
            global_typer.just_write(txt_list[0], (WIDTH/20, HEIGHT/12), win)
            global_typer.just_write(txt_list[1], (WIDTH/20, HEIGHT/12 + 50), win)
            global_typer.just_write(txt_list[2], (WIDTH/20, HEIGHT/12 + 100), win)
            
            global_typer.write_pulsing('Press SPACE to continue...', (WIDTH/2, HEIGHT/1.12), win, c_frame, freq=3)
            
        
         # Transition
        elif state == 4:
            target_planet.update_transition()
            spaceJ.update_transition()
            
            target_planet.draw(win)
            spaceJ.draw(win)
        
        c_frame += 1
        pygame.display.update()
        
        BACK_BUTTON = Button(image=None, pos=(100, 670), 
                           text_input="BACK", font=get_font(30), base_color="White", hovering_color="#ffcc00")
        BACK_BUTTON.update(SCREEN)
                
    pygame.quit()

def play():
    SCREEN.blit(BG1,(0,0))
    # List of planets
    # planets = ["Earth", "Venus", "Mars", "Jupiter", "Saturn", "Mercury", "Uranus", "Neptune"]
    planets = ["Mercury", "Venus", "Earth", "Mars"]
    
    # Initialize selection indexes
    origin_idx = 0
    destination_idx = 0
    
    # Get initial planet selections
    selected_origin = planets[origin_idx]
    selected_destination = planets[destination_idx]
    
    while True:
        SCREEN.blit(BG1, (0, 0))  # Draw galaxy background
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Title text
        PLAY_TEXT = get_font(45).render("SET YOUR DESTINATION", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        
        # Subtitle text
        SUB_TEXT = get_font(20).render("SELECT YOUR STARTING PLANET AND WHERE YOU WANT TO GO", True, "White")
        SUB_RECT = SUB_TEXT.get_rect(center=(640, 150))
        SCREEN.blit(SUB_TEXT, SUB_RECT)
        
        # Origin section header
        ORIGIN_TEXT = get_font(30).render("ORIGIN", True, "White")
        ORIGIN_RECT = ORIGIN_TEXT.get_rect(center=(640, 220))
        SCREEN.blit(ORIGIN_TEXT, ORIGIN_RECT)
        
        # Origin selection with arrows
        # Place planet image on the left
        origin_img = planet_image_surfaces.get(selected_origin)
        origin_img_rect = origin_img.get_rect(center=(380, 300))  # Moved to the left
        SCREEN.blit(origin_img, origin_img_rect)
        
        # Planet name in the center
        origin_name = get_font(35).render(selected_origin, True, "White")
        origin_name_rect = origin_name.get_rect(center=(640, 300))  # Kept in center
        SCREEN.blit(origin_name, origin_name_rect)
        
        # Left arrow for origin
        origin_left = Button(image=None, pos=(520, 300), text_input="<", 
                             font=get_font(60), base_color="White", hovering_color="#ffcc00")
        origin_left.changeColor(PLAY_MOUSE_POS)
        origin_left.update(SCREEN)
        
        # Right arrow for origin
        origin_right = Button(image=None, pos=(750, 300), text_input=">", 
                              font=get_font(60), base_color="White", hovering_color="#ffcc00")
        origin_right.changeColor(PLAY_MOUSE_POS)
        origin_right.update(SCREEN)
        
        # Destination section header
        DEST_TEXT = get_font(30).render("DESTINATION", True, "White")
        DEST_RECT = DEST_TEXT.get_rect(center=(640, 440))
        SCREEN.blit(DEST_TEXT, DEST_RECT)
        
        # Destination selection with arrows
        # Place planet image on the left
        dest_img = planet_image_surfaces.get(selected_destination)
        dest_img_rect = dest_img.get_rect(center=(380, 520))  # Moved to the left
        SCREEN.blit(dest_img, dest_img_rect)
        
        # Planet name in the center
        dest_name = get_font(35).render(selected_destination, True, "White")
        dest_name_rect = dest_name.get_rect(center=(640, 520))  # Kept in center
        SCREEN.blit(dest_name, dest_name_rect)
        
        # Left arrow for destination
        dest_left = Button(image=None, pos=(520, 520), text_input="<", 
                           font=get_font(60), base_color="White", hovering_color="#ffcc00")
        dest_left.changeColor(PLAY_MOUSE_POS)
        dest_left.update(SCREEN)
        
        # Right arrow for destination
        dest_right = Button(image=None, pos=(750, 520), text_input=">", 
                            font=get_font(60), base_color="White", hovering_color="#ffcc00")
        dest_right.changeColor(PLAY_MOUSE_POS)
        dest_right.update(SCREEN)
        
        # Check if selection is valid
        valid_selection = selected_origin != selected_destination
        
        # Calculate button
        if valid_selection:
            CALC_BUTTON = Button(image=None, pos=(640, 670), 
                               text_input="CALCULATE SPEED", font=get_font(40), 
                               base_color="#00ff44", hovering_color="White")
            CALC_BUTTON.changeColor(PLAY_MOUSE_POS)
            CALC_BUTTON.update(SCREEN)
        else:
            # Show error message if same planet selected
            error_text = get_font(25).render("Origin and destination cannot be the same!", True, "#ff5555")
            error_rect = error_text.get_rect(center=(640, 670))
            SCREEN.blit(error_text, error_rect)
        
        # Back button
        BACK_BUTTON = Button(image=None, pos=(100, 670), 
                           text_input="BACK", font=get_font(30), base_color="White", hovering_color="#ffcc00")
        BACK_BUTTON.changeColor(PLAY_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check back button
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                
                # Calculate button - now directly calls the modified main function
                if valid_selection and CALC_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main(selected_origin, selected_destination)
                
                # Origin planet navigation
                if origin_left.checkForInput(PLAY_MOUSE_POS):
                    origin_idx = (origin_idx - 1) % len(planets)
                    selected_origin = planets[origin_idx]
                
                if origin_right.checkForInput(PLAY_MOUSE_POS):
                    origin_idx = (origin_idx + 1) % len(planets)
                    selected_origin = planets[origin_idx]
                
                # Destination planet navigation
                if dest_left.checkForInput(PLAY_MOUSE_POS):
                    destination_idx = (destination_idx - 1) % len(planets)
                    selected_destination = planets[destination_idx]
                
                if dest_right.checkForInput(PLAY_MOUSE_POS):
                    destination_idx = (destination_idx + 1) % len(planets)
                    selected_destination = planets[destination_idx]
        
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        
        # Add planets to the main menu, preserving aspect ratio for ringed planets
        # Earth
        left_planet = pygame.transform.scale(planet_image_surfaces["Earth"], (150, 150))
        SCREEN.blit(left_planet, left_planet.get_rect(center=(920, 500)))
        
        # Jupiter
        center_planet = pygame.transform.scale(planet_image_surfaces["Jupiter"], (200, 200))
        SCREEN.blit(center_planet, center_planet.get_rect(center=(1080, 300)))
        
        # Sun
        right_planet = pygame.transform.scale(planet_image_surfaces["Sun"], (300, 300))
        SCREEN.blit(right_planet, right_planet.get_rect(center=(780, 300)))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("WELCOME", True, "#FFFFFF")
        MENU_RECT = MENU_TEXT.get_rect(center=(380, 300))

        Menu_TEXT2 = get_font(20).render("INITIATE NAVIGATION", True, "White")
        Menu_rect = Menu_TEXT2.get_rect(center=(380, 400))
        SCREEN.blit(Menu_TEXT2, Menu_rect)

        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (150, 50)), 
                    pos=(380, 460), text_input="PLAY", font=get_font(40), 
                    base_color="#ecff00", hovering_color="White")
 
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play() 

        pygame.display.update()

main_menu()