import pygame
from Store import Store


class GameObject(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        pygame.display.flip()
