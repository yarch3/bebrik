import pygame as pg
from random import randrange, choice, uniform, random
import math
import configparser

HEART = pg.image.load('heart.png')


class Hearts(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = hearts_image(3)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, health):
        self.image = hearts_image(health)

def hearts_image(val):
    new_image = pg.Surface((val * 70, 70))
    pic = pg.transform.scale(HEART, (70, 70))
    for i in range(val):
        new_image.blit(pic, ( 70 * i, 0))
    return new_image

def spawn_gap(game_speed):
    res = 3800 - (game_speed * 400)
    return res if res >= 1400 else 1400

def printScore(score, endgame = False):
    font = pg.font.SysFont('arial', 50, bold = True)
    surface = font.render(str(score), True, (255, 255, 255))
    return surface

def findVector(start_x, start_y):
    dest_x = 0
    dest_y = randrange(0, 1080)
    length = math.sqrt((dest_x - start_x)**2 + (dest_y - start_y)**2)
    vector = ((dest_x - start_x) * 6 / length, (dest_y - start_y) * 6 / length)
    return vector

def death_animation(screen, x, y):
    sprite_sheet = pg.image.load('explosion.png').convert_alpha()

    frames = []
    frame_width = sprite_sheet.get_width()//6
    frame_height = sprite_sheet.get_height()//4
    for j in range(0, sprite_sheet.get_height()//2, frame_height):
        for i in range(0, sprite_sheet.get_width(), frame_width):
            frame_rect = pg.Rect(i, j, frame_width, frame_height)
            frames.append(sprite_sheet.subsurface(frame_rect))

    current_frame = 0
    animation_timer = 0
    last_frame_ticks = pg.time.get_ticks()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        animation_timer += pg.time.get_ticks() - last_frame_ticks
        last_frame_ticks = pg.time.get_ticks()

        if animation_timer >= 10:
            current_frame += 1
            animation_timer = 0

        if current_frame >= len(frames):
            return  # Завершаем функцию, если закончили анимацию

        screen.blit(frames[current_frame], (x, y))
        pg.display.flip()
def read_numbers():
    numbers = []
    with open("results.txt", "r") as file:
        for line in file:
            numbers.append(int(line.strip()))
    return numbers[0:11]

# Сортировка списка чисел
def sort_add_numbers(numbers, num):
    if not num == -1:
        numbers.append(num)
    sorted_numbers = sorted(numbers, reverse= True)
    return sorted_numbers

# Запись отсортированных чисел в файл
def write_numbers(numbers):
    with open("results.txt", "w") as file:
        for number in numbers:
            file.write(str(number) + "\n")