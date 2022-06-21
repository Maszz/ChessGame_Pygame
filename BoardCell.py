from lib2to3 import pygram
import pygame
from typing import Tuple, TYPE_CHECKING
from Store import Store


if TYPE_CHECKING:
    from Board import Board
    from BoardCell import BoardCell
    from ChessPiece import ChessPieces


class BoardCell:
    def __init__(self, surface: pygame.Surface, x: int, y: int, w: int, h: int, color: Tuple[int, int, int], hlcColor: Tuple[int, int, int]) -> None:
        self.store = Store()
        self.screen = surface
        self.boardCell = pygame.draw.rect(surface, color,
                                          (x, y, w, h), 0)

        # info for static draw
        self.screen = surface
        self.color = color
        self.geo = (x, y, w, h)

        self.cellSize: int = self.store.__getitem__("cellSize").getState()
        self.pieceOnCell: 'ChessPieces' = None
        self.col = int(x/self.cellSize)
        self.row = int(y/self.cellSize)
        self.selected: bool = False
        self.hlc = hlcColor
        self.colorToRender = self.color
        self.updateFlags = None

    def __str__(self):
        return f'{BoardCell} @ col:{self.col} row:{self.row}'

    def setSelected(self, selected: bool) -> None:
        self.selected = selected
        if selected:
            self.colorToRender = self.hlc
        else:
            self.colorToRender = self.color

    def setPieceOnCell(self, pieceOnCell: 'ChessPieces') -> None:
        self.pieceOnCell = pieceOnCell
        if pieceOnCell == None:
            return
        self.pieceOnCell.move(self.col, self.row)
        # pieceOnCell(self.col, self.row)

    def getPieceOnCell(self) -> 'ChessPieces':
        return self.pieceOnCell

    def setUpdateFlag(self, updateFlag: int) -> None:
        self.updateFlags = updateFlag

    def update(self):

        pygame.draw.rect(self.screen, self.colorToRender,
                         self.geo, 0)
        if self.pieceOnCell is not None:
            self.pieceOnCell.draw()
        if self.updateFlags == 0:

            if self.color == (238, 238, 213):
                pygame.draw.circle(self.screen, (214, 214, 191),
                                   (int(self.geo[0]+(self.geo[2]/2)), int(self.geo[1]+(self.geo[3]/2))), int(self.cellSize/6), 0)
            else:

                pygame.draw.circle(self.screen, (111, 134, 84),
                                   (int(self.geo[0]+(self.geo[2]/2)), int(self.geo[1]+(self.geo[3]/2))), int(self.cellSize/6), 0)
            print("Draw cricle")
            # self.updateFlags = None
        if self.updateFlags == 1:
            if self.color == (238, 238, 213):
                pygame.draw.circle(self.screen, (214, 214, 189),
                                   (int(self.geo[0]+(self.geo[2]/2)), int(self.geo[1]+(self.geo[3]/2))), int(self.cellSize/2), 10)
            else:
                pygame.draw.circle(self.screen, (106, 135, 77),
                                   (int(self.geo[0]+(self.geo[2]/2)), int(self.geo[1]+(self.geo[3]/2))), int(self.cellSize/2), 10)

        # else:
