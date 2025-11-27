import pygame, random, sys
from pygame.math import Vector2

class SNAKE:
    # Main function of the snake class
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

    # Draw the snake
    def draw_snake(self):
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            snake_body = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, BLUE, snake_body)

    # Move the snake in a certain direction
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

        
    # Adds a body to the snake after eating a fruit
    def add_body(self):
        self.new_block = True
    
    #  Resets the snake body if game over
    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT:
    # Main function of fruit class
    def __init__(self):
        self.randomize()
    
    # Draw the fruit on the game
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    # Get a random of the fruit
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    # Main function of main class
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    # Updates the location of the snake
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    # Game elements and background
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    # Check if snake eats apple
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            pygame.mixer.music.play()
            self.fruit.randomize()
            self.snake.add_body()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    # Check if snake collides with itself or the game border
    def check_fail(self):
        if  not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: 
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    # Resets the snake position and restart the game
    def game_over(self):
        self.snake.reset()

    # Draw game background
    def draw_grass(self):
        grass_color = DARKGREEN
        for row in range (cell_number):
            if row % 2 == 0:                       
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen,grass_color, grass_rect)

    # Draw the score on the screen
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (0, 0, 0))
        score_x_pos = (cell_size * cell_number - 60)
        score_y_pos = (cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x_pos, score_y_pos))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))

        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Grid block size and number
cell_size = 30
cell_number = 20

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (167, 225, 61)
DARKGREEN = (167, 209, 61)

# Set up the game window
screenWidth = cell_size * cell_number
screenHeight = cell_size * cell_number
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake Game")

# For limit FPS
clock = pygame.time.Clock()

# Game entities
game_font = pygame.font.Font(None, 25)
crunch_sound = pygame.mixer.music.load("sound/crunch_sound.mp3")
apple = pygame.transform.scale( # Scale the image to a specific size
    pygame.image.load('images/apple.png').convert_alpha(), # Get and load the image
    (cell_size, cell_size)  # Image size (width, height) to scale the image
)

# Game update/Snake speed
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

# Main class instance
main_game = MAIN()

# Game loop
running = True
while running:

    screen.fill(GREEN)
    main_game.draw_elements()
    key = pygame.key.get_pressed()

    # Game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)

    # FPS
    pygame.display.update()
    clock.tick(120)

# Quit Pygame
pygame.quit()