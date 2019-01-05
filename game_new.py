import os
from math import tan, radians, degrees, copysign, hypot, sqrt, sin, cos, pi

# import pygame with no welcome message
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame.math import Vector2
from random import randint, uniform, randrange

WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
BLACK =     (  0,   0,   0)

class obstacle:
    pos = [0, 0]
    velocity = None
    speed = 3
    bounds = None

    def __init__(self, pos, bounds):
        self.pos = pos
        self.rand_dir
        self.bounds = bounds

    def rand_dir(self):
        # Set random direction vector of magnitude speed
        self.velocity = Vector2(self.speed, 0).rotate(randrange(360))

    def move(self):
        # Check if about to hit frame, if so change velocity direction
        if self.pos[0]+self.velocity[0] <= 20 or self.pos[0]+self.velocity[0] >= 980:
            self.velocity = Vector2(self.velocity[0]*-1, self.velocity[1])
        if self.pos[1]+self.velocity[1] <= 20 or self.pos[1]+self.velocity[1] >= 580:
            self.velocity = Vector2(self.velocity[0], self.velocity[1]*-1)
        # Update position, turn to list
        self.pos += self.velocity
        self.pos = [int(self.pos[0]), int(self.pos[1])]

class player:
    pos = [0, 0]
    velocity = Vector2()
    speed = 5
    bounds = None

    def __init__(self, pos, bounds):
        self.pos = pos
        self.bounds = bounds
        self.velocity = Vector2(self.speed, 0).rotate(randrange(360))


    def left(self):
        # Set random direction vector of magnitude speed
        self.velocity = self.velocity.rotate(-30)

    def right(self):
        # Set random direction vector of magnitude speed
        self.velocity = self.velocity.rotate(30)

    def move(self):
        # Check if about to hit frame, if so change velocity direction
        if self.pos[0]+self.velocity[0] <= 20 or self.pos[0]+self.velocity[0] >= 980:
            print("Dead")
            self.velocity = Vector2(self.velocity[0]*-1, self.velocity[1])
        if self.pos[1]+self.velocity[1] <= 20 or self.pos[1]+self.velocity[1] >= 580:
            print("Dead")

            self.velocity = Vector2(self.velocity[0], self.velocity[1]*-1)
        # Update position, turn to list
        self.pos += self.velocity
        self.pos = [(self.pos[0]), (self.pos[1])]


class Game:
    epochs = 0
    def __init__(self, n_obstacles):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.ticks =20
        self.exit = False
        self.obstacles = []

        self.initialize(n_obstacles)

        self.player = player([500,300], self.screen)


    def initialize(self, n_obstacles):
        # Create obstacles, in random positions
        for n in range(n_obstacles):
            pos = (randint(20, 980), randint(20, 580))
            ob = obstacle(pos, self.screen)
            ob.rand_dir()
            self.obstacles.append(ob)


    def run(self):
        self.clock.tick(self.ticks)

        while not self.exit:
            # Check if quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # move obstacles
            for o in self.obstacles:
                o.move()
            # move player
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT]:
                self.player.right()
            if pressed[pygame.K_LEFT]:
                self.player.left()
            self.player.move()

            # Draw
            self.screen.fill(BLACK)
            for o in self.obstacles:
                pygame.draw.circle(self.screen, RED, o.pos, 20)
            player_pos = [int(self.player.pos[0]), int(self.player.pos[1])]
            player_vel = [(self.player.velocity[0]), (self.player.velocity[1])]
            pygame.draw.circle(self.screen, BLUE, player_pos, 20)
            pygame.draw.arc(self.screen, WHITE, (player_pos[0], player_pos[1], 20, 20), player_vel[0], player_vel[1], 2)

            pygame.display.update()
            self.clock.tick(self.ticks)






if __name__ == '__main__':
    game = Game(8)
    game.run()