import copy
import random as rnd
from enum import Enum


class GameState(Enum):
    PLAYING = 0  # игра не закончена
    WIN = 1      # игра закончена победой
    FAIL = 2     # игра закончена поражением


class CellState(Enum):
    ORDINARY = 0
    ACTIVE = 1
    WIN = 3


class CellColor(Enum):
    YELLOW = 0
    GREEN = 1
    BLUE = 2
    ANT = 3
    HOME = 4
    WIN = 5

class Cell:
    def __init__(self, x: int, y: int, state: CellState=CellState.ORDINARY,
                 color: CellColor=CellColor.BLUE):
        self._x = x
        self._y = y
        self._state = state
        self._color = color

    @property
    def state(self) -> CellState:
        return self._state

    @property
    def color(self) -> CellColor:
        return self._color

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    # def randomCellColor(self) -> CellColor:
    #     c = rnd.randint(0, 2)
    #     for i in CellColor:
    #         if i.value == c:
    #             color = i
    #     return color


class Game:
    def __init__(self, row_count: int, col_count: int, chain: list):
        self._row_count = row_count
        self._col_count = col_count
        self._chain = chain
        self.new_game()


    def new_game(self) -> None:
        self._field = [copy.deepcopy([Cell(r, c) for c in range(self.col_count)]) for r in range(self.row_count)]

        for cell in self._cells():
            c = rnd.randint(0, 2)
            for i in CellColor:
                if i.value == c:
                    cell._color = i

        r = rnd.randint(0, self.row_count-5)
        c = rnd.randint(0, self.col_count-1)
        self._field[r][c]._color = CellColor.ANT
        self._field[r+4][c]._color = CellColor.HOME

        self._state = GameState.PLAYING

    @property
    def row_count(self) -> int:
        return self._row_count

    @property
    def col_count(self) -> int:
        return self._col_count

    @property
    def state(self) -> GameState:
        return self._state

    def __getitem__(self, indices: tuple) -> Cell:
        return self._field[indices[0]][indices[1]]

    def _cells(self):
        for r in range(self.row_count):
            for c in range(self.col_count):
                yield self[r, c]

    def _update_playing_state(self):
        for r in range(self.row_count-1):
            for c in range(self.col_count-1):
                if (self._field[r][c].color == CellColor.ANT
                        and self._field[r-1][c].color == CellColor.HOME):
                    self._state = GameState.WIN
                    for c in self._cells():
                        c.state = CellState.WIN
        else:
            self._state = GameState.PLAYING

    def left_mouse_click(self, row: int, col: int) -> None:
        chain = self._chain
        if self.state != GameState.PLAYING:
            return
        cell = self._field[row][col]
        cell._x = row
        cell._y = col
        if cell.state == CellState.ORDINARY and not len(chain):
            cell._state = CellState.ACTIVE
            chain.append(cell)
            return
        elif (cell.state == CellState.ORDINARY and len(chain)
                and cell.color == chain[len(chain)-1].color and
                ((cell.x == chain[len(chain)-1].x and cell.y == chain[len(chain)-1].y-1) or
                (cell.x == chain[len(chain)-1].x and cell.y == chain[len(chain)-1].y+1)
                or (cell.x == chain[len(chain)-1].x-1 and cell.y == chain[len(chain)-1].y) or
                (cell.x == chain[len(chain)-1].x+1 and cell.y == chain[len(chain)-1].y))):
            cell._state = CellState.ACTIVE
            chain.append(cell)
            return
        elif cell.state == CellState.ACTIVE and cell == chain[len(chain)-1]:
            cell._state = CellState.ORDINARY
            chain.pop()
            return

        self._update_playing_state()

    def confirmChain (self):
        chain = self._chain
        if len(chain)>=2:
            for r in range(self.row_count-1, 0, -1):
                for c in range(self.col_count-1, 0, -1):

                    cell = self._field[r][c]

                    if cell in chain: # если шарик в выбранной цепочке
                        inChainInThisCol = 1
                        for i in range(r, 0, -1): # считаем количество шариков из цепочки в колонке
                            if self._field[i][c] in chain:
                                inChainInThisCol += 1
                        print(inChainInThisCol)

                        if inChainInThisCol < r+1: # случай, при котором шарики в колонке не доверху
                            remainingCellsInThisCol = r + 1 - inChainInThisCol
                            if remainingCellsInThisCol < inChainInThisCol:
                                # меняем на что хватит оставшихся шариков
                                for row in range(r, r-inChainInThisCol, -1):
                                    self._field[row][c]._color = self._field[r-inChainInThisCol][c]._color
                                # остальное в колонке - рандом
                                for row in range(r-inChainInThisCol, 0, -1):
                                    col = rnd.randint(0, 2)
                                    for j in CellColor:
                                        if j.value == c:
                                            self._field[row][c]._color = j

                            if remainingCellsInThisCol > inChainInThisCol:
                                # меняем все цепочные шарики на оставшиеся
                                print('fg')
                                # верхние строчки по количеству цепочных шариков рандомим


                        if inChainInThisCol == r+1: # случай, при котором шарики в колонке доверху
                            for k in range(r, 0, -1): # меняем цвет каждого шарика на рандом
                                col = rnd.randint(0, 2)
                                for j in CellColor:
                                    if j.value == c:
                                        self._field[k][c]._color = j

            for i in chain:
                i._state = CellState.ORDINARY # отменяем выделение цепочки
            self._chain = [] # очищаем цепочку

            return
        self._update_playing_state()

    def right_mouse_click(self, row: int, col: int) -> None:
        if self.state != GameState.PLAYING:
            return
        pass
