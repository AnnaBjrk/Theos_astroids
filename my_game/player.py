import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)#
        self.rotation = 0
        self.timer = 0
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    
    
    

    def draw(self, screen):
        pygame.draw.polygon(screen,(255, 255, 255), self.triangle(), 2)


    def update(self, dt):
        neg_dt = 0 - dt
        keys = pygame.key.get_pressed()
        
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_pos) - self.position
        self.rotation = direction.as_polar()[1] + 90 * 3
        
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(neg_dt)
        if self.timer == 0:
            if keys[pygame.K_SPACE]:
                self.shoot()
        else:
            self.timer -= dt
            if self.timer < 0:
                self.timer = 0
        
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        self.timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED 
        