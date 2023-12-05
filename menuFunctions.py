import pygame as pg

from pygame import Surface, SurfaceType
from random import randrange, choice, uniform, random

import addOns
from addOns import spawn_gap, printScore

import scene
import gameObjects
import menu



pg.init()
pg.mixer.init()
#scene initializing
screenSize = width, height = (1920, 1080)
screen = pg.display.set_mode(screenSize)

stars_group = pg.sprite.Group()

for _ in range(70):
    scene.Star(stars_group)

myfont = pg.font.Font('fonts/Kanit-Black.ttf', 200)
myfont1 = pg.font.Font('fonts/Kanit-Black.ttf', 75)
myfont1_5 = pg.font.Font('fonts/Kanit-Black.ttf', 125)
myfont2 = pg.font.Font('fonts/Kanit-Black.ttf', 50)
ARIAL_50 = pg.font.SysFont('arial', 50)
ARIAL_75 = pg.font.SysFont('arial', 75)
ARIAL_125 = pg.font.SysFont('arial', 125)

text_surface = myfont.render('ASTRO FLIGHT', True, 'White')



def game_cycle():
    game_speed = 1
    current_time = pg.time.get_ticks()
    clock = 0
    pg.init()
    # scene initializing
    screenSize = width, height = (1920, 1080)
    screen: Surface | SurfaceType = pg.display.set_mode(screenSize)
    hborder = scene.Border(0, width, 0, 0)
    lborder = scene.Border(0, width, height, height)
    topBorder = pg.sprite.Group(hborder)
    botBorder = pg.sprite.Group(lborder)
    last_enemy_spawn_time = pg.time.get_ticks()

    stars_group = pg.sprite.Group()
    player_group = pg.sprite.Group()
    enemy_group = pg.sprite.Group()
    bullet_group = pg.sprite.Group()
    obstacle_group = pg.sprite.Group()
    all_sprites = pg.sprite.Group()

    player = gameObjects.Player(50, height // 2, player_group)
    hpprint = addOns.Hearts(10, 10)
    hearts = pg.sprite.Group(hpprint)

    for _ in range(70):
        scene.Star(stars_group)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                bullet = gameObjects.Bullet(player.rect.x + player.rect.width, player.rect.y + player.rect.height // 2, True, bullet_group)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause()
        keys = pg.key.get_pressed()
        player_group.update(keys, topBorder, botBorder, enemy_group, obstacle_group)
        screen.fill((0, 0, 0))
        stars_group.draw(screen)
        player_group.draw(screen)
        hearts.draw(screen)
        screen.blit(printScore(player.score), (width - 100, 10))
        clock += pg.time.get_ticks() - current_time
        current_time = pg.time.get_ticks()
        if current_time - last_enemy_spawn_time >= spawn_gap(game_speed):
            index = choice([0, 1, 2])
            if index == 2 or index == 1:
                enemy = gameObjects.EnemyShip(enemy_group)
                enemy_group.add(enemy)
                last_enemy_spawn_time = current_time
            if index == 0:
                enemy = gameObjects.Asteroid(obstacle_group, player)
                obstacle_group.add(enemy)
                last_enemy_spawn_time = current_time

        bullet_group.update(player, enemy_group, obstacle_group, screen, game_speed)
        bullet_group.draw(screen)

        enemy_group.draw(screen)
        obstacle_group.draw(screen)
        pg.display.flip()
        stars_group.update(game_speed)
        hearts.update(player.hp)
        enemy_group.update(bullet_group, current_time, game_speed)
        obstacle_group.update(bullet_group)

        game_speed = clock / 10000 + 1
        player.score = (clock // 2000) + (player.exp() // 5)
        all_sprites.add(player_group, enemy_group, obstacle_group, bullet_group)



white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
menu = menu.Menu()
def show_menu():
    show = True
    menu.clear()
    menu.append_option('START GAME', start_game)
    menu.append_option('CONTROLS', controls_menu)
    menu.append_option('BEST RESULTS', best_results_menu)
    menu.append_option('QUIT', quit)
    while show:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    menu.switch(-1)
                elif event.key == pg.K_DOWN:
                    menu.switch(1)
                elif event.key == pg.K_KP_ENTER:
                    menu.select()

        keys = pg.key.get_pressed()
        stars_group.update(1)
        pg.display.update()
        screen.fill((0, 0, 0))
        stars_group.draw(screen)
        screen.blit(text_surface, (280, 20))
        menu.draw(screen, 720, 300, 120)
        pg.display.flip()

def controls_menu():
    controls_menu = True
    menu.clear()
    menu.append_option('BACK', show_menu)
    text_controls = myfont1_5.render('CONTROLS', True, 'White')
    text_controls1 = myfont1.render('MOVING UP', True, 'White')
    text_controls11 = myfont1.render('W', True, 'White')
    text_controls2 = myfont1.render('MOVING DOWN', True, 'White')
    text_controls22 = myfont1.render('S', True, 'White')
    text_controls3 = myfont1.render('SHOT', True, 'White')
    text_controls33 = myfont1.render('SPACE', True, 'White')
    text_controls4 = myfont1.render('PAUSE', True, 'White')
    text_controls44 = myfont1.render('ESCAPE', True, 'White')

    while controls_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_ENTER:
                    menu.select()
        keys = pg.key.get_pressed()
        stars_group.update(1)
        pg.display.update()
        screen.fill((0, 0, 0))
        stars_group.draw(screen)
        screen.blit(text_controls, (620, 250))
        screen.blit(text_controls1, (320, 430))
        screen.blit(text_controls11, (1300, 430))
        screen.blit(text_controls2, (320, 530))
        screen.blit(text_controls22, (1300, 530))
        screen.blit(text_controls3, (320, 630))
        screen.blit(text_controls33, (1300, 630))
        screen.blit(text_controls4, (320, 730))
        screen.blit(text_controls44, (1300, 730))
        screen.blit(text_surface, (280, 20))
        menu.draw(screen, 1600, 900, 120)
        pg.display.flip()

def best_results_menu():
    best_results_menu = True
    menu.results = addOns.read_numbers()
    text_best_results = myfont1_5.render('BEST RESULTS', True, 'White')
    menu.results = addOns.read_numbers()
    menu.results = addOns.sort_add_numbers(menu.results, -1)
    addOns.write_numbers(menu.results)
    strings = []
    length = 10 if len(menu.results) >= 10 else len(menu.results)
    for i in range(length):
        strings.append(myfont2.render(str(i+1) +'.  ' + str(menu.results[i]), True, 'White'))
    menu.clear()
    menu.append_option('BACK', show_menu)
    while best_results_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_ENTER:
                    menu.select()
        keys = pg.key.get_pressed()
        stars_group.update(1)
        pg.display.update()
        screen.fill((0, 0, 0))
        stars_group.draw(screen)
        screen.blit(text_best_results, (550, 250))
        for i in range(length):
            screen.blit(strings[i], (580, 400 + 50 * i))

        screen.blit(text_surface, (280, 20))
        menu.draw(screen, 1600, 900, 120)
        pg.display.flip()




def pause():
    pause = True
    pg.mixer.music.pause()
    menu.clear()
    menu.append_option('CONTINUE', continue_game)
    menu.append_option('START NEW GAME', start_game)
    # menu.append_option('CONTROLS', controls_pause)
    # menu.append_option('BEST RESULTS', best_results_pause)
    menu.append_option('QUIT', quit)
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    menu.switch(-1)
                elif event.key == pg.K_DOWN:
                    menu.switch(1)
                elif event.key == pg.K_KP_ENTER:
                    if menu._current_option_index == 0:
                        pg.mixer.music.unpause()
                        return
                    menu.select()

        keys = pg.key.get_pressed()
        stars_group.update(1)
        pg.display.update()
        screen.fill((0, 0, 0))
        stars_group.draw(screen)
        screen.blit(text_surface, (280, 20))
        menu.draw(screen, 720, 300, 120)
        pg.display.flip()


def controls_pause():
    controls_pause = True
    menu.clear()
    menu.append_option('BACK', pause)
    text_controls = myfont1_5.render('CONTROLS', True, 'White')
    text_controls1 = myfont1.render('MOVING UP', True, 'White')
    text_controls11 = myfont1.render('W', True, 'White')
    text_controls2 = myfont1.render('MOVING DOWN', True, 'White')
    text_controls22 = myfont1.render('S', True, 'White')
    text_controls3 = myfont1.render('SHOT', True, 'White')
    text_controls33 = myfont1.render('SPACE', True, 'White')
    text_controls4 = myfont1.render('PAUSE', True, 'White')
    text_controls44 = myfont1.render('ESCAPE', True, 'White')

    while controls_pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_ENTER:
                    menu.clear()
                    return
                    menu.select()
        stars_group.update(1)
        pg.display.update()
        screen.fill((0, 0, 0))
        stars_group.draw(screen)
        screen.blit(text_controls, (620, 250))
        screen.blit(text_controls1, (320, 430))
        screen.blit(text_controls11, (1300, 430))
        screen.blit(text_controls2, (320, 530))
        screen.blit(text_controls22, (1300, 530))
        screen.blit(text_controls3, (320, 630))
        screen.blit(text_controls33, (1300, 630))
        screen.blit(text_controls4, (320, 730))
        screen.blit(text_controls44, (1300, 730))
        screen.blit(text_surface, (280, 20))
        menu.draw(screen, 1600, 900, 120)
        pg.display.flip()


def best_results_pause():
    best_results_pause = True
    text_best_results = myfont1_5.render('BEST RESULTS', True, 'White')
    menu.results = addOns.read_numbers()
    menu.results = addOns.sort_add_numbers(menu.results, -1)
    addOns.write_numbers(menu.results)
    strings = []
    length = 10 if len(menu.results) >= 10 else len(menu.results)
    for i in range(length):
        strings.append(myfont2.render(str(i+1) +'.  ' + str(menu.results[i]), True, 'White'))
    menu.clear()
    menu.append_option('BACK', pause)
    while best_results_pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_ENTER:
                    return
                    menu.select()
        stars_group.update(1)
        pg.display.update()
        screen.fill((0, 0, 0))
        stars_group.draw(screen)
        screen.blit(text_best_results, (550, 250))
        for i in range(length):
            screen.blit(strings[i], (580, 400 + 50 * i))

        screen.blit(text_surface, (280, 20))
        menu.draw(screen, 1600, 900, 120)
        pg.display.flip()
def start_game():
    pg.mixer.music.load("track.mp3")
    pg.mixer.music.play()
    game_cycle()
def continue_game():
    menu.clear()
    return
def game_over(result):
    menu.results = addOns.read_numbers()
    menu.results = addOns.sort_add_numbers(menu.results, result)
    addOns.write_numbers(menu.results)
    show = True
    menu.clear()
    menu.append_option('PLAY AGAIN', start_game)
    menu.append_option('MENU', show_menu)
    menu.append_option('QUIT', quit)
    text_game_over = (myfont.render('GAME OVER', True, 'White'))
    while show:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    menu.switch(-1)
                elif event.key == pg.K_DOWN:
                    menu.switch(1)
                elif event.key == pg.K_KP_ENTER:
                    menu.select()

        stars_group.update(1)
        pg.display.update()
        screen.fill((0, 0, 0))
        stars_group.draw(screen)
        screen.blit(text_game_over, (380, 180))
        menu.draw(screen, 700, 500, 120)
        pg.display.flip()


show_menu()


