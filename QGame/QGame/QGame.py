import copy
from enum import Enum

from PyQt5.uic.properties import QtWidgets


class QGameState(Enum):
    PLAYING = 0  # игра не закончена
    END = 1  # игра закончена


class QGameCellState(Enum):
    BLOCK = 0
    REDBLOCK = 1
    BLUEBLOCK = 2
    REDBALL = 4
    BLUEBALL = 5
    EMPTY = 7

    W = 8
    I = 9
    N = 10
    EP = 11


class QGameCell:
    def __init__(self, state: QGameCellState = QGameCellState.EMPTY, x: int = 0, y: int = 0):
        self._state = state  # состояние клетки
        self.x = x
        self.y = y

    @property
    def state(self) -> QGameCellState:
        return self._state

    @property
    def x(self) -> QGameCellState:
        return self._x

    @property
    def y(self) -> QGameCellState:
        return self._y

    @state.setter
    def state(self, value):
        self._state = value

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value


class QGame:

    def __init__(self, level: list):
        self._level = level
        self.selected_figure = None
        self.selected_direction = None
        self.new_game()

    def new_game(self) -> None:
        self._field = [
            copy.deepcopy([QGameCell() for element in row])
            for row in self.level
        ]

        for row in range(len(self.level)):
            for element in range(len(self.level[row])):
                if self.level[row][element] == 0:
                    self._field[row][element].state = QGameCellState.BLOCK
                if self.level[row][element] == 1:
                    self._field[row][element].state = QGameCellState.REDBLOCK
                if self.level[row][element] == 2:
                    self._field[row][element].state = QGameCellState.BLUEBLOCK
                if self.level[row][element] == 4:
                    self._field[row][element].state = QGameCellState.REDBALL
                if self.level[row][element] == 5:
                    self._field[row][element].state = QGameCellState.BLUEBALL

        self._state = QGameState.PLAYING

    @property
    def level(self) -> list:
        return self._level

    @property
    def state(self) -> QGameState:
        return self._state

    def __getitem__(self, indices: tuple) -> QGameCell:
        return self._field[indices[0]][indices[1]]

    def _cells(self):
        for row in self.level:
            for element in row:
                yield self[row, element]

    def _update_playing_state(self):
        for row in range(len(self.level)):
            for element in range(len(self.level[row])):
                if (self._field[row][element].state == QGameCellState.REDBALL) or (self._field[row][element].state == QGameCellState.BLUEBALL):
                    self._state = QGameState.PLAYING
                    return
                else:
                    self._state = QGameState.END

    def move_ball(self):
        row_cell = self.selected_figure.y
        col_cell = self.selected_figure.x
        row_direction = self.selected_direction.y
        col_direction = self.selected_direction.x

        state = self.selected_figure.state
        self._field[row_cell][col_cell].state = QGameCellState.EMPTY

        if row_direction == row_cell and col_cell > col_direction:
            while self._field[row_direction][col_direction].state == QGameCellState.EMPTY:
                col_direction = col_direction - 1
            if (self._field[row_direction][col_direction].state == QGameCellState.REDBLOCK and state == QGameCellState.REDBALL) or (self._field[row_direction][col_direction].state == QGameCellState.BLUEBLOCK and state == QGameCellState.BLUEBALL):
                return
            self._field[row_direction][col_direction + 1].state = state
        if col_direction == col_cell and row_direction > row_cell:
            while self._field[row_direction][col_direction].state == QGameCellState.EMPTY:
                row_direction = row_direction + 1
            if (self._field[row_direction][col_direction].state == QGameCellState.REDBLOCK and state == QGameCellState.REDBALL) or (self._field[row_direction][col_direction].state == QGameCellState.BLUEBLOCK and state == QGameCellState.BLUEBALL):
                return
            self._field[row_direction - 1][col_direction].state = state
        if col_direction == col_cell and row_cell > row_direction:
            while self._field[row_direction][col_direction].state == QGameCellState.EMPTY:
                row_direction = row_direction - 1
            if (self._field[row_direction][col_direction].state == QGameCellState.REDBLOCK and state == QGameCellState.REDBALL) or (self._field[row_direction][col_direction].state == QGameCellState.BLUEBLOCK and state == QGameCellState.BLUEBALL):
                return
            self._field[row_direction + 1][col_direction].state = state
        if row_direction == row_cell and col_direction > col_cell:
            while self._field[row_direction][col_direction].state == QGameCellState.EMPTY:
                col_direction = col_direction + 1
            if (self._field[row_direction][col_direction].state == QGameCellState.REDBLOCK and state == QGameCellState.REDBALL) or (self._field[row_direction][col_direction].state == QGameCellState.BLUEBLOCK and state == QGameCellState.BLUEBALL):
                return
            self._field[row_direction][col_direction - 1].state = state

    def left_mouse_click(self, row: int, col: int) -> None:
        if self.state != QGameState.PLAYING:
            return
        cell = QGameCell(self[row, col].state, col, row)
        if (cell.state != QGameCellState.REDBALL) and (cell.state != QGameCellState.BLUEBALL):
            self.selected_figure = None
            return
        else:
            self.selected_figure = cell

    def right_mouse_click(self, row: int, col: int) -> None:
        if self.state != QGameState.PLAYING:
            return
        cell = QGameCell(self[row, col].state, col, row)
        if cell.state != QGameCellState.EMPTY:
            self.selected_direction = None
            return
        else:
            self.selected_direction = cell
        if self.selected_direction is not None and self.selected_figure is not None:
            if (row == self.selected_figure.y) or (col == self.selected_figure.x):
                self.move_ball()
            else:
                return

        self._update_playing_state()

        if self._state == QGameState.END:
            self._field[2][1].state = QGameCellState.W
            self._field[2][2].state = QGameCellState.I
            self._field[2][3].state = QGameCellState.N
            self._field[2][4].state = QGameCellState.EP




