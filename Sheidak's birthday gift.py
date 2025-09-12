
# r"C:\Users\hp\OneDrive\04.09.2025_02.57.35_REC.png"
#r"C:\Users\hp\Python Projects\sheid.jpg"
import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Run from Your Teachers!")

# Colors
SKY_BLUE = (135, 206, 235)
GREEN = (0, 150, 0)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
CLOUD_WHITE = (250, 250, 250)

# Game variables
scroll_speed = 5
ground_height = 50
game_speed = 1.0
score = 0
high_score = 0
obstacles = []

# Generate a scrolling background
def create_background(width):
    bg_width = max(width, SCREEN_WIDTH * 2)
    bg = pygame.Surface((bg_width, SCREEN_HEIGHT))
    bg.fill(SKY_BLUE)
    
    # Draw sun
    pygame.draw.circle(bg, (255, 255, 0), (bg_width - 100, 80), 50)
    
    # Draw clouds at various positions
    cloud_positions = [(200, 100), (500, 70), (800, 120), (1100, 60), (1400, 90)]
    for pos in cloud_positions:
        x, y = pos
        pygame.draw.ellipse(bg, CLOUD_WHITE, (x, y, 100, 50))
        pygame.draw.ellipse(bg, CLOUD_WHITE, (x+20, y-20, 80, 50))
        pygame.draw.ellipse(bg, CLOUD_WHITE, (x+40, y+10, 70, 40))
    
    # Draw ground
    pygame.draw.rect(bg, GREEN, (0, SCREEN_HEIGHT - ground_height, bg_width, ground_height))
    
    # Draw some grass details
    for i in range(0, bg_width, 20):
        pygame.draw.line(bg, DARK_GREEN, (i, SCREEN_HEIGHT - ground_height), 
                         (i, SCREEN_HEIGHT - ground_height - 20), 2)
    
    return bg

def create_teacher_faces():
    teacher_faces = []
    
    try:
        # Load teacher 1 image
        teacher1 = pygame.image.load(r"C:\Users\hp\Python Projects\fati.jpg").convert_alpha()
        teacher1 = pygame.transform.scale(teacher1, (60, 60))
        teacher_faces.append(teacher1)
    except:
        print("Could not load teacher1.jpg, using generated face")
        # Create a generated face as fallback
        face1 = pygame.Surface((60, 60), pygame.SRCALPHA)
        # ... drawing code for teacher 1
        
    try:
        # Load teacher 2 image
        teacher2 = pygame.image.load(r"C:\Users\hp\Python Projects\masoom.jpg").convert_alpha()
        teacher2 = pygame.transform.scale(teacher2, (60, 60))
        teacher_faces.append(teacher2)
    except:
        print("Could not load teacher2.jpg, using generated face")
        # Create a generated face as fallback
        face2 = pygame.Surface((60, 60), pygame.SRCALPHA)
        # ... drawing code for teacher 2
        
    return teacher_faces

# Create a face-based character
class RunnerCharacter:
    def __init__(self):
        self.x = 150
        self.y = SCREEN_HEIGHT - 150
        self.width = 60
        self.height = 90
        self.jump_velocity = 0
        self.is_jumping = False
        self.gravity = 0.8
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.is_running = True
        
        # Create a surface for the face
        self.face_img = self.create_face_image()
        
    def create_face_image(self):
        try:
        # Replace "friend_face.jpg" with your image file
            face_img = pygame.image.load(r"C:\Users\hp\Python Projects\sheid.jpg").convert_alpha()
            face_img = pygame.transform.scale(face_img, (50, 50))
            return face_img
        except:
            print("Could not load face image, using generated face")
        # Keep the generated face as fallback
            face_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        # ... rest of the generated face code
            return face_surf
    
    def draw(self, surface):
        # Draw body
        pygame.draw.rect(surface, RED, (self.x + 15, self.y + 40, 30, 40))
        
        # Draw legs in different positions for animation
        frame_mod = int(self.animation_frame) % 2
        pygame.draw.line(surface, SKY_BLUE, (self.x + 20, self.y + 80), 
                        (self.x + 15 - 5 * frame_mod, self.y + 100 + 5 * frame_mod), 6)
        pygame.draw.line(surface, SKY_BLUE, (self.x + 40, self.y + 80), 
                        (self.x + 45 + 5 * frame_mod, self.y + 100 - 5 * frame_mod), 6)
        
        # Draw arms
        arm_swing = 5 * int(self.animation_frame % 3)
        pygame.draw.line(surface, (255, 220, 180), (self.x + 15, self.y + 50), 
                        (self.x - 5 + arm_swing, self.y + 60), 4)
        pygame.draw.line(surface, (255, 220, 180), (self.x + 45, self.y + 50), 
                        (self.x + 55 - arm_swing, self.y + 60), 4)
        
        # Draw the face
        surface.blit(self.face_img, (self.x + 10, self.y + 5))
    
    def update(self, keys):
        # Handle jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and not self.is_jumping:
            self.jump_velocity = -16
            self.is_jumping = True
            
        # Apply gravity and jumping physics
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity
            
            # Check if landed
            if self.y >= SCREEN_HEIGHT - 150:
                self.y = SCREEN_HEIGHT - 150
                self.is_jumping = False
                self.jump_velocity = 0
        
        # Update animation frame
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 4:
            self.animation_frame = 0

