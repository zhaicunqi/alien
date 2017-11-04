#!/usr/bin/env python3
# 子单类

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        # 在飞船所处的位置创建一个子单对象
        super(Bullet, self).__init__()
        self.screen = screen

        # 在（0，0）处创建一个表示子单的矩形，在设置正确的位置
        self.image = pygame.image.load("images/bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示的子单位置
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        # 在制定位置绘制飞船
        self.screen.blit(self.image, self.rect)




