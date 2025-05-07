import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        
    def collide_with(self, other):
        pos1 = self.position
        pos2 = other.position
        
        distance = pos1.distance_to(pos2)
        if distance <= self.radius + other.radius:
            return True
        else:
            return False
        
        #from pygame.math import Vector2

#Inside your check_collision method:
    #pos1 = Vector2(self.x, self.y)
    #pos2 = Vector2(other_circle.x, other_circle.y)
    #distance = pos1.distance_to(pos2)
        
    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):

        # sub-classes must override
        pass