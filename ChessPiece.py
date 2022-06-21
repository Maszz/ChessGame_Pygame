import pygame
from Store import Store


class ChessPieces(pygame.sprite.Sprite):
    def __init__(self, name: str, board: pygame.Surface) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.store = Store()
        self.cellSize: int = self.store.__getitem__("cellSize").getState()

        pieceImage = pygame.image.load(f'assets/Pieces/{name}.png').convert_alpha()
        self.pieceImage = pygame.transform.scale(
            pieceImage, (self.cellSize, self.cellSize))
        self.name = name
        self.board = board
        self.row = None
        self.col = None
        self.piece = self.board.blit(
            self.pieceImage, (0,0))
        self.firstMove = True
        
    def move(self, col: int, row: int) -> None:
        self.col = col
        self.row = row
    
    # def capture(self,col: int, row: int) -> None:

    #     self.move(col,row)
    #     print(F"CAPTURE @ {self.col},{self.row}")

   
    def setIsFirstMove(self) -> None:
        if self.firstMove:
            self.firstMove = False
    def isFirstMove(self)->bool:
        return self.firstMove
        # self.updateSplite()

    # def update(self, *args: Any, **kwargs: Any) -> None:
    #     return super().update(*args, **kwargs)
    def draw(self) -> None:
        self.piece = self.board.blit(
            self.pieceImage,(self.cellSize*self.col,self.cellSize*self.row))
        print(F"REDRAW @ {self.col},{self.row}")
        # pygame.display.flip()
    