import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
                      bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
                      bullets,mouse_x,mouse_y):
    """在玩家电机play按钮时开始游侠"""
    button_checked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_checked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人并让飞船居中
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """更新屏幕上的图像并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #显示得分
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_high_score(stats,sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        # 删除现有子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        creat_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return  number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    available_speace_y = (ai_settings.screen_height -
                          (3 * alien_height) - ship_height)
    number_rows = int(available_speace_y / (2*alien_height))
    return number_rows

def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def creat_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有外星人到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            break

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)

    # 检查是否有外星人到达屏幕底部
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)


