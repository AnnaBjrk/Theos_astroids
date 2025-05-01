import pygame
from constants import *
from circleshape import CircleShape
import random

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle( screen, (255,255,255),self.position, self.radius, 2)

    def update(self,dt):
        self.position += self.velocity * dt

    def split(self):
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
        else:
            self.kill()
            neg_Ran_angle = random.uniform(-50, -20)
            Ran_angle = random.uniform(20, 50)
            
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            split1 = Asteroid(self.position.x, self.position.y, new_radius)
            split2 = Asteroid(self.position.x, self.position.y, new_radius)
            split1.velocity = pygame.Vector2(self.velocity)
            split2.velocity = pygame.Vector2(self.velocity)
            
            split1.velocity.rotate_ip(Ran_angle)
            split2.velocity.rotate_ip(neg_Ran_angle)
            split1.velocity *= 1.2
            split1.velocity *= 1.2
            for group in Asteroid.containers:
                group.add(split1)
                group.add(split2)
            #return (split1, split2)
            