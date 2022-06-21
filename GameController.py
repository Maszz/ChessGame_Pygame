
import pygame
from Board import Board
from Store import Store
from typing import Any, TypeVar, Generic, List
from ChessPiece import ChessPieces
from GameEnd import GameEnd


class GameController:

    def __init__(self, menu) -> None:
        self.store = Store()
        # self.initGlobalState()
        self.screen = pygame.display.set_mode((800, 800))
        self.exit_code = 0
        self.board = Board(self.screen)
        self.turn = "w"
        self.gameData = [[None for _ in range(8)] for _ in range(8)]

        self.menu = menu

        self.run_game_event_loop()

    def initGlobalState(self) -> None:
        raise NotImplementedError

    def nextTurn(self):
        if self.turn == "w":
            self.turn = "b"
        else:
            self.turn = "w"

    def run_game_event_loop(self) -> None:
        running = 1

        while (running == 1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                if event.type == pygame.MOUSEBUTTONUP and self.board.status == "onGoing":
                    pos = pygame.mouse.get_pos()
                    serilizedPos = self.board.getBoardPosition(pos)
                    print(self.board.getBoardPosition(pos))

                    # SOME deallocation bug.
                    # print(f"{self.board.boardCell[serilizedPos[0]][serilizedPos[1]].pieceOnCell.name[0] != self.turn} : {self.turn} {self.board.boardCell[serilizedPos[0]][serilizedPos[1]].pieceOnCell.name[0]}")
                    if self.board.selectedCell is not None and (self.board.boardCell[serilizedPos[0]][serilizedPos[1]].pieceOnCell is None or self.getValidMove(
                            self.board.boardCell[self.board.selectedCell[0]][self.board.selectedCell[1]].getPieceOnCell())[1]):  # or inkillalble
                        validMove = self.getValidMove(
                            self.board.boardCell[self.board.selectedCell[0]][self.board.selectedCell[1]].getPieceOnCell())

                        # if serilizedPos in validMove[1]:

                        if list(serilizedPos) in [*validMove[0], *validMove[1]]:
                            if self.board.safe_move(
                                    serilizedPos[0], serilizedPos[1]):  # if game is over safe_move should return true.
                                self.exit_code = 0
                                GameEnd(self.board.status.split(
                                    " ")[1], GameController, self.menu)
                                break
                            print("Next turn")
                            self.nextTurn()

                        if len(validMove[2]) != 0:
                            print(validMove[2])
                            if list(serilizedPos) == validMove[2][2]:
                                self.board.selected_boardCell(
                                    validMove[2][1][0], validMove[2][0])
                                self.board.safe_move(
                                    validMove[2][1][0], validMove[2][1][1])

                    else:
                        print("In else loop")
                        # print(self.board.boardCell[serilizedPos[0]][serilizedPos[1]].getPieceOnCell().name[0] , self.turn)
                        if self.board.boardCell[serilizedPos[0]][serilizedPos[1]].pieceOnCell is not None and self.board.boardCell[serilizedPos[0]][serilizedPos[1]].getPieceOnCell().name[0] == self.turn:
                            self.board.selected_boardCell(
                                serilizedPos[0], serilizedPos[1])

                            # if no selectedCell that mean we have selected same cell again or we have selected a empty cell
                            if self.board.selectedCell is not None:
                                print(
                                    self.board.selectedCell[0], self.board.selectedCell[1])

                                # draw valid path when clicked cell.
                                validMove = self.getValidMove(
                                    self.board.boardCell[self.board.selectedCell[0]][self.board.selectedCell[1]].getPieceOnCell())
                                print(validMove)
                                for move in validMove[0]:
                                    # self.board.drawValidMove(move[0], move[1])
                                    self.board.boardCell[move[0]
                                                         ][move[1]].setUpdateFlag(0)

                                for move in validMove[1]:
                                    # self.board.drawValidMove(move[0], move[1])
                                    self.board.boardCell[move[0]
                                                         ][move[1]].setUpdateFlag(1)

                                self.board.update()
                                for move in validMove[0]:
                                    self.board.boardCell[move[0]
                                                         ][move[1]].setUpdateFlag(None)
                                for move in validMove[1]:
                                    self.board.boardCell[move[0]
                                                         ][move[1]].setUpdateFlag(None)

                    # self.turn()

                self.board.board_event_loop()

    def getValidMove(self, chessPiece: ChessPieces) -> List[List[List[int]]]:
        """
        Output Shape should be (2,n,2)

        this non refactor version. for easy to read and debuging.

        """
        posMove = []
        posToCapture = []
        castlingMove = []
        side = chessPiece.name[0]

        if chessPiece.name == "bp":
            if self.board.boardCell[chessPiece.row+1][chessPiece.col].pieceOnCell is None:
                posMove.append([chessPiece.row + 1, chessPiece.col])
                if chessPiece.isFirstMove() and self.board.boardCell[chessPiece.row+2][chessPiece.col].pieceOnCell is None:

                    posMove.append([chessPiece.row + 2, chessPiece.col])

            posToCapture.append([chessPiece.row + 1, chessPiece.col-1])
            posToCapture.append([chessPiece.row + 1, chessPiece.col+1])

        if chessPiece.name == "wp":
            if self.board.boardCell[chessPiece.row-1][chessPiece.col].pieceOnCell is None:
                posMove.append([chessPiece.row - 1, chessPiece.col])
                if chessPiece.isFirstMove() and self.board.boardCell[chessPiece.row-2][chessPiece.col].pieceOnCell is None:
                    posMove.append([chessPiece.row - 2, chessPiece.col])
            posToCapture.append([chessPiece.row - 1, chessPiece.col-1])
            posToCapture.append([chessPiece.row - 1, chessPiece.col+1])

        if chessPiece.name == "br" or chessPiece.name == "wr":
            # casting type for syntax hilighting purpose.
            col = int(chessPiece.col)
            row = chessPiece.row
            # vertical Move
            # [1,2,3,4,5]
            # up
            for r in range(row-1, -1, -1):
                if self.board.boardCell[r][col].pieceOnCell is None:
                    posMove.append([r, col])
                else:
                    posToCapture.append([r, col])
                    break
            # down
            for r in range(row+1, 8):
                if self.board.boardCell[r][col].pieceOnCell is None:
                    posMove.append([r, col])
                else:
                    posToCapture.append([r, col])
                    break
            # horizontal move
            # left
            for c in range(col-1, -1, -1):
                if self.board.boardCell[row][c].pieceOnCell is None:
                    posMove.append([row, c])
                else:
                    posToCapture.append([row, c])
                    break
            # right
            for c in range(col+1, 8):
                if self.board.boardCell[row][c].pieceOnCell is None:
                    posMove.append([row, c])
                else:
                    posToCapture.append([row, c])
                    break

        if chessPiece.name == "wb" or chessPiece.name == "bb":
            col = int(chessPiece.col)
            row = chessPiece.row
            # posMove = []
            # (-1 -1) (-1 +1) (+1 -1) (+1 +1)

            # third quardrant digonal move.
            thridQuadrantCol = col
            for r in range(row-1, -1, -1):
                thridQuadrantCol -= 1
                if thridQuadrantCol == -1:
                    break
                if self.board.boardCell[r][thridQuadrantCol].pieceOnCell is None:
                    posMove.append([r, thridQuadrantCol])

                else:
                    posToCapture.append([r, thridQuadrantCol])
                    break
            # first quardrant digonal move.
            firstQuadrantCol = col
            for r in range(row+1, 8):
                firstQuadrantCol += 1
                if firstQuadrantCol == 8:
                    break
                if self.board.boardCell[r][firstQuadrantCol].pieceOnCell is None:
                    posMove.append([r, firstQuadrantCol])
                else:
                    posToCapture.append([r, firstQuadrantCol])
                    break

            fourthQuadrantCol = col
            for r in range(row+1, 8):
                fourthQuadrantCol -= 1
                if fourthQuadrantCol == 8:
                    break
                if self.board.boardCell[r][fourthQuadrantCol].pieceOnCell is None:
                    posMove.append([r, fourthQuadrantCol])
                else:
                    posToCapture.append([r, fourthQuadrantCol])
                    break
            secondQuadrantCol = col  # (7,5) -> (6,6) , (5,7)
            for r in range(row-1, -1, -1):
                secondQuadrantCol += 1
                print(f"DEBUG: {(r,secondQuadrantCol)}")
                if secondQuadrantCol == 8:
                    break
                if self.board.boardCell[r][secondQuadrantCol].pieceOnCell is None:
                    posMove.append([r, secondQuadrantCol])
                else:
                    posToCapture.append([r, secondQuadrantCol])
                    break
        if chessPiece.name == "bn" or chessPiece.name == "wn":
            col = int(chessPiece.col)
            row = chessPiece.row

            posMove.append([row+2, col-1])
            posMove.append([row+2, col+1])
            posMove.append([row-2, col-1])
            posMove.append([row-2, col+1])
            posMove.append([row+1, col-2])
            posMove.append([row+1, col+2])
            posMove.append([row-1, col-2])
            posMove.append([row-1, col+2])

            posToCapture.append([row+2, col-1])
            posToCapture.append([row+2, col+1])
            posToCapture.append([row-2, col-1])
            posToCapture.append([row-2, col+1])
            posToCapture.append([row+1, col-2])
            posToCapture.append([row+1, col+2])
            posToCapture.append([row-1, col-2])
            posToCapture.append([row-1, col+2])

            # posToCapture = list(filter(lambda pos: -1<pos[0] < 8 and -1<pos[1] < 8 and self.board.boardCell[pos[0]][pos[1]].pieceOnCell is None, posMove))
            posMove = list(filter(lambda pos: -1 < pos[0] < 8 and -1 < pos[1] < 8 and
                                  self.board.boardCell[pos[0]][pos[1]].pieceOnCell is None, posMove))

        if chessPiece.name == "bk" or chessPiece.name == "wk":
            col = int(chessPiece.col)
            row = chessPiece.row
            for r in range(-1, 2):
                for c in range(-1, 2):
                    if -1 < row+r < 8 and -1 < col+c < 8 and self.board.boardCell[row+r][col+c].pieceOnCell is None:
                        posMove.append([row+r, col+c])
                        posToCapture.append([row+r, col+c])
            # if chessPiece.name == "wk":
            if chessPiece.isFirstMove() and self.board.boardCell[row][col+1].pieceOnCell is None and self.board.boardCell[row][col+2].pieceOnCell is None:
                posMove.append([row, col+2])
                castlingMove.append(7)
                castlingMove.append([row, col+1])
                castlingMove.append([row, col+2])

            if chessPiece.isFirstMove() and self.board.boardCell[row][col-1].pieceOnCell is None and self.board.boardCell[row][col-2].pieceOnCell is None and self.board.boardCell[row][col-3].pieceOnCell is None:
                posMove.append([row, col-2])
                castlingMove.append(0)

                castlingMove.append([row, col-1])
                castlingMove.append([row, col-2])

        if chessPiece.name == "bq" or chessPiece.name == "wq":
            col = int(chessPiece.col)
            row = chessPiece.row
            # posMove = []
            # (-1 -1) (-1 +1) (+1 -1) (+1 +1)

            # third quardrant digonal move.
            thridQuadrantCol = col
            for r in range(row-1, -1, -1):
                thridQuadrantCol -= 1
                if thridQuadrantCol == -1:
                    break
                if self.board.boardCell[r][thridQuadrantCol].pieceOnCell is None:
                    posMove.append([r, thridQuadrantCol])

                else:
                    posToCapture.append([r, thridQuadrantCol])
                    break
            # first quardrant digonal move.
            firstQuadrantCol = col
            for r in range(row+1, 8):
                firstQuadrantCol += 1
                if firstQuadrantCol == 8:
                    break
                if self.board.boardCell[r][firstQuadrantCol].pieceOnCell is None:
                    posMove.append([r, firstQuadrantCol])
                else:
                    if self.board.boardCell[r][firstQuadrantCol].pieceOnCell.name[0] != side:
                        posToCapture.append([r, firstQuadrantCol])
                    break

            fourthQuadrantCol = col
            for r in range(row+1, 8):
                fourthQuadrantCol -= 1
                if fourthQuadrantCol == 8:
                    break
                if self.board.boardCell[r][fourthQuadrantCol].pieceOnCell is None:
                    posMove.append([r, fourthQuadrantCol])
                else:
                    posToCapture.append([r, fourthQuadrantCol])
                    break
            secondQuadrantCol = col  # (7,5) -> (6,6) , (5,7)
            for r in range(row-1, -1, -1):
                secondQuadrantCol += 1
                print(f"DEBUG: {(r,secondQuadrantCol)}")
                if secondQuadrantCol == 8:
                    break
                if self.board.boardCell[r][secondQuadrantCol].pieceOnCell is None:
                    posMove.append([r, secondQuadrantCol])
                else:
                    posToCapture.append([r, secondQuadrantCol])
                    break

            for r in range(row-1, -1, -1):
                if self.board.boardCell[r][col].pieceOnCell is None:
                    posMove.append([r, col])
                else:
                    posToCapture.append([r, col])
                    break
            # down
            for r in range(row+1, 8):
                if self.board.boardCell[r][col].pieceOnCell is None:
                    posMove.append([r, col])
                else:
                    posToCapture.append([r, col])
                    break
            # horizontal move
            # left
            for c in range(col-1, -1, -1):
                if self.board.boardCell[row][c].pieceOnCell is None:
                    posMove.append([row, c])
                else:
                    posToCapture.append([row, c])
                    break
            # right
            for c in range(col+1, 8):
                if self.board.boardCell[row][c].pieceOnCell is None:
                    posMove.append([row, c])
                else:
                    posToCapture.append([row, c])
                    break

        posToCapture = list(filter(lambda pos: -1 < pos[0] < 8 and -1 < pos[1] < 8 and self.board.boardCell[pos[0]][pos[1]
                                                                                                                    ].pieceOnCell is not None and self.board.boardCell[pos[0]][pos[1]].pieceOnCell.name[0] != side, posToCapture))

        return [posMove, posToCapture, castlingMove]
