#! /usr/bin/env python3

import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # 游戏标题
    pygame.display.set_caption("Ailen Invasion")

    # 飞船
    ship = Ship(screen, ai_settings)
    # 子单
    bullets = Group()
    # 外星人
    aliens = Group()
    # 创建外星人
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 游戏状态
    stats = GameStats(ai_settings)
    # 开始按钮
    play_button = Button(ai_settings, screen, 'Play')
    # 创建得分牌
    sb = Scoreboard(ai_settings, screen, stats)

    while True:
        # 监听键盘和鼠标事件
        gf.check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens, sb)
        # 判断游戏状态
        if stats.game_active:
            # 更新飞船
            ship.update()
            # 更新外星人
            gf.update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb)
            # 更新子单
            gf.update_bullet(bullets, aliens, ai_settings, screen, ship, stats, sb)
        # 更新屏幕
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb)


run_game()
