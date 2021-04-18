import pygame
import sys
from random import randint

_red = (255, 0, 0)
_green = (0, 255, 0)
_blue = (0, 0, 255)
_black = (0, 0, 0)
_boxsize = 20


class Box:
    def __init__(self, pos, v):
        self.rect = pygame.Rect(pos[0] * _boxsize, pos[1] * _boxsize, _boxsize, _boxsize)
        self.position = pos
        self.velocity = v

    def move(self):
        self.rect.move_ip(self.velocity[0] * _boxsize, self.velocity[1] * _boxsize)
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def reset(self):
        self.rect.x = self.position[0] * _boxsize
        self.rect.y = self.position[1] * _boxsize

    def __eq__(self, other):
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]

    def __repr__(self):
        return "Position: {}\nVelocity: {}".format(self.position, self.velocity)


class Snake:
    def __init__(self, hard_walls=False, debug=False):
        self.snake = [Box([20, 20], [0, 0])]
        self.moving = [0, 0]
        self.hard_walls = hard_walls
        self.apple_exists = False
        self.debug_mode = debug
        self.game_over = False
        self._create_apple()

    def parse_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_LEFT:
                    self.moving = [-1, 0] if self.moving[0] != 1 else [1, 0]
                elif key == pygame.K_RIGHT:
                    self.moving = [1, 0] if self.moving[0] != -1 else [-1, 0]
                elif key == pygame.K_UP:
                    self.moving = [0, -1] if self.moving[1] != 1 else [0, 1]
                elif key == pygame.K_DOWN:
                    self.moving = [0, 1] if self.moving[1] != -1 else [0, -1]
                elif key == pygame.K_SPACE:
                    if self.debug_mode:
                        self.apple_exists = False

    def set_move(self, move):
        self.moving = move

    def _create_apple(self):
        if self.apple_exists:
            return
        self.apple = Box([randint(0, 40), randint(0, 40)], [0, 0])
        self.apple_exists = True

    def handle_collision(self):
        head = self.snake[0]
        tail = self.snake[-1]
        if self.hard_walls:
            if (head.position[0] < 0 or head.position[0] > 40 or
                    head.position[1] < 0 or head.position[1] > 40):
                self.game_over = True
        for box in self.snake:
            if box.position[0] < 0:
                box.position[0] = 40
                box.reset()
            if box.position[0] > 40:
                box.position[0] = 0
                box.reset()
            if box.position[1] < 0:
                box.position[1] = 40
                box.reset()
            if box.position[1] > 40:
                box.position[1] = 0
                box.reset()
        for box in self.snake[1:]:
            if head == box:
                self.game_over = True

        if head == self.apple:
            self.apple_exists = False
            self.snake.append(Box([tail.position[0] - tail.velocity[0], tail.position[1] - tail.velocity[1]], [0, 0]))

    def update_velocities(self):
        for i in reversed(range(1, len(self.snake))):
            self.snake[i].velocity = self.snake[i-1].velocity.copy()
        self.snake[0].velocity = self.moving.copy()

    def step(self, screen, return_results=False):
        if self.game_over:
            return
        self.update_velocities()

        self._create_apple()

        screen.fill(_black)
        pygame.draw.rect(screen, _red, self.apple)
        for body in self.snake:
            pygame.draw.rect(screen, _green, body.rect)
            body.move()
        self.handle_collision()
        pygame.display.flip()

        if return_results:
            return self.snake, self.apple, self.apple_exists, self.game_over


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((41 * _boxsize, 41 * _boxsize))
    pygame.display.set_caption("Snake")
    game = Snake()
    clock = pygame.time.Clock()
    while True:
        game.parse_event()
        game.step(screen)
        clock.tick(15)
