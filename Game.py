import os
from math import tan, radians, degrees, copysign, hypot
import pygame
from pygame.math import Vector2

class Car:
    def __init__(self, x, y, angle=0.0, length=4,
                 max_steering=60, max_acceleration=5.0):
        self.position = Vector2(x,y)
        self.velocity = Vector2(1.0, 0.0)
        self.angle = angle
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 10
        self.acceleration = 0.0
        self.steering = 0.0
        self.length = length
        self.car_image = pygame.transform.scale(pygame.image.load("car.png"), (60, 30))

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = min(self.velocity.x, self.max_velocity)
        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1000
        height = 600
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        self.clock.tick(self.ticks)

        road = pygame.image.load("export.png")
        self.screen.blit(road, (100,100))

        car = Car(0,0)
        car_image = pygame.image.load("car.png")
        car_image = pygame.transform.scale(car_image, (38, 19))

        ppu = 32

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queueR
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            car.acceleration += 2 * dt
            if pressed[pygame.K_RIGHT]:
                car.steering = -1800 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering = 1800 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
            car.update(dt)
            print(car.velocity)

            # Logic
            # Car logic goes here

            # Drawing
            self.screen.fill((255, 255, 255))
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.flip()


            self.clock.tick(self.ticks)
            # print(pygame.time.get_ticks())
        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()