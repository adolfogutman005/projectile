


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

# Projectile class
class Projectile:
    def __init__(self, x, y, velocity, angle, gravity):
        self.x = x  # Starting x position
        self.y = y  # Starting y position
        self.velocity = velocity  # Initial speed
        self.angle = math.radians(angle)  # Convert angle to radians
        self.vx = self.velocity * math.cos(self.angle)  # Initial velocity in x
        self.vy = -self.velocity * math.sin(self.angle)  # Initial velocity in y (negative due to screen y-axis)
        self.gravity = gravity
        self.trajectory = []  # Store trajectory points
        self.time = 0  # Track time in seconds
        self.in_motion = False  # Is the projectile moving?

    def update(self, dt):
        """Update the projectile's position and velocity."""
        if self.in_motion:
            self.time += dt
            self.vy += self.gravity * dt * SCALE_FACTOR  # Gravity acts on vy, scaled for pixels
            self.x += self.vx * dt * SCALE_FACTOR  # Multiply by 100 to convert seconds to pixels
            self.y += self.vy * dt * SCALE_FACTOR

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


# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Projectile Motion Simulation")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 24)

# Standard initial values
initial_x, initial_y = 100, GROUND_LEVEL
initial_velocity = 100  # m/s
initial_angle = 45  # degrees
gravity = GRAVITY  # m/s^2

# Create the projectile
projectile = Projectile(initial_x, initial_y, initial_velocity, initial_angle, gravity)

# UI elements
launching = False
running = True

# Main loop
while running:
    dt = clock.tick(FPS) / 1000  # Delta time in seconds

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Reset projectile if 'r' key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            
            # Shoot the projectile with space bar
            if event.key == pygame.K_SPACE:
                projectile.in_motion = True

            # Adjust angle with up/down arrow keys
            if event.key == pygame.K_UP:
                initial_angle = min(initial_angle + 5, 90)  # Max angle 90 degrees
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            if event.key == pygame.K_DOWN:
                initial_angle = max(initial_angle - 5, 0)  # Min angle 0 degrees
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            
            # Adjust speed with left/right arrow keys
            if event.key == pygame.K_RIGHT:
                initial_velocity += 10
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            if event.key == pygame.K_LEFT:
                initial_velocity = max(10, initial_velocity - 10)  # Min velocity 10 m/s
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)

            # Adjust gravity with 'g' and 'h' keys (Optional feature)
            if event.key == pygame.K_g:
                gravity = max(0, gravity - 0.5)
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)
            if event.key == pygame.K_h:
                gravity += 0.5
                projectile.reset(initial_x, initial_y, initial_velocity, initial_angle, gravity)

    # Update the projectile's motion
    projectile.update(dt)

    # Rendering
    screen.fill(WHITE)  # Clear screen
    pygame.draw.line(screen, BLACK, (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 2)  # Ground
    projectile.draw(screen)  # Draw projectile and trajectory

    # Display real-time values (angle, velocity, gravity)
    angle_text = font.render(f"Angle: {initial_angle} degrees", True, BLACK)
    velocity_text = font.render(f"Velocity: {initial_velocity} m/s", True, BLACK)
    time_text = font.render(f"Time: {projectile.time:.2f} s", True, BLACK)
    
    screen.blit(angle_text, (10, 10))
    screen.blit(velocity_text, (10, 40))
    screen.blit(time_text, (10, 70))

    pygame.display.flip()  # Update display

pygame.quit()

