import sys
import random
import math
import pygame

pygame.init()
pygame.display.set_caption('Gravitational N-body simulation')
screen_size = 1000
screen = pygame.display.set_mode((screen_size, screen_size))

yellow = (255, 255, 102)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

clock = pygame.time.Clock()
game_speed = 30


class Body:
    def __init__(self):
        self.mass = self.rand_mass()
        self.pos = self.rand_coord()
        self.dir = self.rand_dir()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def rand_mass():
        return random.randint(100, 1000)

    @staticmethod
    def rand_coord():
        return [random.randint(int(screen_size / 3), int(screen_size * 2 / 3)), random.randint(int(screen_size / 3), int(screen_size * 2 / 3))]

    @staticmethod
    def rand_dir():
        dir_x = random.randint(-50, 50) / 100
        dir_y = random.randint(-50, 50) / 100
        return [dir_x, dir_y]


class Simulation:
    def __init__(self):
        self.is_running = True
        self.g = 0.001

    def run_simulation(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            pygame.display.set_caption(f"Gravitational N-body simulation FPS:{round(clock.get_fps(),2)}")
            screen.fill(black)
            dt = clock.get_time() / 1000
            for i in bodies:
                self.move_body(i)
                self.draw_body(i.mass, i.pos)
            pygame.display.update()
            for i in bodies:
                for j in bodies:
                    self.change_v(i, j, dt)
            clock.tick(game_speed)

    def draw_body(self, m, pos):
        r = ((m/3.1415)**(1/3))/1.5
        if r < 1:
            r = 1
        if m > 850:
            body_colour = yellow
        elif m > 600:
            body_colour = green
        elif m > 350:
            body_colour = blue
        else:
            body_colour = red
        pygame.draw.circle(screen, body_colour, pos, r)

    def move_body(self, body):
        body.pos[0] += body.dir[0]
        body.pos[1] += body.dir[1]

    def change_v(self, body1, body2, dt):
        if body1 == body2:
            a_vec = [0, 0]
        else:
            dist = math.sqrt(pow(body1.pos[0] - body2.pos[0], 2) + pow(body1.pos[1] - body2.pos[1], 2))
            if dist <= 1:
                a_vec = [0, 0]
            else:
                v_vec = [-1 * (body1.pos[0] - body2.pos[0]) / dist, -1 * (body1.pos[1] - body2.pos[1]) / dist]
                f = (self.g * body1.mass * body2.mass) / pow(dist, 1)  # To apply the simulation to a 3D space, divide by distance on the power of 2
                f_vec = [v_vec[0] * f, v_vec[1] * f]
                a_vec = [f_vec[0] / body1.mass, f_vec[1] / body1.mass]

        body1.dir = [body1.dir[0] + (a_vec[0] * dt), body1.dir[1] + (a_vec[1] * dt)]


if __name__ == '__main__':
    simulation = Simulation()
    N_OF_BODIES = 160
    bodies = [Body() for i in range(N_OF_BODIES)]
    for i in bodies:
        print(i.mass, " ", i.pos, " ", i.dir)
    simulation.run_simulation()

    sys.exit(0)
