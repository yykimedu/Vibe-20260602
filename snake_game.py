import sys
import random
import pygame


class Snake:
    def __init__(self, pos, color=(0, 200, 0)):
        self.body = [pos]
        self.direction = (1, 0)
        self.grow_pending = 0
        self.color = color

    def set_direction(self, direction):
        # Prevent reversing directly
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        self.direction = direction

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

    def get_head(self):
        return self.body[0]


class Food:
    def __init__(self, grid_size, grid_w, grid_h, color=(200, 0, 0)):
        self.grid_size = grid_size
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.color = color
        self.position = (0, 0)
        self.randomize([])

    def randomize(self, forbidden):
        choices = [
            (x, y)
            for x in range(self.grid_w)
            for y in range(self.grid_h)
            if (x, y) not in forbidden
        ]
        if not choices:
            self.position = None
        else:
            self.position = random.choice(choices)


class Game:
    def __init__(self, grid_w=30, grid_h=20, grid_size=20, fps=10):
        pygame.init()
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.grid_size = grid_size
        self.width = grid_w * grid_size
        self.height = grid_h * grid_size
        self.fps = fps

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        start_pos = (grid_w // 2, grid_h // 2)
        self.snake = Snake(start_pos)
        self.food = Food(grid_size, grid_w, grid_h)
        self.food.randomize(self.snake.body)
        self.score = 0
        self.game_over = False

    def draw_rect(self, pos, color):
        x, y = pos
        rect = pygame.Rect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
        pygame.draw.rect(self.screen, color, rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_direction((1, 0))
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()

    def update(self):
        if self.game_over:
            return
        self.snake.move()

        head = self.snake.get_head()

        # wall collision
        if not (0 <= head[0] < self.grid_w and 0 <= head[1] < self.grid_h):
            self.game_over = True

        # self collision
        if self.snake.collides_with_self():
            self.game_over = True

        # food collision
        if head == self.food.position:
            self.snake.grow(1)
            self.score += 1
            self.food.randomize(self.snake.body)

    def draw(self):
        self.screen.fill((30, 30, 30))
        # draw food
        if self.food.position:
            self.draw_rect(self.food.position, self.food.color)

        # draw snake
        for i, segment in enumerate(self.snake.body):
            color = (0, 180, 0) if i == 0 else self.snake.color
            self.draw_rect(segment, color)

        if self.game_over:
            self.show_game_over()

        pygame.display.flip()

    def show_game_over(self):
        font = pygame.font.SysFont(None, 48)
        text = font.render(f'Game Over! Score: {self.score}', True, (255, 255, 255))
        rect = text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        self.screen.blit(text, rect)

        font2 = pygame.font.SysFont(None, 28)
        tip = font2.render('Press R to restart or close window to quit', True, (200, 200, 200))
        rect2 = tip.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(tip, rect2)

    def reset(self):
        start_pos = (self.grid_w // 2, self.grid_h // 2)
        self.snake = Snake(start_pos)
        self.food.randomize(self.snake.body)
        self.score = 0
        self.game_over = False

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    game = Game(grid_w=30, grid_h=20, grid_size=20, fps=10)
    game.run()
