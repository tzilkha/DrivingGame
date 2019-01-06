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
YELLOW =    (255, 255,   0)

# Environment obstacle
class obstacle:
    speed = 3

    def __init__(self, pos, screen, radius):
        self.pos = pos
        self.velocity = 0
        self.rand_dir
        self.screen = screen
        self.radius = radius

    # Set random direction vector of magnitude speed
    def rand_dir(self):
        self.velocity = Vector2(self.speed, 0).rotate(randrange(360))

    # Move obstacle based on velocity vector
    def move(self):
        # Check if about to hit frame, if so change velocity direction
        dim = self.screen.get_size()
        if self.pos[0]+self.velocity[0] <= self.radius or self.pos[0]+self.velocity[0] >= dim[0]-self.radius:
            self.velocity = Vector2(self.velocity[0]*-1, self.velocity[1])
        if self.pos[1]+self.velocity[1] <= self.radius or self.pos[1]+self.velocity[1] >= dim[1]-self.radius:
            self.velocity = Vector2(self.velocity[0], self.velocity[1]*-1)
        # Update position, turn to list
        self.pos += self.velocity
        self.pos = [(self.pos[0]), (self.pos[1])]

    # Draw obstacle
    def draw(self):
        o_pos = [int(self.pos[0]), int(self.pos[1])]
        pygame.draw.circle(self.screen, RED, o_pos, self.radius)

# Agent
class player:
    speed = 5
    sensor_length = 8

    def __init__(self, pos, screen, radius):
        self.pos = pos
        self.screen = screen
        self.velocity = Vector2(self.speed, 0).rotate(randrange(360))
        self.radius = radius
        self.sensors = []

    # Rotate left
    def left(self):
        # Set random direction vector of magnitude speed
        self.velocity = self.velocity.rotate(-20)

    # Rotate right
    def right(self):
        self.velocity = self.velocity.rotate(20)

    # Move player based on velocity vector
    def move(self):
        # Check if about to hit frame, if so change velocity direction
        dim = self.screen.get_size()
        crash = False
        if self.pos[0]+self.velocity[0] <= self.radius or self.pos[0]+self.velocity[0] >= dim[0]-self.radius:
            self.velocity = Vector2(self.velocity[0]*-1, self.velocity[1])
            crash = True
        if self.pos[1]+self.velocity[1] <= self.radius or self.pos[1]+self.velocity[1] >= dim[1]-self.radius:
            self.velocity = Vector2(self.velocity[0], self.velocity[1]*-1)
            crash = True
        # Update position, turn to list
        self.pos += self.velocity
        self.pos = [(self.pos[0]), (self.pos[1])]
        return crash

    # Set up sensor field
    def create_sensors(self):
        # Set relative distance of sensors
        d = self.sensor_length
        self.sensors = []
        # Front row sensors
        self.sensors.append(self.__sens_pos(-45, sqrt(8)*d))
        self.sensors.append(self.__sens_pos(degrees(atan(-0.5)), sqrt(5)*d))
        self.sensors.append(self.__sens_pos(0, 2*d))
        self.sensors.append(self.__sens_pos(degrees(atan(0.5)), sqrt(5)*d))
        self.sensors.append(self.__sens_pos(45, sqrt(8)*d))
        # Middle row sensors
        self.sensors.append(self.__sens_pos(degrees(atan(-2)), sqrt(5)*d))
        self.sensors.append(self.__sens_pos(-45, sqrt(2)*d))
        self.sensors.append(self.__sens_pos(0, d))
        self.sensors.append(self.__sens_pos(45, sqrt(2)*d))
        self.sensors.append(self.__sens_pos(degrees(atan(2)), sqrt(5)*d))
        # Back row sensors
        self.sensors.append(self.__sens_pos(-90, 2*d))
        self.sensors.append(self.__sens_pos(-90, d))
        self.sensors.append(self.__sens_pos(90, d))
        self.sensors.append(self.__sens_pos(90, 2*d))

    # Return position of a sensor given angle deviation from movement and distance
    def __sens_pos(self, angle, length):
        point = Vector2(self.pos)
        point += self.velocity.rotate(angle) * length
        point = [int(point[0]), int(point[1])]
        return point

    # Calculate which sensors are touched given the radius of obstacles
    def sensor_readings(self, obstacle_locations, r):
        dim = self.screen.get_size()
        reading = [False for x in range(len(self.sensors))]
        for x in range(len(reading)):
            sensor = self.sensors[x]
            if sensor[0] <= 0 or sensor[0] >= dim[0]:
                reading[x] = True
            elif sensor[1] <= 0 or sensor[1] >= dim[1]:
                reading[x] = True
            if not reading[x]:
                for ob in obstacle_locations:
                    ob = ob.pos
                    if hypot(ob[0]-sensor[0], ob[1]-sensor[1])<=r:
                        reading[x] = True
                        break
        return reading

    # Display readings as readable text to console
    def print_readings(self, readings):
        print("\n")
        for s in ["+" if x else "-" for x in readings[0:5]]: print(s+"   ", end="")
        print("\n")
        for s in ["+" if x else "-" for x in readings[5:10]]: print(s+"   ", end="")
        print("\n")
        last = ["+" if x else "-" for x in readings[10:12]]+ ["O"] + ["+" if x else "-" for x in readings[12:14]]
        for s in last: print(s+"   ", end="")
        print("\n")

    # Draw player and sensors
    def draw(self, reading = None):
        # Draw blue circle and arc indicating position of movement
        player_pos = [int(self.pos[0]), int(self.pos[1])]
        pygame.draw.circle(self.screen, BLUE, player_pos, self.radius)
        arc_setting = [int(self.pos[0]) - self.radius, int(self.pos[1]) - self.radius, 2*self.radius, 2*self.radius]
        arc_angle = radians((self.velocity.as_polar()[1] * (-1)) % 360)
        pygame.draw.arc(self.screen, WHITE, arc_setting, arc_angle - pi / 4, arc_angle + pi / 4, 1)
        # Color sensors in different color if reading is provided, otherwise all white
        if reading is None:
            for p in self.sensors:
                pygame.draw.circle(self.screen, WHITE, p, 1)
        else:
            for p in range(len(self.sensors)):
                if reading[p]: pygame.draw.circle(self.screen, YELLOW, self.sensors[p], 6)
                else: pygame.draw.circle(self.screen, WHITE, self.sensors[p], 1)


