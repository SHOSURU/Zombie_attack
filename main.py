import pygame
from pygame import mixer
from assets import spritesheet as ss
import random
import sys
import vars
from player import Player   
from enemy import Enemy  

pygame.init()
mixer.init()

screen = pygame.display.set_mode((vars.SCREEN_WIDTH, vars.SCREEN_HEIGHT))
pygame.display.set_caption('Zombie Game')
clock = pygame.time.Clock()

def draw_text(screen, text, font, color, center):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)

def start_screen():
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    title = "Выберите уровень сложности"
    options = ["1. Легкий", "2. Средний", "3. Тяжелый"]

    screen.fill(vars.BG)
    draw_text(screen, title, font, (255, 255, 255), (vars.SCREEN_WIDTH / 2, vars.SCREEN_HEIGHT / 2 - 100))
    draw_text(screen, options[0], small_font, (255, 255, 255), (vars.SCREEN_WIDTH / 2, vars.SCREEN_HEIGHT / 2 - 30))
    draw_text(screen, options[1], small_font, (255, 255, 255), (vars.SCREEN_WIDTH / 2, vars.SCREEN_HEIGHT / 2 + 10))
    draw_text(screen, options[2], small_font, (255, 255, 255), (vars.SCREEN_WIDTH / 2, vars.SCREEN_HEIGHT / 2 + 50))

    pygame.display.flip()

    waiting = True
    difficulty = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "easy"
                    waiting = False
                elif event.key == pygame.K_2:
                    difficulty = "medium"
                    waiting = False
                elif event.key == pygame.K_3:
                    difficulty = "hard"
                    waiting = False

    return difficulty

def game_over_screen(screen, player):
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render('GAME OVER', True, (255, 0, 0))
    text_rect = game_over_text.get_rect(
        center=(vars.SCREEN_WIDTH / 2, vars.SCREEN_HEIGHT / 2 - 50)
    )

    retry_text = pygame.font.SysFont(None, 36).render(
        'Нажмите R для рестарта или Q для выхода',
        True,
        (255, 255, 255),
    )
    retry_rect = retry_text.get_rect(
        center=(vars.SCREEN_WIDTH / 2, vars.SCREEN_HEIGHT / 2 + 20)
    )

    screen.blit(game_over_text, text_rect)
    screen.blit(retry_text, retry_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main()  
                elif event.key == pygame.K_q:
                    waiting = False
                    pygame.quit()
                    sys.exit()

def main():
    global screen, clock
    enemy_mult=[]
    difficulty = start_screen()
    if difficulty == "easy":
        enemy_count = 2
        enemy_mult = [1,1,1,1]
    elif difficulty == "medium":
        enemy_count = 4
        enemy_mult = [1.5,2,1.5,0.5]
    elif difficulty == "hard":
        enemy_count = 6
        enemy_mult = [2,2,2,0.5]
   
    player = Player()
    enemies = [Enemy(random.randint(0, 3),enemy_mult) for _ in range(enemy_count)]

    run = True
    while run:
        screen.fill(vars.BG)
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update(enemies)
        player.draw(screen)
        player.draw_inv(screen)
        
        

        if player.alive:
            enemies = [enemy for enemy in enemies if enemy.update(player)]
            for enemy in enemies:
                enemy.draw(screen)
            
            while len(enemies) < enemy_count:
                enemies.append(Enemy(random.randint(0, 3),enemy_mult))
        else:
            game_over_screen(screen, player)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(vars.animation_speed)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
