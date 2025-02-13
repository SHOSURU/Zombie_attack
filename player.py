import pygame
import random
from pygame import mixer
from assets import spritesheet as ss
import vars

pygame.init()
mixer.init()

class HealthKit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        pygame.draw.line(self.image, (255, 0, 0), (8, 2), (8, 18), 4)
        pygame.draw.line(self.image, (255, 0, 0), (2, 10), (18, 10), 4)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 100
        self.heal_amount = 1

    def apply_healing(self, player):
        if hasattr(player, 'health'):
            player.health = min(player.health + self.heal_amount, player.max_health)
            self.kill()

    @staticmethod
    def should_drop(player):
        missing_hp = player.max_health - player.health
        drop_chance = (missing_hp / player.max_health)
        return random.random() < drop_chance

class Player:
    def __init__(self):
        self.x = 200
        self.y = vars.GROUND_LEVEL
        self.width = vars.frames[0][0].get_width()
        self.height = vars.frames[0][0].get_height()
        self.state = 0  
        self.frame_index = 0
        self.image = vars.frames[self.state][self.frame_index]
        self.velocity = 5  
        self.facing_left = False  
        self.defending = False
        self.attacking = False
        self.attack_speed = 30  
        self.attack_timer = 0  
        self.health = 10
        self.max_health = 10
        self.taking_damage = False
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 30
        self.kill_count = 0  
        self.alive = True  
        self.walk_sound_playing = False  
        self.health_kits = pygame.sprite.Group()

    def animate(self, enemies):
        self.frame_index += 1
        if self.state != 3:
            if self.frame_index >= len(vars.frames[self.state]):
                self.frame_index = 0
                if self.state == 2:
                    vars.player_attack_sound.play()  
                    for enemy in enemies:
                        if not enemy.taking_damage and abs(self.x - enemy.x) < 50:
                            enemy.taking_damage = True
                            enemy.state = 3  
                            enemy.frame_index = 0
                            enemy.health -= 1
                            vars.zombie_bite_sound.play()
                            if enemy.health <= 0:
                                enemy.state = 4  
                                enemy.frame_index = 0
                                vars.zombie_death_sound.play()  
                                self.increment_kill_count()
                                if HealthKit.should_drop(self):
                                    health_kit = HealthKit(enemy.x - 20, vars.GROUND_LEVEL)
                                    self.health_kits.add(health_kit)
                    self.attacking = False
                    if self.state != 1:
                        self.state = 0
        else:
            if self.frame_index >= len(vars.frames[self.state]):
                self.frame_index = len(vars.frames[self.state]) - 1

        self.image = vars.frames[self.state][self.frame_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False).convert_alpha()
        else:
            self.image = self.image.convert_alpha()

    def update(self, enemies):
        if not self.alive:
            return  
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
        if self.attacking:
            self.state = 2
            self.attack_timer -= 1  
            if self.attack_timer <= 0:  
                self.attacking = False  
        elif self.defending:
            self.state = 3
        self.animate(enemies)
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for health_kit in self.health_kits:
            if health_kit.rect.colliderect(player_rect):
                health_kit.apply_healing(self)

    def move(self, keys):
        if not self.alive:
            return  
        moving = False  
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.defending = True
            if self.walk_sound_playing:
                vars.player_walk_sound.stop()
                self.walk_sound_playing = False
            if keys[pygame.K_a]:
                self.facing_left = True
                moving = True
            elif keys[pygame.K_d]:
                self.facing_left = False
                moving = True
        elif keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_timer = self.attack_speed  
            self.frame_index = 0
            if self.walk_sound_playing:
                vars.player_walk_sound.stop()
                self.walk_sound_playing = False
            if keys[pygame.K_a]:
                self.facing_left = True
            elif keys[pygame.K_d]:
                self.facing_left = False
        elif not keys[pygame.K_SPACE]:
            self.attacking = False  
            self.defending = False
            if keys[pygame.K_a]:
                self.x -= self.velocity
                self.state = 1  
                self.facing_left = True
                moving = True
            elif keys[pygame.K_d]:
                self.x += self.velocity
                self.state = 1  
                self.facing_left = False
                moving = True
            else:
                self.state = 0  
                if self.walk_sound_playing:
                    vars.player_walk_sound.stop()
                    self.walk_sound_playing = False
        if moving and not self.defending:
            if not self.walk_sound_playing:
                vars.player_walk_sound.play(-1)  
                self.walk_sound_playing = True
        else:
            if self.walk_sound_playing:
                vars.player_walk_sound.stop()
                self.walk_sound_playing = False

    def take_damage(self):
        if not self.defending and not self.invulnerable:
            self.health -= 1
            self.taking_damage = True
            self.invulnerable = True
            self.invulnerable_timer = self.invulnerable_duration  
            if self.health <= 0:
                self.alive = False  
                

    def increment_kill_count(self):
        self.kill_count += 1

    def draw_inv(self, screen):
        if self.invulnerable and (self.invulnerable_timer % 10 < 4):
            return  
        screen.blit(self.image, (self.x, self.y))
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (20, 20, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0), (20, 20, 100 * (self.health / self.max_health), 10))
        font = pygame.font.SysFont(None, 24)
        kill_text = font.render(f'Kills: {self.kill_count}', True, (255, 255, 255))
        screen.blit(kill_text, (20, 40))
        self.health_kits.draw(screen)
