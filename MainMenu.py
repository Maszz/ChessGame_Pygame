import pygame
from Components.Button import Button
import sys
from GameController import GameController


class MainMenu:
    def __init__(self, ):
        self.SCREEN = pygame.display.set_mode((1280, 720))
        self.menu_event_loop()

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def menu_event_loop(self):
        while True:
            # SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(self.SCREEN, (640, 250),
                                 "PLAY", self.get_font(50), "#d7fcd4", "White")
            MUL_BUTTON = Button(self.SCREEN, (640, 400),
                                "Multiplayer", self.get_font(50), "#d7fcd4", "White")

            QUIT_BUTTON = Button(self.SCREEN, (640, 550),
                                 "QUIT", self.get_font(50), "#d7fcd4", "White")
            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, MUL_BUTTON, QUIT_BUTTON]:
                button.changeState(MENU_MOUSE_POS)
                button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        game = GameController(MainMenu)

                    # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #     options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