class Game:
    def __init__(self, n_obstacles, generation = 0, best = 0):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.ticks = 30
        self.exit = False
        self.obstacles = []
        self.player = player([int(self.screen.get_size()[0]/2),int(self.screen.get_size()[1]/2)], self.screen, 20)
        self.obstacle_radius = 20
        self.initialize(n_obstacles)
        self.generation = generation
        self.best = best
        self.crash = False



    def initialize(self, n_obstacles):
        # Create obstacles, in random positions
        dim = self.screen.get_size()
        for n in range(n_obstacles):
            xr, yr = int(uniform(0,2)), int(uniform(0,2))
            if xr : x = (randint(self.obstacle_radius, int(dim[0]/3)))
            else :  x = (randint(int(dim[0]*2/3), int(dim[0])))
            if yr : y = (randint(self.obstacle_radius, int(dim[1]/3)))
            else :  y = (randint(int(dim[1]*2/3), int(dim[1])))
            pos = [x, y]
            ob = obstacle(pos, self.screen, self.obstacle_radius)
            ob.rand_dir()
            self.obstacles.append(ob)

    def collisions(self):
        for ob in self.obstacles:
            dis = hypot(self.player.pos[0]-ob.pos[0], self.player.pos[1]-ob.pos[1])
            if dis <= 40: #####
                return True
        return False

    def run(self):
        self.clock.tick(self.ticks)
        font = pygame.font.SysFont("monospace", 30)

        while not self.exit and not self.crash:
            # Check if quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    break

            if self.collisions():
                self.crash = True
                break

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
                self.crash = True
                break

            # Initialize sensor positions
            self.player.create_sensors()

            readings = self.player.sensor_readings(self.obstacles, self.obstacle_radius)
            self.player.print_readings(readings)

            # Check collisions
            self.collisions()

            # Get the time that has passed
            time = pygame.time.get_ticks()/1000
            score = font.render("Score: " + str(time), 10, GREEN)
            gen = font.render("Generation: " + str(self.generation), 10, GREEN)
            best = font.render("Best: " + str(self.best), 10, GREEN)


            # Draw
            self.screen.fill(BLACK)
            for o in self.obstacles:
                o.draw()
            self.player.draw(readings)

            # Draw menu and scores
            s = pygame.Surface((200, 100), pygame.SRCALPHA)  # per-pixel alpha
            s.fill((255, 255, 255, 70))  # notice the alpha value in the color
            self.screen.blit(s, (10, 10))
            self.screen.blit(gen, (15,15))
            self.screen.blit(score, (15,50))
            self.screen.blit(best, (15,85))

            pygame.display.update()
            self.clock.tick(self.ticks)

        print("Score: " + str(time))
        if self.crash: input("Game Over - Press Enter to continue...")


if __name__ == '__main__':
    game = Game(20)
    game.run()