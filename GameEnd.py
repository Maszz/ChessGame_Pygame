import pygame
from Components.Button import Button
import sys

from typing import Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from GameController import GameController
    from MainMenu import MainMenu


class GameEnd:
    def __init__(self, winner: str, gameController, mainMenu,):
        self.SCREEN = pygame.display.set_mode((1280, 720))
        self.winner = winner
        self.gameController: GameController = gameController
        self.mainMenu: MainMenu = mainMenu

        self.menu_event_loop()

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def menu_event_loop(self):
        while True:
            # SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            TITLE_TEXT = self.get_font(60).render(
                f"{self.winner} won the game.", True, "#b68f40")
            TITLE_RECT = TITLE_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(self.SCREEN, (640, 250),
                                 "PLAY AGAIN", self.get_font(40), "#d7fcd4", "White")
            MENU_BUTTON = Button(self.SCREEN, (640, 400),
                                 "GO BACK MENU", self.get_font(40), "#d7fcd4", "White")

            QUIT_BUTTON = Button(self.SCREEN, (640, 550),
                                 "QUIT", self.get_font(40), "#d7fcd4", "White")
            self.SCREEN.blit(TITLE_TEXT, TITLE_RECT)

            for button in [PLAY_BUTTON, MENU_BUTTON, QUIT_BUTTON]:
                button.changeState(MENU_MOUSE_POS)
                button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        game = self.gameController(self.mainMenu)
                        break

                    if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                        main = self.mainMenu()
                        break
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