# Obstacle class with teacher faces
class TeacherObstacle:
    def __init__(self, x, teacher_face):
        self.x = x
        self.face = teacher_face
        self.width = 50
        self.height = 50
        self.y = SCREEN_HEIGHT - ground_height - self.height
        self.wobble_offset = 1
        self.wobble_direction = 1
    
    def draw(self, surface):
        # Draw a simple body under the face
        pygame.draw.rect(surface, (100, 100, 100), 
                        (self.x + 15, self.y + self.height, 30, 30))
        
        # Draw the teacher face with wobble effect
        wobble_y = self.y + self.wobble_offset
        surface.blit(self.face, (self.x, wobble_y))
    
    def update(self):
        self.x -= scroll_speed * game_speed
        
        # Add a little wobble to the face
        self.wobble_offset += 0.5 * self.wobble_direction
        if abs(self.wobble_offset) > 5:
            self.wobble_direction *= -1
            
        return self.x > -self.width

# Check collision between character and obstacle
def check_collision(character, obstacle):
    char_rect = pygame.Rect(character.x + 15, character.y + 40, 30, 60)
    obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
    return char_rect.colliderect(obstacle_rect)

# Create background (wider for scrolling)
background = create_background(SCREEN_WIDTH * 3)
bg_x = 0  # Background scroll position

# Create teacher faces
teacher_faces = create_teacher_faces()

# Create character
character = RunnerCharacter()

# Game loop
clock = pygame.time.Clock()
obstacle_timer = 0
game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_over and event.key == pygame.K_r:
                # Reset game
                game_over = False
                high_score = int(score if score >= high_score else high_score)
                score = 0
                obstacles = []
                game_speed = 1.0
                bg_x = 0
                obstacle_timer = 0
    
    if not game_over:
        # Get keyboard state
        keys = pygame.key.get_pressed()
        
        # Update character
        character.update(keys)
        
        # Scroll background
        bg_x -= scroll_speed * game_speed
        if bg_x <= -background.get_width() + SCREEN_WIDTH:
            bg_x = 0
        
        # Update obstacles
        obstacles = [obs for obs in obstacles if obs.update()]
        
        # Generate new obstacles
        obstacle_timer += 1
        if obstacle_timer > 60 / game_speed:
            # Randomly select a teacher face
            teacher_face = random.choice(teacher_faces)
            obstacles.append(TeacherObstacle(SCREEN_WIDTH, teacher_face))
            obstacle_timer = 0
        
        # Check for collisions
        for obstacle in obstacles:
            if check_collision(character, obstacle):
                game_over = True
                break
        
        # Increase score and difficulty
        score += 0.1 * game_speed
        if score > 100 and game_speed < 1.5:
            game_speed = 1.2
        if score > 200 and game_speed < 2.0:
            game_speed = 1.5
        if score > 300 and game_speed < 2.5:
            game_speed = 2.0
        if score > high_score and high_score >= 500:
            game_speed *= 2

    
    # Draw the background with scrolling
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + background.get_width(), 0))
    
    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    # Draw character 
    character.draw(screen)
    
    # Draw score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(score_text, (20, 20))

    high_score_text = font.render(f"High Score: {int(high_score)}", True, BLACK)
    screen.blit(high_score_text, (20, 60))
    
    # Draw speed indicator
    speed_text = font.render(f"Speed: {game_speed:.1f}x", True, BLACK)
    screen.blit(speed_text, (20, 100))
    
    # Game over screen
    if game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("CAUGHT BY TEACHER!", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 30))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Clean up
sys.exit()