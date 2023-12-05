from random import randrange, choice, uniform, random
import pygame as pg

import addOns
from addOns import findVector
import menuFunctions
screenSize = width, height = (1920, 1080)
all_sprites = pg.sprite.Group()

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, isHandledbyPlayer, bullets):
        radius = 5
        super().__init__(bullets)
        self.damage = 1
        self.isPlayers = isHandledbyPlayer
        self.image = pg.Surface((10, 10),
                                    pg.SRCALPHA, 32)
        self.rect = pg.Rect(x, y, 2 * radius, 2 * radius)
        color = pg.Color("cyan") if isHandledbyPlayer else pg.Color("red")
        pg.draw.circle(self.image, color,
                           (radius, radius), radius)

    def update(self, player, enemies, asteroids, screen, game_speed):
        if self.isPlayers:
            self.rect = self.rect.move(6 * (0.8 + game_speed/5), 0)
            collided_enemies = pg.sprite.spritecollide(self, enemies, True)
            for enemy in collided_enemies:
                player.gainXP()
                x = self.rect.x
                y = self.rect.y
                self.kill()
             #   addOns.death_animation(screen, x, y)

        else:
            self.rect = self.rect.move(-6 * (0.8 + game_speed/5), 0)
            if pg.sprite.collide_rect(self, player):
                player.hp -= 1
                self.kill()
                del self

class EnemyShip(pg.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        image = pg.image.load('enemy.png')
        self.image = pg.transform.scale(image, (120, 100))
        self.image = pg.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = 2000.
        self.rect.y = randrange(0, height - self.rect.height)
        self.hp = 1
        self.last_time_shot = 0

    def update(self, bulletgr, time, game_speed):
        self.rect.x -= 0.501 * (0.8 + game_speed/5 )
        if time - self.last_time_shot > randrange(100, 200) + 700:
            Bullet(self.rect.x, self.rect.y + self.rect.height // 2, False, bulletgr)
            self.last_time_shot = time

class Asteroid(pg.sprite.Sprite):
    def __init__(self, group, player):
        super().__init__(group)
        image = pg.image.load('asteroid.png')
        self.image = pg.transform.scale(image, (200, 200))
        self.image = pg.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.x = 2000.
        self.rect.y = randrange(0, 950)
        vec = ((), ())
        self.dx, self.dy = findVector(self.rect.x, self.rect.y)
        self.hp = 100
    def update(self, bullet_group):
        self.rect = self.rect.move(self.dx, self.dy)
        bullets = pg.sprite.spritecollide(self, bullet_group, True)
        for bullet in bullets:
            del bullet


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        image = pg.image.load('player.png')
        self.image = pg.transform.scale(image, (100, 150))
        self.image = pg.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 3
        self.experience = 0
        self.score = 0
        #self.level = self. experience % 5
    def gainXP(self):
        self.experience += 10
    def exp(self):
        return self.experience


    def update(self, keys, hborder, lborder, enemies, obstacles):
        self.checkHealth()
        if keys[pg.K_w]:
            if not pg.sprite.spritecollideany(self, hborder):
                self.rect.y -= 5
        if keys[pg.K_s]:
            if not pg.sprite.spritecollideany(self, lborder):
                self.rect.y += 5
        for sprite in enemies:
            if pg.sprite.collide_rect(self, sprite):
                self.hp -= 1
                self.gainXP()
                sprite.hp -= 1
                if sprite.hp == 0:
                    sprite.kill()
                    del sprite
        for asteroid in obstacles:
            if pg.sprite.collide_rect(self,asteroid):
                self.hp = 0
        #self.checkHealth(screen)
    def moveUp(self):
        self.rect.y -= 1
    def moveDown(self):
        self.rect.y += 1
    def attack(self):
        Bullet(self.rect.x, self.rect.y + self.rect.height//2)
    def checkHealth(self):
        pts = self.score
        if self.hp == 0:
            self.kill()
            del self
            pg.mixer.music.stop()
            pg.mixer.music.load("poorYoda.mp3")
            pg.mixer.music.play()
            menuFunctions.game_over(pts)
            return False
        else:
            return True


