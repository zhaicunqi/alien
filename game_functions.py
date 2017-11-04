#!/usr/bin/env python3
# 公共方法
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens, sb):
    # 监听键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_event_keydown(event, ship, ai_settings, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_event_keyup(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets,ai_settings, screen, ship, sb)

def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets,ai_settings, screen, ship, sb):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 设置游戏状态
        stats.game_active = True
        # 重置
        stats.reset_stats()
        aliens.empty()
        bullets.empty()

        # 重置得分信息
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #创建一群新的外星人，并将飞船放到屏幕底部中间位置
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 初始化游戏等级
        ai_settings.initialize_dynamic_settings()

# 监听键盘按下事件
def check_event_keydown(event, ship, ai_settings, screen, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_settings.bullet_num:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)


# 监听键盘抬起事件
def check_event_keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb):
    # 填充北京颜色
    screen.fill(ai_settings.bg_color)
    # 绘制子单
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 绘制飞船
    ship.blitme()
    # 绘制外星人
    aliens.draw(screen)
    # 绘制分数
    sb.show_score()
    # 开始按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullet(bullets, aliens, ai_settings, screen, ship, stats, sb):
    bullets.update()
    # 清除已消失的子单
    for bullet in bullets:
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    # 判断是否集中外星人
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb)

# 判断是否集中外星人
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):
    # 检查是否相撞
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for collision in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    # 重新绘制外星人
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ai_settings.increse_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()

# 创建外星人群
def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    # number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    number_rows = 3;
    # 遍历单个创建外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien, alien_number, row_number)

# 一行可容纳的外星人数量
def get_number_aliens_x(ai_settings, alien_width):
    avaliable_space_x = ai_settings.screen_width - 1 * alien_width
    number_aliens_x = int(avaliable_space_x / (     2 * alien_width))
    return number_aliens_x

# 创建外形人
def create_alien(ai_settings, screen, aliens, alien, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.6 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

# 外星人行数
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

# 更新外星人
def update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测外星人与飞船相撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

# 集中飞船
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    # 响应被外星人撞到的飞船
    if stats.ship_left > 0:
        stats.ship_left -= 1
        sb.prep_ships()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    #清空外星人列表和子单列表
    aliens.empty()
    bullets.empty()
    #创建一群新的外星人，并将飞船放到屏幕底部中间位置
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

# 外星人移动
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

# 移动方向
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

# 外星人到达底部
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

# 检验最高分
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()







