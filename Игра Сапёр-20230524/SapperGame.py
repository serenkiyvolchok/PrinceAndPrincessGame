import copy
import random as rnd
from enum import Enum


class SapperGameState(Enum):
    PLAYING = 0  # игра не закончена
    WIN = 1      # игра закончена победой
    FAIL = 2     # игра закончена поражением


class SapperCellState(Enum):
    HIDDEN = 0   # клетка закрыта
    OPEN = 1     # клетка открыта("разминированна")
    FLAG = 2     # установлен флаг(предполагается в этой клетке мина)
    PROBLEM = 3  # установлен вопрос(сомнения насчет наличия в клетке мины)


class SapperCell:
    def __init__(self, mine: bool=False, around: int=0, state: SapperCellState=SapperCellState.HIDDEN):
        self._mine = mine      # есть ли мина в клетке
        self._around = around  # кол-во мин вокруг
        self._state = state    # состояние клетки

    @property
    def mine(self) -> bool:
        return self._mine

    @property
    def around(self) -> int:
        return self._around

    @property
    def state(self) -> SapperCellState:
        return self._state


class SapperGame:
    def __init__(self, row_count: int, col_count: int, mine_count: int):
        self._row_count = row_count
        self._col_count = col_count
        self._mine_count = mine_count
        self.new_game()

    def new_game(self) -> None:
        self._field = [
            copy.deepcopy([SapperCell() for c in range(self.col_count)])
            for r in range(self.row_count)
        ]

        for p in rnd.sample([
            (r, c)
            for r in range(self.row_count)
            for c in range(self.col_count)
        ], self.mine_count):
            self[p]._mine = True

        for r in range(self.row_count):
            for c in range(self.col_count):
                for rr in range(max(r - 1, 0), min(r + 2, self.row_count)):
                    for cc in range(max(c - 1, 0), min(c + 2, self.col_count)):
                        if (r, c) != (rr, cc) and self[rr, cc].mine:
                            self._field[r][c]._around += 1

        self._state = SapperGameState.PLAYING

    @property
    def row_count(self) -> int:
        return self._row_count

    @property
    def col_count(self) -> int:
        return self._col_count

    @property
    def mine_count(self) -> int:
        return self._mine_count

    @property
    def state(self) -> SapperGameState:
        return self._state

    def __getitem__(self, indices: tuple) -> SapperCell:
        #return SapperCell(False, rnd.randint(1, 8), SapperCellState.OPEN)
        return self._field[indices[0]][indices[1]]

    def _cells(self):
        for r in range(self.row_count):
            for c in range(self.col_count):
                yield self[r, c]

    def _update_playing_state(self):
        if any(cell for cell in self._cells() if cell.mine and cell.state == SapperCellState.OPEN):
            self._state = SapperGameState.FAIL
        elif sum(1 for cell in self._cells() if cell.state == SapperCellState.OPEN) == \
                self.row_count * self.col_count - self.mine_count:
            self._state = SapperGameState.WIN
        else:
            self._state = SapperGameState.PLAYING

    def left_mouse_click(self, row: int, col: int) -> None:
        if self.state != SapperGameState.PLAYING:
            return
        cell = self[row, col]
        if cell.state == SapperCellState.OPEN:
            return
        if cell.mine:
            cell._state = SapperCellState.OPEN
            self._state = SapperGameState.FAIL
            return

        cell._state = SapperCellState.OPEN
        opened = [copy.copy([False] * self.col_count) for c in range(self.row_count)]
        opened[row][col] = True
        while True:
            count = 0
            for r in range(self.row_count):
                for c in range(self.col_count):
                    if opened[r][c] and self[r, c].around == 0:
                        for rr in range(max(r - 1, 0), min(r + 2, self.row_count)):
                            for cc in range(max(c - 1, 0), min(c + 2, self.col_count)):
                                if not opened[rr][cc] and not self[rr, cc].mine:
                                    self[rr, cc]._state = SapperCellState.OPEN
                                    opened[rr][cc] = True
                                    count += 1
            if count == 0:
                break

        self._update_playing_state()

    def right_mouse_click(self, row: int, col: int) -> None:
        if self.state != SapperGameState.PLAYING:
            return
        pass
