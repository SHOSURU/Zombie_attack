import pygame
from pygame import mixer
from assets import spritesheet as ss
import random
import vars

class Enemy:
    def __init__(self, enemy_type,enemy_mult):
        self.x = random.choice([-128, vars.SCREEN_WIDTH])
        self.y = vars.GROUND_LEVEL
        self.state = 1  
        self.frame_index = 0
        self.enemy_type = enemy_type
        self.image = vars.enemy_frames[self.enemy_type][self.state][self.frame_index]

        if self.enemy_type == 0:
            self.speed = 1*enemy_mult[0]
            self.health = 3*enemy_mult[1]
            self.attack_speed = 30*enemy_mult[2]
            self.attack_cooldown = 30*enemy_mult[3]  
        elif self.enemy_type == 1:
            self.speed = 3*enemy_mult[0]
            self.health = 1*enemy_mult[1]
            self.attack_speed = 15* enemy_mult[2]   
            self.attack_cooldown = 15  * enemy_mult[3]
        else:
            self.speed = 2*enemy_mult[0]
            self.health = 2*enemy_mult[1]
            self.attack_speed = 20*enemy_mult[2]
            self.attack_cooldown = 20  *    enemy_mult[3]

        self.velocity = self.speed if self.x < vars.SCREEN_WIDTH / 2 else -self.speed
        self.facing_left = self.velocity < 0
        self.dead = False
        self.taking_damage = False
        self.attacking = False
        self.current_attack_cooldown = 0
        self.walk_sound_playing = False  

    def animate(self, player):
        self.frame_index += 1
        total_frames = len(vars.enemy_frames[self.enemy_type][self.state])
        if self.frame_index >= total_frames:
            if self.state == 2:  
                if abs(self.x - player.x) <= self.attack_range and player.alive:  
                    player.take_damage()
                    vars.zombie_bite_sound.play()
                self.attacking = False
                self.state = 1
            elif self.state == 3:  
                self.taking_damage = False
                if self.health <= 0:
                    self.state = 4  
                    vars.zombie_death_sound.play()
                else:
                    knockback_distance = 30
                    if player.x < self.x:
                        self.x += knockback_distance  
                    else:
                        self.x -= knockback_distance  
                    self.state = 1  
            elif self.state == 4:  
                self.dead = True
            self.frame_index = 0

        self.image = vars.enemy_frames[self.enemy_type][self.state][self.frame_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False).convert_alpha()
        else:
            self.image = self.image.convert_alpha()

    def update(self, player):
        if self.dead:
            self.animate(player)
            return False

        if self.taking_damage or self.attacking:
            self.animate(player)
            return True

        distance_to_player = player.x - self.x
        self.attack_range = 30
        if abs(distance_to_player) > self.attack_range:
            self.velocity = self.speed if distance_to_player > 0 else -self.speed
            self.facing_left = self.velocity < 0
            self.x += self.velocity

            if not self.walk_sound_playing:
                random.choice(vars.zombie_walk_sounds).play()
                self.walk_sound_playing = True
        else:
            self.velocity = 0
            if self.walk_sound_playing:
                self.walk_sound_playing = False 

            if self.current_attack_cooldown == 0 and player.alive:
                self.attacking = True
                self.state = 2
                self.frame_index = 0
                self.current_attack_cooldown = self.attack_cooldown  

        self.animate(player)

        if self.current_attack_cooldown > 0:
            self.current_attack_cooldown -= 1

        return True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
