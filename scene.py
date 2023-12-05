import pygame as pg
import random
width, height = 1920, 1080

class Star(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.len = random.randint(1, 10)
        self.image = pg.Surface((self.len, self.len))
        pg.draw.circle(self.image, (200, 200, 200), (self.len // 2, self.len // 2), self.len // 2)
        self.rect = self.image.get_rect()
        self.x = self.rect.x = random.randrange(width)
        self.y = self.rect.y = random.randrange(height)

    def update(self, game_speed):
        self.x -= 0.2 * (0.8 + game_speed/5 ) * (self.len // 2)
        self.y += 0.05
        self.rect.x = self.x % width
        self.rect.y = self.y % height

class Border(pg.sprite.Sprite):
    def __init__(self, x1, x2, y1, y2):
        pg.sprite.Sprite.__init__(self)
        # горизонтальная стенка
        self.image = pg.Surface((x2 - x1, 1))
        self.rect = pg.Rect(x1, y1, x2 - x1, 1)
