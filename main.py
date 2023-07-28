import pygame
import random
import os

pygame.init()

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

CELL_SIZE = 50

img_food = pygame.transform.scale(pygame.image.load('images/Apple.png'), [CELL_SIZE, CELL_SIZE])

# Загрузка изображений для анимации головы змейки
HEAD_IMAGES = {
    "up": pygame.transform.scale(pygame.image.load(os.path.join("images", "head_up.png")), [CELL_SIZE, CELL_SIZE]),
    "down": pygame.transform.scale(pygame.image.load(os.path.join("images", "head_down.png")), [CELL_SIZE, CELL_SIZE]),
    "left": pygame.transform.scale(pygame.image.load(os.path.join("images", "head_left.png")), [CELL_SIZE, CELL_SIZE]),
    "right": pygame.transform.scale(pygame.image.load(os.path.join("images", "head_right.png")), [CELL_SIZE, CELL_SIZE])
}

# Загрузка изображений для туловища змейки
BODY_HORIZONTAL = pygame.transform.scale(pygame.image.load(os.path.join("images", "body_horizontal.png")), [CELL_SIZE, CELL_SIZE])
BODY_VERTICAL = pygame.transform.scale(pygame.image.load(os.path.join("images", "body_vertical.png")), [CELL_SIZE, CELL_SIZE])

# Загрузка изображений для хвоста змейки
TAIL_IMAGES = {
    "up": pygame.transform.scale(pygame.image.load(os.path.join("images", "tail_up.png")), [CELL_SIZE, CELL_SIZE]),
    "down": pygame.transform.scale(pygame.image.load(os.path.join("images", "tail_down.png")), [CELL_SIZE, CELL_SIZE]),
    "left": pygame.transform.scale(pygame.image.load(os.path.join("images", "tail_left.png")), [CELL_SIZE, CELL_SIZE]),
    "right": pygame.transform.scale(pygame.image.load(os.path.join("images", "tail_right.png")), [CELL_SIZE, CELL_SIZE])
}

BODY_TURN = pygame.transform.scale(pygame.image.load(os.path.join("images", "body_turn.png")), [CELL_SIZE, CELL_SIZE])

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.color = GREEN

    def draw(self):
        for index, position in enumerate(self.positions):
            if index == 0:  # Голова змейки
                img = HEAD_IMAGES[self.direction]
            elif index == len(self.positions) - 1:  # Хвост змейки
                img = TAIL_IMAGES[self.get_tail_direction()]
            else:
                if self.is_corner(index):  # Угол туловища змейки
                    img = pygame.transform.rotate(BODY_TURN, self.get_corner_angle(index))
                elif self.is_body_horizontal(index):  # Туловище змейки (горизонтальное)
                    img = BODY_HORIZONTAL
                else:  # Туловище змейки (вертикальное)
                    img = BODY_VERTICAL

            window.blit(img, position)

    def move(self):
        head_x, head_y = self.positions[0]
        if self.direction == 'up':
            head_y -= CELL_SIZE
        elif self.direction == 'down':
            head_y += CELL_SIZE
        elif self.direction == 'left':
            head_x -= CELL_SIZE
        elif self.direction == 'right':
            head_x += CELL_SIZE

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

    def get_tail_direction(self):
        tail_x, tail_y = self.positions[-1]
        second_to_last_x, second_to_last_y = self.positions[-2]

        if tail_x < second_to_last_x:
            return 'left'
        elif tail_x > second_to_last_x:
            return 'right'
        elif tail_y < second_to_last_y:
            return 'up'
        else:
            return 'down'

    def is_body_horizontal(self, index):
        x1, y1 = self.positions[index - 1]
        x2, y2 = self.positions[index]
        return x1 != x2

    def is_corner(self, index):
        if index < 1 or index >= len(self.positions) - 1:
            return False

        x1, y1 = self.positions[index - 1]
        x2, y2 = self.positions[index]
        x3, y3 = self.positions[index + 1]

        # Проверяем, является ли позиция туловища углом (вставляем проверку на угол)
        if (x1 - x2 == 0 and x2 - x3 == 0) or (y1 - y2 == 0 and y2 - y3 == 0):
            return False
        return True

    def get_corner_angle(self, index):
        x1, y1 = self.positions[index - 1]
        x2, y2 = self.positions[index]
        x3, y3 = self.positions[index + 1]

        if x2 == x1 and y2 > y1:
            if x2 < x3:
                return 0
            else:
                return 90
        elif x2 == x1 and y2 < y1:
            if x2 < x3:
                return 270
            else:
                return 180
        elif y2 == y1 and x2 > x1:
            if y2 < y3:
                return 180
            else:
                return 90
        elif y2 == y1 and x2 < x1:
            if y2 < y3:
                return 270
            else:
                return 0


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food_position = self.generate_food_pos()
        self.score = 0

    def generate_food_pos(self):
        while True:
            x = random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
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
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction('left')
                    elif event.key == pygame.K_RIGHT:
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
            or head[0] >= WINDOW_WIDTH
            or head[1] < 0
            or head[1] >= WINDOW_HEIGHT
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
        window.blit(img_food, (self.food_position[0], self.food_position[1], CELL_SIZE, CELL_SIZE))
        pygame.display.update()


game = Game()
game.play()
