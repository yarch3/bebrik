import pygame as pg
import random
import addOns
pg.init()
screenSize = width, height = (1920, 1080)
screen = pg.display.set_mode(screenSize)
ARIAL_50 = pg.font.SysFont('arial', 100)

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callback = []
        self.current_option_index = 0
        self.results = []

    def append_option(self, option, callback):
        self._option_surfaces.append(ARIAL_50.render(option, True, (255, 255, 255)))
        self._callback.append(callback)

    def clear(self):
        self._option_surfaces = []
        self._callback = []
        self._current_option_index = 0

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        self._callback[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y +i * option_y_padding)
            if i == self._current_option_index:
                pg.draw.rect(surf, (35, 35, 35), option_rect)
            surf.blit(option, option_rect)

