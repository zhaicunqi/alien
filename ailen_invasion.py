#! /usr/bin/env python3

import sys
import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

# 背景颜色
bg_color = (230, 230, 230)


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Ailen Invasion")

    ship = Ship(screen,ai_settings)

    bullets = Group()

    # 创建一个外星人
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    stats = GameStats(ai_settings)

    play_button = Button(ai_settings, screen, 'Play')

    # 创建得分牌
    sb = Scoreboard(ai_settings, screen, stats)

    while True:
        # 监听键盘和鼠标事件
        gf.check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens, sb)
        if stats.game_active:
            ship.update()
            gf.update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb)
            gf.update_bullet(bullets, aliens, ai_settings, screen, ship, stats, sb)
        # 更新屏幕
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb)


run_game()
