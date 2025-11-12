from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Класс описывает объект игры.
    Является родительским классом для объектов игры.
    """

    position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def __init__(
        self,
        position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color=(0, 0, 0)
    ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки поля."""
        pass


class Apple(GameObject):
    """Класс описывает объект игры - яблоко."""

    body_color = (255, 0, 0)

    def __init__(self):
        self.randomize_position()
        super().__init__(self.position, self.body_color)

    def randomize_position(self):
        """Задает рандномую позицию яблока на поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывает объект игры - змейку."""

    length = 1
    positions = [GameObject.position]
    direction = RIGHT
    next_direction = None
    body_color = (0, 255, 0)

    def __init__(self):
        self.last = None
        super().__init__(self.position, self.body_color)

    def update_direction(self):
        """Обновляет направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод отвечает за добавление нового сегмента змейки."""
        x, y = self.get_head_position()
        x_greed = x // GRID_SIZE + self.direction[0]
        y_greed = y // GRID_SIZE + self.direction[1]
        if x_greed >= GRID_WIDTH:
            x_greed = 0
        elif x_greed < 0:
            x_greed = GRID_WIDTH - 1
        if y_greed >= GRID_HEIGHT:
            y_greed = 0
        elif y_greed < 0:
            y_greed = GRID_HEIGHT - 1
        x = x_greed * GRID_SIZE
        y = y_greed * GRID_SIZE

        self.last = self.positions[-1]
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на поле."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает положение головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку к исходным настройкам"""
        self.length = 1
        self.positions = [GameObject.position]
        self.direction = choice((LEFT, RIGHT, UP, DOWN))
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обрабатывает нажатие клавиш пользователем."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Описывает основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        if snake.next_direction:
            snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
