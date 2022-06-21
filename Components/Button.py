import pygame
from typing import Tuple


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Button:
    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], text: str,  font: pygame.font.Font, baseColor: Tuple[int, int, int], hoverColor: Tuple[int, int, int], ):
        self.x = pos[0]
        self.y = pos[1]
        # self.width = w
        # self.height = h
        self.baseColor = baseColor
        self.hoverColor = hoverColor
        self.rawText = text
        self.font = font
        self.text = self.font.render(self.rawText, True, self.baseColor)
        self.screen = screen
        # self.font = pygame.font.Font("assets/font.ttf", 75)
        self.font = font
        self.textRect = self.text.get_rect(center=(self.x, self.y))

    def draw(self):
        self.screen.blit(self.text, self.textRect)

    def checkForInput(self, position):
        if position[0] in range(self.textRect.left, self.textRect.right) and position[1] in range(self.textRect.top, self.textRect.bottom):
            return True
        return False

    def changeState(self, position):
        if position[0] in range(self.textRect.left, self.textRect.right) and position[1] in range(self.textRect.top, self.textRect.bottom):
            self.text = self.font.render(
                self.rawText, True, self.hoverColor)
        else:
            self.text = self.font.render(
                self.rawText, True, self.baseColor)
