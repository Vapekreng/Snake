# TODO: Hfpyst dbls tls
# TODO: Очки (в том числе за упраляющие нажатия и ожидание)
# TODO: Отображение статистики
# TODO: Рекорды
# TODO: Цвет змеи в зависимости от скорости

from bearlibterminal import terminal
import random

SNAKE_HEADS_CHAR = 'O'
SNAKE_BODIES_CHAR = '*'
FOOD = 'X'
INIT_DELAY = 500000
ACCELERATION = 0.95
INIT_SNAKES_LEN = 5
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 25
START_SNAKE = [[35, 10], [36, 10], [37, 10], [38, 10], [39, 10]]
START_DIRECTION = 'left'
DIRECTION_TO_VECTOR = {'left': [-1, 0], 'right': [1, 0], 'up': [0, -1], 'down': [0, 1], }
CODE_TO_DIRECTION = {terminal.TK_LEFT: 'left', terminal.TK_RIGHT: 'right', terminal.TK_UP: 'up',
                     terminal.TK_DOWN: 'down'}


class Snake:

    def __init__(self):
        self.is_alive = True
        self.body = START_SNAKE
        self.direction = 'left'

    def set_new_direction(self, new_direction):
        answer = 'not changed'
        old_vector = DIRECTION_TO_VECTOR[self.direction]
        new_vector = DIRECTION_TO_VECTOR[new_direction]
        reverse = (old_vector[0] + new_vector[0] == 0) and (old_vector[1] + new_vector[1] == 0)
        if not reverse:
            self.direction = new_direction
            answer = 'changed'
        return answer

    def move(self):
        n = len(self.body)
        head = self.body[0]
        vector = DIRECTION_TO_VECTOR[self.direction]
        x = (head[0] + vector[0]) % SCREEN_WIDTH
        y = (head[1] + vector[1]) % SCREEN_HEIGHT
        self.body[0] = [x, y]
        for i in range(n - 2):
            self.body[n - i - 1] = self.body[n - i - 2]
        self.body[1] = head
        if self.body[0] in self.body[1:]:
            self.is_alive = False

    def eat(self):
        tail = self.body[-1]
        self.move()
        self.body.append(tail)


class Level:

    def __init__(self):
        self.snake = Snake()
        self.food = None
        self.add_food()
        self.delay = INIT_DELAY

    def add_food(self):
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        while [x, y] in self.snake.body:
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)
        self.food = [x, y]

    def print(self):
        terminal.clear()
        body = self.snake.body
        n = len(body)
        for i in range(1, n - 1):
            x, y = body[i]
            char = SNAKE_BODIES_CHAR
            terminal.printf(x, y, char)
        x = self.food[0]
        y = self.food[1]
        text = FOOD
        terminal.printf(x, y, text)
        x, y = body[0]
        char = SNAKE_HEADS_CHAR
        terminal.printf(x, y, char)
        terminal.refresh()

    def run(self):
        terminal.open()
        terminal.set('font: UbuntuMono-R.ttf, size = 24')
        snake = self.snake
        self.add_food()
        self.print()
        while snake.is_alive:
            new_direction = get_new_direction(self.delay)
            if new_direction in DIRECTION_TO_VECTOR.keys():
                self.snake.set_new_direction(new_direction)
            snake.move()
            if snake.body[0] == self.food:
                snake.eat()
                self.add_food()
                self.delay = int(ACCELERATION * self.delay)
            self.print()
        terminal.color('red')
        self.print()
        terminal.read()
        terminal.close()


def get_new_direction(delay):
    new_direction = 'no direction'
    for i in range(delay):
        if terminal.has_input():
            key = terminal.read()
            if key in CODE_TO_DIRECTION.keys():
                new_direction = CODE_TO_DIRECTION[key]
                break
    return new_direction


level = Level()
level.run()
