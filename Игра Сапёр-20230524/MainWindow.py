import os

from MainWindowUI import Ui_MainWindow as MainWindowUI
from SapperGame import *

from PyQt5 import QtSvg
from PyQt5.QtGui import QMouseEvent, QPainter, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import QModelIndex, QRectF, Qt


class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        self._images = {
            os.path.splitext(f)[0]: QtSvg.QSvgRenderer(os.path.join(images_dir, f))
            for f in os.listdir(images_dir)
        }

        self._game = SapperGame(10, 10, 20)
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

    def game_resize(self, game: SapperGame) -> None:
        model = QStandardItemModel(game.row_count, game.col_count)
        self.gameFieldTableView.setModel(model)
        self.update_view()

    def update_view(self):
        self.gameFieldTableView.viewport().update()

    def on_new_game(self):
        self._game = SapperGame(self._game.row_count, self._game.col_count, self._game.mine_count)
        self.game_resize(self._game)
        self.update_view()

    def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
        item = self._game[e.row(), e.column()]
        if item.state == SapperCellState.FLAG:
            img = self._images['flag']
        elif item.state == SapperCellState.PROBLEM:
            img = self._images['problem']
        elif item.state == SapperCellState.OPEN and item.mine:
            img = self._images['mine_red']
        elif item.state == SapperCellState.OPEN:
            img = self._images['type' + str(item.around)]
        else:
            img = self._images['closed']
        img.render(painter, QRectF(option.rect))

    def on_item_clicked(self, e: QModelIndex, me: QMouseEvent=None) -> None:
        if me.button() == Qt.LeftButton:
            self._game.left_mouse_click(e.row(), e.column())
        elif me.button() == Qt.RightButton:
            self._game.right_mouse_click(e.row(), e.column())
        self.update_view()
