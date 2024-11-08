


# Class Projectile 

# Constants

# Standard initial values

# velocity
# x, y 
# angle 
# time 

# Set up Pygame 

# While game 
    # Events 
        # If user quits
        # Reset 
        # if user changes input (angle, x, y, etc.)
        # if user shoots projectile 
            # Get values  
            # Update values with a loop (x, y, velocity) using math formulas 
            # Graph projectile and Trajectorie point   
    

# Standard Values 


import pygame
import math

# Constants
GRAVITY = 9.81  # m/s^2 (can be changed by the user)
FPS = 60  # Frame rate
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600  # Screen dimensions
GROUND_LEVEL = SCREEN_HEIGHT - 100  # Ground y-coordinate
SCALE_FACTOR = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Projectile Motion Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# UI elements
launching = False
running = True
paused = False 
recorded_trajectories = []
selected_trajectories = []


# Projectile class
class Projectile:
    def __init__(self, x0, y0, velocity, angle, gravity):
        self.x = x0  # Starting x position
        self.y = y0  # Starting y position
        self.x0 = x0 
        self.velocity = velocity  # Initial speed
        self.angle = math.radians(angle)  # Convert angle to radians
        self.vx = self.velocity * math.cos(self.angle)  # Initial velocity in x
        self.vy = -self.velocity * math.sin(self.angle)  # Initial velocity in y (negative due to screen y-axis)
        self.gravity = gravity
        self.trajectory = []  # Store trajectory points
        self.time = 0  # Track time in seconds
        self.in_motion = False  # Is the projectile moving?
        self.distance = 0
        self.canon = ... 
        self.record_current_trajectory = False
    
    @classmethod
    def standard_values(cls):
        initial_x, initial_y = 100, GROUND_LEVEL
        initial_velocity = 25  # m/s
        initial_angle = 45  # degrees
        gravity = GRAVITY  # m/s^2
        print(initial_angle)
        return cls(initial_x, initial_y, initial_velocity, initial_angle, gravity)
    
    def update(self, dt):
        """Update the projectile's position and velocity."""
        if self.in_motion:
            self.time += dt
            self.vy += self.gravity * dt  # Gravity acts on vy, scaled for pixels
            self.x += self.vx * dt * SCALE_FACTOR  # Multiply by 100 to convert seconds to pixels
            self.y += self.vy * dt * SCALE_FACTOR
            self.distance = (self.x - self.x0) / SCALE_FACTOR

            # Store trajectory points
            self.trajectory.append((int(self.x), int(self.y)))

            # Stop when hitting the ground
            if self.y >= GROUND_LEVEL:  
                self.in_motion = False
                self.y = GROUND_LEVEL  # Clamp y to ground level


    def reset(self, x, y, velocity, angle, gravity):
        """Reset the projectile's initial conditions."""
        self.__init__(x, y, velocity, angle, gravity)
        

        
    def draw(self, screen):
        """Draw the projectile and its trajectory."""
        # Draw trajectory
        for point in self.trajectory:
            pygame.draw.circle(screen, RED, point, 2)

        # Draw projectile
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 5)

class Button:
    button_standard_color = (200, 200, 200)
    button_standard_hover_color = (150, 150, 150)
    
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen=screen):
        # Draw the button
        button_color_current = (
        self.__class__.button_standard_hover_color if self.rect.collidepoint(mouse_pos) 
        else self.__class__.button_standard_color
    )
        pygame.draw.rect(screen, button_color_current, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Standard initial values
initial_x, initial_y = 100, GROUND_LEVEL
initial_velocity = 25  # m/s
initial_angle = 45  # degrees
gravity = GRAVITY  # m/s^2

# Create the projectile
projectile = Projectile(initial_x, initial_y, initial_velocity, initial_angle, gravity)


# defining buttons 
button_standard = Button(10, 160, 150, 40, "Standard Values")
angle_plus_button = Button(200, 10, 30, 30, "+")
angle_minus_button = Button(240, 10, 30, 30, "-")
velocity_plus_button = Button(200, 40, 30, 30, "+")
velocity_minus_button = Button(240, 40, 30, 30, "-")
gravity_plus_button = Button(200, 70, 30, 30, "+")
gravity_minus_button = Button(240, 70, 30, 30, "-")
record_button = Button(10, 200, 150, 40, "Record Trajectory")
clean_button = Button(10, 240, 150, 40, "Clean Trajectories")

def is_point_near(point1, point2, distance_threshold=10):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) <= distance_threshold

# Function to render selected projectiles' information in the right sidebar

