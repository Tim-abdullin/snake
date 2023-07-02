import pygame
import random

pygame.init()

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

window_width = 800
window_height = 600

cell_size = 50

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(window_width // 2, window_height // 2)]
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.color = GREEN

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(window, self.color, (position[0], position[1], cell_size, cell_size))

    def move(self):
        head_x, head_y = self.positions[0]
        if self.direction == 'up':
            head_y -= cell_size
        elif self.direction == 'down':
            head_y += cell_size
        elif self.direction == 'left':
            head_x -= cell_size
        elif self.direction == 'right':
            head_x += cell_size

        self.positions.insert(0, (head_x, head_y))

        if len(self.positions) > self.length:
            self.positions.pop()

    def change_direction(self, new_direction):
        if new_direction == 'up' and self.direction != 'down':
            self.direction = 'up'
        if new_direction == 'down' and self.direction != 'up':
            self.direction = 'down'
        if new_direction == 'left' and self.direction != 'right':
            self.direction = 'left'
        if new_direction == 'right' and self.direction != 'left':
            self.direction = 'right'


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food_position = self.generate_food_pos()
        self.score = 0

    def generate_food_pos(self):
        while True:
            x = random.randint(0, (window_width - cell_size) // cell_size) * cell_size
            y = random.randint(0, (window_height - cell_size) // cell_size) * cell_size
            food_position = (x, y)

            if food_position not in self.snake.positions:
                return food_position

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction('up')
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction('down')
                    if event.key == pygame.K_LEFT:
                        self.snake.change_direction('left')
                    if event.key == pygame.K_RIGHT:
                        self.snake.change_direction('right')

            self.snake.move()

            if self.is_collision():
                running = False

            self.draw()

            clock.tick(5)

    def is_collision(self):
        head = self.snake.positions[0]

        if (
            head[0] < 0
            or head[0] >= window_width
            or head[1] < 0
            or head[1] >= window_height
            or head in self.snake.positions[1:]
        ):
            return True

        if head == self.food_position:
            self.snake.length += 1
            self.score += 1
            self.food_position = self.generate_food_pos()

        return False

    def draw(self):
        window.fill(BLACK)
        self.snake.draw()
        pygame.draw.rect(window, RED, (self.food_position[0], self.food_position[1], cell_size, cell_size))
        pygame.display.update()


game = Game()
game.play()
