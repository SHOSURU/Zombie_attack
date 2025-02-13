import pygame
from pygame import mixer
from assets import spritesheet as ss


pygame.init()
mixer.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player_spritesheets = [
    pygame.image.load(f'assets/sprite/player/player_{i}.png').convert_alpha()
    for i in range(4)
]
player_spritesheet = [ss.SpriteSheet(player_spritesheets[i]) for i in range(4)]


enemy_spritesheets = [
    [
        pygame.image.load(
            f'assets/sprite/enemies/zombie_{i}/zombie_{j}.png'
        ).convert_alpha()
        for j in range(5)
    ]
    for i in range(4)
]
enemy_spritesheet = [
    [ss.SpriteSheet(enemy_spritesheets[i][j]) for j in range(5)]
    for i in range(4)
]

BG = (50, 50, 50) 
BLACK = (0, 0, 0)

GROUND_LEVEL = SCREEN_HEIGHT-150


player_walk_sound = mixer.Sound('assets/sound/player_walk.mp3')
player_attack_sound = mixer.Sound('assets/sound/player_atack.mp3')
zombie_bite_sound = mixer.Sound('assets/sound/zombie_bite.mp3')
zombie_death_sound = mixer.Sound('assets/sound/zombie_death.mp3')


zombie_walk_sounds = []
for i in range(2): 
    sound = mixer.Sound(f'assets/sound/zombie_walk_{i}.mp3')
    zombie_walk_sounds.append(sound)


frame_counts = [player_spritesheets[i].get_width() // 128 for i in range(4)]
frames = [[player_spritesheet[i].get_image(j, 128, 128, 1, BLACK)for j in range(frame_counts[i])]for i in range(4)]


enemy_frames = [
    [
        [
            enemy_spritesheet[i][j].get_image(k, 128, 128, 1, BLACK)
            for k in range(
                enemy_spritesheets[i][j].get_width() // 128
            )
        ]
        for j in range(5)
    ]
    for i in range(4)
]


animation_speed = 10 
