import pygame
import random

pygame.init()

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

window_width = 800
window_height = 600

cell_size = 20

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Змейка")


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(window_width // 2, window_height // 2)]
        self.direction = random.choice(["up", 'down', 'left', 'right'])
        self.color = GREEN

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(window, self.color, (position[0], position[1], cell_size, cell_size))


class Game:
    def __init__(self):
        self.snake = Snake()
        self.score = 0

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw()

    def draw(self):
        window.fill(BLACK)
        self.snake.draw()
        pygame.display.update()


game = Game()
game.play()

