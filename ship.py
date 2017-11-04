#!/usr/bin/env python3
# 飞船类
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, screen, ai_settings):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并取其外接矩形
        self.image = pygame.image.load("images/life.png")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 允许不断移动
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        # 在制定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.ai_settings.ship_speed_factor

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
