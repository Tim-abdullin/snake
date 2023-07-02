import pygame
import random

pygame.init()

window_width = 800
window_height = 600

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Змейка")


class Game:
    def __init__(self):
        self.score = 0

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


game = Game()
game.play()

