#!/usr/bin/env python3
# 设置类

class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3

        # 子单设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_num = 5000

        # 外星人移动速度
        self.fleet_drop_speed = 30


        # 外星人等级加速
        self.speedup_scale = 1.5
        # 得分等级
        self.score_scale = 1.5

        # 初始化游戏节奏
        self.initialize_dynamic_settings()

    # 初始化游戏节奏
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 3
        self.fleet_direction = 1 # 1：向右， -1：向左
        self.alien_points = 10

    def increse_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
