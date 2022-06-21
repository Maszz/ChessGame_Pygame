from typing import Tuple, List
import pygame

from Store import Store
from BoardCell import BoardCell
from ChessPiece import ChessPieces

import numpy as np


class Board:
    def __init__(self, screen: pygame.Surface) -> None:
        self.store = Store()
        self.screen = screen
        self.boardSize = self.screen.get_size()
        self.selectedCell = None
        self.status = "onGoing"
        self.cellSize = self.boardSize[0]/8
        self.store.__setitem__(
            "cellSize", self.store.storeItem[int](int(self.cellSize)))
        self.boardCell: List[List[BoardCell]] = []

        self.board = self.drawBoard()
        # self.boardCell[0][0].pieceOnCell = ChessPieces(
        #     "wp", 1, 1, self.board)
        self.drawInitializedPieces()
        self.screen.blit(self.board, (0, 0))

        print(self.boardCell[0][0], self.boardCell[0][1])
        self.update()

    def board_event_loop(self):
        # self.update()
        pass

    def drawValidMove(self, row, col):

        self.boardCell[row][col].setUpdateFlag(0)
        self.update()
        self.boardCell[row][col].setUpdateFlag(None)

    def selected_boardCell(self, row: int, col: int):
        if self.boardCell[row][col].pieceOnCell is not None:

            if self.selectedCell is None:
                self.boardCell[row][col].setSelected(True)
                self.selectedCell = (row, col)
            else:
                if self.selectedCell[0] == row and self.selectedCell[1] == col:
                    self.boardCell[self.selectedCell[0]
                                   ][self.selectedCell[1]].setSelected(False)
                    self.selectedCell = None
                    print("should this case")
                else:
                    self.boardCell[self.selectedCell[0]
                                   ][self.selectedCell[1]].setSelected(False)
                    self.boardCell[row][col].setSelected(True)
                    self.selectedCell = (row, col)

        self.update()

    def safe_move(self, row: int, col: int):
        """
        This function is called when a piece is selected and the user clicks on a empty cell.
        Algo : move the piece to the new cell w/ set pieceOnCell -> then set pieceOnCell of previous cell to `None` -> dehilighting the previous cell -> update the board
        """
        if self.selectedCell is not None:

            # if is an enemy this action is prefered to capturing the piece ** wrapper of this function should be carefull about the gameControll
            if self.boardCell[row][col].pieceOnCell is not None:
                if self.boardCell[row][col].pieceOnCell.name == "wk":
                    print("Winner is black")
                    self.status = "gameEnd black"
                    return True
                if self.boardCell[row][col].pieceOnCell.name == "bk":
                    print("Winner is white")
                    self.status = "gameEnd white"
                    return True

            self.boardCell[row
                           ][col].setPieceOnCell(self.boardCell[self.selectedCell[0]
                                                                ][self.selectedCell[1]].getPieceOnCell())

            selectedTemp = (self.selectedCell[0], self.selectedCell[1])

            # selected yourself for dehilighting cell when you move.
            self.selected_boardCell(selectedTemp[0], selectedTemp[1])
            # set pieceOnCell before move to None
            self.boardCell[selectedTemp[0]
                           ][selectedTemp[1]].setPieceOnCell(None)
            self.boardCell[row][col].getPieceOnCell().setIsFirstMove()

            self.update()

        return False

        # raise NotImplementedError

    def safe_capture(self, row, col):
        if self.selectedCell is not None:

            self.boardCell[row
                           ][col].setPieceOnCell(self.boardCell[self.selectedCell[0]
                                                                ][self.selectedCell[1]].getPieceOnCell())

            selectedTemp = (self.selectedCell[0], self.selectedCell[1])

            # selected yourself for dehilighting cell when you move.
            self.selected_boardCell(selectedTemp[0], selectedTemp[1])

            # set pieceOnCell before move to None
            self.boardCell[selectedTemp[0]
                           ][selectedTemp[1]].setPieceOnCell(None)

            self.boardCell[row][col].getPieceOnCell().setIsFirstMove()

            self.update()

    def update(self):
        self.board.fill((0, 0, 0, 0))

        for i in range(8):
            for j in range(8):
                self.boardCell[i][j].update()
                pass

        self.screen.blit(self.board, (0, 0))
        pygame.display.flip()
        print("Update")

    def drawInitializedPieces(self):
        for i in range(8):
            self.boardCell[1][i].setPieceOnCell(ChessPieces(
                "bp", self.board))
            self.boardCell[6][i].setPieceOnCell(ChessPieces(
                "wp", self.board))

        self.boardCell[0][0].setPieceOnCell(ChessPieces("br", self.board))
        self.boardCell[0][7].setPieceOnCell(ChessPieces("br", self.board))
        self.boardCell[7][0].setPieceOnCell(ChessPieces("wr", self.board))
        self.boardCell[7][7].setPieceOnCell(ChessPieces("wr", self.board))

        self.boardCell[0][1].setPieceOnCell(ChessPieces("bn", self.board))
        self.boardCell[0][6].setPieceOnCell(ChessPieces("bn", self.board))
        self.boardCell[7][1].setPieceOnCell(ChessPieces("wn", self.board))
        self.boardCell[7][6].setPieceOnCell(ChessPieces("wn", self.board))

        self.boardCell[0][2].setPieceOnCell(ChessPieces("bb", self.board))
        self.boardCell[0][5].setPieceOnCell(ChessPieces("bb", self.board))
        self.boardCell[7][2].setPieceOnCell(ChessPieces("wb", self.board))
        self.boardCell[7][5].setPieceOnCell(ChessPieces("wb", self.board))

        self.boardCell[0][3].setPieceOnCell(ChessPieces("bq", self.board))
        self.boardCell[0][4].setPieceOnCell(ChessPieces("bk", self.board))
        self.boardCell[7][3].setPieceOnCell(ChessPieces("wq", self.board))
        self.boardCell[7][4].setPieceOnCell(ChessPieces("wk", self.board))

        # a = np.array(self.boardCell)
        # c = np.rot90(a, 2)
        # self.boardCell = c

    def drawBoard(self) -> pygame.Surface:

        board = pygame.Surface(self.boardSize)
        board = board.convert()
        board.fill((255, 255, 255))

        # pygame.draw.rect(board, (0, 0, 0),
        #                  (0, 0, self.cellSize, self.cellSize), 1)

        for col in range(8):
            height = self.cellSize * col
            tempArr = list()
            for row in range(8):
                if (row % 2 == 0 and col % 2 == 0) or (col % 2 != 0 and row % 2 != 0):
                    # pygame.draw.rect(board, (0, 0, 0),
                    #                  (row * self.cellSize, height, self.cellSize, self.cellSize), 0)
                    tempArr.append(BoardCell(board, row * self.cellSize, height,
                                             self.cellSize, self.cellSize, (238, 238, 213), (246, 245, 149)))
                else:
                    # pygame.draw.rect(board, (255, 0, 0),
                    #                  (row * self.cellSize, height, self.cellSize, self.cellSize), 0)
                    tempArr.append(BoardCell(board, row * self.cellSize, height,
                                             self.cellSize, self.cellSize, (124, 149, 93), (189, 201, 89)))
                    # pygame.draw.rect(board, (0, 0, 0),
                    #                  (0, i * self.cellSize, self.cellSize, self.cellSize), 1)

            self.boardCell.append(tempArr)

        return board

    def getBoardPosition(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Get the board position
        retunr: Tuple[int, int] -> Pos [row,col]

        """
        return (int(pos[1] // self.cellSize), int(pos[0] // self.cellSize))
