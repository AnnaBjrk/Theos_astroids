import pygame
from constants import *
from player import Player
from asteroids import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot
endles = True
def main():
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    
    
    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatables, drawables)
    Asteroid.containers = (asteroids, updatables, drawables)
    AsteroidField.containers = (updatables)
    Shot.containers = (shots, updatables, drawables)
    
    asteroidfield = AsteroidField()
    
    player = Player(x, y)
    print('Starting Asteroids!')
    print(f'Screen width: {SCREEN_WIDTH}')
    print(f'Screen height: {SCREEN_HEIGHT}')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fps = pygame.time.Clock()
    
    dt = 0
    
    while endles == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
        
        updatables.update(dt)
        black = (0, 0, 0)
        screen.fill(black)
        
        for obj in asteroids:
            if obj.collide_with(player) == True:
                print("Game Over!")
                sys.exit()

        for obj in drawables:
            obj.draw(screen)

        for obj in asteroids:
            for bullet in shots:
                if bullet.collide_with(obj):
                    obj.split()
                    bullet.kill()
        pygame.display.flip()
        dt = fps.tick(60) / 1000

if __name__ == "__main__":
    main()