def render_sidebar_information(screen, font, selected_trajectories):
    x = SCREEN_WIDTH - 250  # Starting x position on the right side
    y = 50  # Starting y position

    for idx, record in enumerate(selected_trajectories):
        record = selected_trajectories[idx]
        
        # Render endpoint label (e.g., "Projectile N") near the endpoint
        endpoint = record["trajectory"][-1]
        label_text = f"Proj: {idx + 1}"
        label_surface = font.render(label_text, True, BLACK)
        screen.blit(label_surface, (endpoint[0] + 10, endpoint[1] - 15))  # Offset to avoid overlap
        
        # Render the title of the projectile
        title_text = f"Projectile {idx + 1}"
        title_surface = font.render(title_text, True, BLACK)
        screen.blit(title_surface, (x, y))
        y += title_surface.get_height() + 5
        
        # Render initial velocity
        velocity_text = f"Velocity: {record['initial_velocity']} m/s"
        velocity_surface = font.render(velocity_text, True, BLACK)
        screen.blit(velocity_surface, (x, y))
        y += velocity_surface.get_height() + 5
        
        # Render angle
        angle_text = f"Angle: {record['angle']:.1f}°"
        angle_surface = font.render(angle_text, True, BLACK)
        screen.blit(angle_surface, (x, y))
        y += angle_surface.get_height() + 5
        
        # Render gravity
        gravity_text = f"Gravity: {record['gravity']:.2f} m/s²"
        gravity_surface = font.render(gravity_text, True, BLACK)
        screen.blit(gravity_surface, (x, y))
        y += gravity_surface.get_height() + 20  # Extra space before next projectile


# Main loop
while running:
    dt = clock.tick(FPS) / 1000  # Delta time in seconds
    mouse_pos = pygame.mouse.get_pos()
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # reset the projectile 
            if event.key == pygame.K_r:
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            # Shoot the projectile with space bar
            if event.key == pygame.K_SPACE:
                projectile.in_motion = True
            # Adjust pause button 
            if event.key == pygame.K_p:
                paused = not paused
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if angle_plus_button.is_clicked(event.pos):
                initial_angle = min(initial_angle + 5, 90)
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            if angle_minus_button.is_clicked(event.pos):
                initial_angle = max(initial_angle - 5, 0)
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            if velocity_plus_button.is_clicked(event.pos):
                initial_velocity = min(initial_velocity + 5, 50)
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            if velocity_minus_button.is_clicked(event.pos):
                initial_velocity = max(10, initial_velocity - 5)
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            if gravity_plus_button.is_clicked(event.pos):
                gravity += 0.5
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            if gravity_minus_button.is_clicked(event.pos):
                gravity = max(0, gravity - 0.5)
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            if button_standard.is_clicked(event.pos):
                projectile = Projectile.standard_values()
                initial_angle = 45
                initial_velocity = 25
                gravity = GRAVITY
            if record_button.is_clicked(event.pos):
                projectile.record_current_trajectory = True
            if clean_button.is_clicked(event.pos):
                recorded_trajectories.clear()
                selected_trajectories.clear()
            for record in recorded_trajectories:
                # Check if the user wants to show/hide information
                if record["trajectory"]:
                    endpoint = record["trajectory"][-1]
                    if is_point_near(mouse_pos, endpoint):
                        # Toggle the display information flag
                        record["showing_information"] = not record["showing_information"]
                        
                        # Add or remove from selected_trajectories based on the flag
                        if record["showing_information"]:
                            if record not in selected_trajectories:
                                selected_trajectories.append(record)
                        else:
                            if record in selected_trajectories:
                                selected_trajectories.remove(record)

                

    # Update the projectile's motion
    if not paused:
        projectile.update(dt)
    
    # Save trajectory if button is clicked 
    if not projectile.in_motion and projectile.record_current_trajectory:
        recorded_trajectories.append({
            "trajectory": list(projectile.trajectory),
            "initial_velocity": projectile.velocity,
            "angle": math.degrees(projectile.angle),
            "gravity": projectile.gravity,
            "showing_information": False,
            "time": projectile.time,
            "distance": projectile.distance
        })
        projectile.record_current_trajectory = False  # Reset the recording fla

    # Rendering Projectile 
    screen.fill(WHITE)  # Clear screen
    pygame.draw.line(screen, BLACK, (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 2)  # Ground
    projectile.draw(screen)  # Draw projectile and trajectory
    
    # Rendering trajectories
    for record in recorded_trajectories:
        for point in record["trajectory"]:
            pygame.draw.circle(screen, BLUE, point, 2)  # Use a different color for recorded trajectories
    
    # Rendering sidebar information
    if selected_trajectories:
        render_sidebar_information(screen, font, selected_trajectories)
        
    # Rendering buttons 
    button_standard.draw()
    angle_plus_button.draw()
    angle_minus_button.draw()
    velocity_plus_button.draw()
    velocity_minus_button.draw()
    gravity_plus_button.draw()
    gravity_minus_button.draw()
    record_button.draw()
    clean_button.draw()

    # Render Texts 
    angle_text = font.render(f"Angle: {projectile.angle * (180 / math.pi):.0f} degrees", True, BLACK)
    initial_velocity_text = font.render(f"Initial Velocity: {projectile.velocity} m/s", True, BLACK)
    gravity_text = font.render(f"Gravity: {projectile.gravity:.2f} m/s", True, BLACK)
    time_text = font.render(f"Time: {projectile.time:.2f} s", True, BLACK)
    distance_text = font.render(f"Distance: {projectile.distance:.1f} meters", True, BLACK)
    velocity_text = font.render(f"Velocity: {-projectile.vy:.1f} m/s", True, BLACK)
    
    
    # Buttons Text
    screen.blit(angle_text, (10, 20))
    screen.blit(initial_velocity_text, (10, 50))
    screen.blit(gravity_text, (10, 80))
    # Info text
    screen.blit(time_text, (1025, 10))
    screen.blit(distance_text, (1025, 40))
    screen.blit(velocity_text, (1025, 70))

    pygame.display.flip()  # Update display

pygame.quit()
