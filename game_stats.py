#!/usr/bin/env python3
# 游戏状态

class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()

        self.game_active = False

        # 最高纪录
        self.high_score = 0
        # 游戏积分
        self.score = 0
        # 游戏等级
        self.level = 1

    def reset_stats(self):
        self.ship_left = self.ai_settings.ship_limit

