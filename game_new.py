import os
from math import tan, radians, degrees, copysign, hypot, sqrt, sin, cos, pi, atan, acos
import time

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
    screen = None

    def __init__(self, pos, screen):
        self.pos = pos
        self.rand_dir
        self.screen = screen

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
        self.pos = [(self.pos[0]), (self.pos[1])]

    def draw(self):
        o_pos = [int(self.pos[0]), int(self.pos[1])]
        pygame.draw.circle(self.screen, RED, o_pos, 20)

class player:
    pos = [0, 0]
    velocity = Vector2()
    speed = 5
    screen = None
    sensors = []

    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen
        self.velocity = Vector2(self.speed, 0).rotate(randrange(360))

    def left(self):
        # Set random direction vector of magnitude speed
        self.velocity = self.velocity.rotate(-20)

    def right(self):
        # Set random direction vector of magnitude speed
        self.velocity = self.velocity.rotate(20)

    def move(self):
        # Check if about to hit frame, if so change velocity direction
        crash = False
        if self.pos[0]+self.velocity[0] <= 20 or self.pos[0]+self.velocity[0] >= 980:
            self.velocity = Vector2(self.velocity[0]*-1, self.velocity[1])
            crash = True
        if self.pos[1]+self.velocity[1] <= 20 or self.pos[1]+self.velocity[1] >= 580:
            self.velocity = Vector2(self.velocity[0], self.velocity[1]*-1)
            crash = True
        # Update position, turn to list
        self.pos += self.velocity
        self.pos = [(self.pos[0]), (self.pos[1])]
        return crash

    def create_sensors(self):
        self.sensors = []
        d = 8

        self.sensors.append(self.__sens_pos(0, d))
        self.sensors.append(self.__sens_pos(0, 2*d))
        self.sensors.append(self.__sens_pos(45, sqrt(2)*d))
        self.sensors.append(self.__sens_pos(45, sqrt(8)*d))
        self.sensors.append(self.__sens_pos(-45, sqrt(2)*d))
        self.sensors.append(self.__sens_pos(-45, sqrt(8)*d))
        self.sensors.append(self.__sens_pos(90, d))
        self.sensors.append(self.__sens_pos(90, 2*d))
        self.sensors.append(self.__sens_pos(-90, d))
        self.sensors.append(self.__sens_pos(-90, 2*d))
        self.sensors.append(self.__sens_pos(degrees(atan(0.5)), sqrt(5)*d))
        self.sensors.append(self.__sens_pos(degrees(atan(-0.5)), sqrt(5)*d))
        self.sensors.append(self.__sens_pos(degrees(atan(2)), sqrt(5)*d))
        self.sensors.append(self.__sens_pos(degrees(atan(-2)), sqrt(5)*d))

    def __sens_pos(self, angle, length):
        point = Vector2(self.pos)
        point += self.velocity.rotate(angle) * length
        point = [int(point[0]), int(point[1])]
        return point


    def draw(self):
        # Draw blue circle and arc indicating position of movement
        player_pos = [int(self.pos[0]), int(self.pos[1])]
        pygame.draw.circle(self.screen, BLUE, player_pos, 20)
        arc_setting = [int(self.pos[0]) - 20, int(self.pos[1]) - 20, 40, 40]
        arc_angle = radians((self.velocity.as_polar()[1] * (-1)) % 360)
        pygame.draw.arc(self.screen, WHITE, arc_setting, arc_angle - pi / 4, arc_angle + pi / 4, 2)
        for p in self.sensors:
            pygame.draw.circle(self.screen, WHITE, p, 2)


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

    def collisions(self):
        for ob in self.obstacles:
            dis = hypot(self.player.pos[0]-ob.pos[0], self.player.pos[1]-ob.pos[1])
            if dis <= 40:
                return True
        return False

    def run(self):
        self.clock.tick(self.ticks)

        while not self.exit:
            # Check if quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            if self.collisions():
                print("Dead")

            # move obstacles
            for o in self.obstacles:
                o.move()
            # move player
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT]:
                self.player.right()
            if pressed[pygame.K_LEFT]:
                self.player.left()
            if self.player.move():
                print("Dead")

            # Initialize sensor positions
            self.player.create_sensors()

            # Check collisions
            self.collisions()

            # Draw
            self.screen.fill(BLACK)
            for o in self.obstacles:
                o.draw()
            self.player.draw()

            # Draw menu
            s = pygame.Surface((200, 100), pygame.SRCALPHA)  # per-pixel alpha
            s.fill((255, 255, 255, 70))  # notice the alpha value in the color
            self.screen.blit(s, (10, 10))
            pygame.display.update()
            self.clock.tick(self.ticks)


if __name__ == '__main__':
    game = Game(20)
    game.run()