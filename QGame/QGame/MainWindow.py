import os

from MainWindowUI import Ui_MainWindow as MainWindowUI
from QGame import *

from PyQt5 import QtSvg
from PyQt5.QtGui import QMouseEvent, QPainter, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import QModelIndex, QRectF, Qt


def read_level(file):
    lst = [line.replace("\n", "").split() for line in file]
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst[i][j] = int (lst[i][j])
    return lst


def select_level(value):
    if value == 1:
        file = open("level1.txt", "r")
    if value == 2:
        file = open("level2.txt", "r")
    level = read_level(file)
    return level


class MainWindow(QMainWindow, MainWindowUI):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.level = [[0, 0, 0, 0, 0, 0],
                      [0, 7, 7, 7, 7, 0],
                      [0, 7, 4, 2, 7, 0],
                      [0, 7, 1, 5, 7, 0],
                      [0, 7, 7, 7, 7, 0],
                      [0, 0, 0, 0, 0, 0]]
        self.level_value = 1
        self.click_flag = False
        self.setupUi(self)

        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        self._images = {
            os.path.splitext(f)[0]: QtSvg.QSvgRenderer(os.path.join(images_dir, f))
            for f in os.listdir(images_dir)
        }

        self._game = QGame(self.level)
        self.game_resize(self._game)

        class MyDelegate(QItemDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_item_paint(idx, painter, option)
                painter.restore()

        self.gameFieldTableView.setItemDelegate(MyDelegate(self))

        # такие ухищрения, т.к. не предусмотрено сигналов для правой кнопки мыши
        def new_mouse_press_event(e: QMouseEvent) -> None:
            idx = self.gameFieldTableView.indexAt(e.pos())
            self.on_item_clicked(idx, e)

        self.gameFieldTableView.mousePressEvent = new_mouse_press_event

        self.newGamePushButton.clicked.connect(self.on_new_game)

        self.exitGamePushButton.clicked.connect(self.close)

        self.levelSpinBox.valueChanged.connect(self.change_value_of_the_level)

        self.gamePushButton.clicked.connect(self.update_level)

    def change_value_of_the_level(self, value: int):
        self.level_value = value

    def update_level(self):
        self.level = select_level(self.level_value)
        self._game = QGame(self.level)
        self.game_resize(self._game)

    def game_resize(self, game: QGame) -> None:
        model = QStandardItemModel(len(game.level), len(game.level[1]))
        self.gameFieldTableView.setModel(model)
        self.update_view()

    def update_view(self):
        self.gameFieldTableView.viewport().update()

    def on_new_game(self):
        self._game = QGame(self._game.level)
        self.game_resize(self._game)
        self.update_view()

    def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
        item = self._game[e.row(), e.column()]
        if item.state == QGameCellState.BLOCK:
            img = self._images['block']
        elif item.state == QGameCellState.REDBLOCK:
            img = self._images['red_block']
        elif item.state == QGameCellState.BLUEBLOCK:
            img = self._images['blue_block']
        elif item.state == QGameCellState.REDBALL:
            img = self._images['red_ball']
        elif item.state == QGameCellState.BLUEBALL:
            img = self._images['blue_ball']
        elif item.state == QGameCellState.W:
            img = self._images['letter_w']
        elif item.state == QGameCellState.I:
            img = self._images['letter_i']
        elif item.state == QGameCellState.N:
            img = self._images['letter_n']
        elif item.state == QGameCellState.EP:
            img = self._images['exclamation_point']
        else:
            img = self._images['empty']
        img.render(painter, QRectF(option.rect))

    def on_item_clicked(self, e: QModelIndex, me: QMouseEvent = None) -> None:
        if me.button() == Qt.LeftButton:
            self._game.left_mouse_click(e.row(), e.column())
        elif me.button() == Qt.RightButton:
            self._game.right_mouse_click(e.row(), e.column())
            self.update_view()
