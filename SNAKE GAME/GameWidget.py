from random import choice

from PyQt5.QtCore import QRect, QTime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPaintEvent, QPen, QColor, QBrush, QKeyEvent, QResizeEvent
from PyQt5.QtWidgets import QWidget


class Snake:
    def __init__(self):
        self.body_positions = [[4, 2], [3, 2], [2, 2]]
        self.orientation = "Right"
        self.deaths_counter = 0
        self.color_head = QColor(0, 255, 0)
        self.color_body = QColor(0, 200, 0)

    @property
    def deaths(self):
        self.deaths_counter += 1
        return self.deaths_counter

    @property
    def snake_length(self):
        return len(self.body_positions)

    @property
    def head(self):
        return self.body_positions[0]

    def reset(self):
        self.body_positions = [[4, 2], [3, 2], [2, 2]]
        self.orientation = "Right"

    def grow(self):
        self.body_positions.append(self.body_positions[-1].copy())

    def move_forward(self):
        self.body_positions.insert(0, self.body_positions[0].copy())
        if self.orientation == "Right":
            self.body_positions[0][0] += 1
        elif self.orientation == "Left":
            self.body_positions[0][0] -= 1
        elif self.orientation == "Up":
            self.body_positions[0][1] -= 1
        else:
            self.body_positions[0][1] += 1
        self.body_positions.pop()

    def set_orientation(self, orientation: str):
        if self.orientation == "Right" and orientation == "Left":
            pass
        elif self.orientation == "Up" and orientation == "Down":
            pass
        elif self.orientation == "Left" and orientation == "Right":
            pass
        elif self.orientation == "Down" and orientation == "Up":
            pass
        else:
            self.orientation = orientation
            self.move_forward()

    def move_up(self):
        self.set_orientation("Up")

    def move_down(self):
        self.set_orientation("Down")

    def move_right(self):
        self.set_orientation("Right")

    def move_left(self):
        self.set_orientation("Left")


class GameWidget(QWidget):
    GRID_SIZE = 15

    def __init__(self, main_window):
        QWidget.__init__(self)
        self.snake = Snake()
        self.main_window = main_window

        self.pen_grid = QPen(QColor(0, 0, 0))
        self.pen_grid.setWidth(1)

        self.brush_snake = QBrush(self.snake.color_head)
        self.brush_food = QBrush(QColor(255, 0, 0))
        self.timer = QTime()
        self.frame_count = 1

        self.food_position = self.create_food()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_W or event.key() == Qt.Key_Up:
            self.snake.set_orientation("Up")
        elif event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
            self.snake.set_orientation("Left")
        elif event.key() == Qt.Key_S or event.key() == Qt.Key_Down:
            self.snake.set_orientation("Down")
        elif event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
            self.snake.set_orientation("Right")
        elif event.key() == Qt.Key_G:
            self.snake.grow()
        elif event.key() == Qt.Key_P:
            pass
        self.update()

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)

        if self.frame_count == 1:
            self.timer.start()

        """
        Automaticly moves snake every second
        try:
            if self.frame_count % round(1000 / (self.timer.elapsed() / self.frame_count)) == 0:
                self.snake.move()
        except ZeroDivisionError:
            pass
        """
        self.check_snake_food_collision()
        self.check_snake_body_collision()
        self.check_snake_boundary_collision()

        self.draw_grid(qp)
        self.draw_snake(qp)
        self.draw_food(qp)

        self.frame_count += 1

    def draw_grid(self, qp):
        x, y = self.width(), self.height()
        qp.setPen(self.pen_grid)

        for i in range(x//GameWidget.GRID_SIZE):
            qp.drawLine(0 + i * GameWidget.GRID_SIZE, 0,
                        i * GameWidget.GRID_SIZE, y - y % GameWidget.GRID_SIZE - GameWidget.GRID_SIZE)

        for i in range(y//GameWidget.GRID_SIZE):
            qp.drawLine(0, i * GameWidget.GRID_SIZE,
                        x - x % GameWidget.GRID_SIZE - GameWidget.GRID_SIZE, i * GameWidget.GRID_SIZE)

    def draw_snake(self, qp):
        # Draws the head
        self.brush_snake.setColor(self.snake.color_head)
        qp.setBrush(self.brush_snake)
        qp.drawRect(QRect(self.snake.body_positions[0][0] * GameWidget.GRID_SIZE,
                          self.snake.body_positions[0][1] * GameWidget.GRID_SIZE,
                          GameWidget.GRID_SIZE, GameWidget.GRID_SIZE))
        # Draws the body
        temp_color = QColor(0, 200, 0)
        for i in range(1, self.snake.snake_length):
            temp_color.setGreen(255*(1-i/self.snake.snake_length))
            self.brush_snake.setColor(temp_color)
            qp.setBrush(self.brush_snake)
            qp.drawRect(QRect(self.snake.body_positions[i][0] * GameWidget.GRID_SIZE,
                              self.snake.body_positions[i][1] * GameWidget.GRID_SIZE,
                              GameWidget.GRID_SIZE, GameWidget.GRID_SIZE))

    def draw_food(self, qp):
        qp.setBrush(self.brush_food)
        qp.drawRect(QRect(self.food_position[0] * GameWidget.GRID_SIZE,
                          self.food_position[1] * GameWidget.GRID_SIZE,
                          GameWidget.GRID_SIZE, GameWidget.GRID_SIZE))

    def create_food(self):
        self.main_window.ui.label_food_count.setText(f"Food count: {self.snake.snake_length - 3}")
        self.main_window.ui.label_snake_length.setText(f"Snake length: {self.snake.snake_length}")

        x, y = self.width()//GameWidget.GRID_SIZE - 2, self.height()//GameWidget.GRID_SIZE - 2
        # Avoids spawning food inside the snake's body
        avaiable_cells = []
        for i in range(x):
            for j in range(y):
                if not [i, j] in self.snake.body_positions:
                    avaiable_cells.append((i, j))
        return choice(avaiable_cells)

    def check_snake_body_collision(self):
        if any(self.snake.head.copy() == i for i in self.snake.body_positions[1:].copy()):
            # Currently bugged
            # msg = QMessageBox()
            # msg.setWindowTitle("Game over!")
            # msg.setText("Snake has eaten itself!")
            # msg.exec()
            self.main_window.ui.label_death_counter.setText(f"Deaths counter: {self.snake.deaths}")
            self.snake.reset()
            self.food_position = self.create_food()

    def check_snake_food_collision(self):
        if tuple(self.snake.head) == self.food_position:
            self.snake.grow()
            self.food_position = self.create_food()

    def check_snake_boundary_collision(self):
        x, y = self.width() // GameWidget.GRID_SIZE - 1, self.height() // GameWidget.GRID_SIZE - 1
        if self.snake.head[0] < 0 or self.snake.head[1] < 0 or self.snake.head[0] == x or self.snake.head[1] == y:
            self.main_window.ui.label_death_counter.setText(f"Death count: {self.snake.deaths}")
            self.snake.reset()
            self.food_position = self.create_food()

    @property
    def cell_number(self):
        return self.width() // GameWidget.GRID_SIZE - 1, self.height() // GameWidget.GRID_SIZE - 1

    def resizeEvent(self, event: QResizeEvent):
        self.snake.reset()
        self.food_position = self.create_food()
        QWidget.resizeEvent(self, event)
