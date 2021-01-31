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
blue = (0, 100, 255)

clock = pygame.time.Clock()
game_speed = 30


class Body:
    def __init__(self, mass, pos, dir):
        self.mass = mass
        self.pos = [pos[0], pos[1]]
        self.dir = [dir[0], dir[1]]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class IntNode:
    def __init__(self, x, y, size):
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.size = size
        self.mass = 0
        self.pos = [0.0, 0.0]  # Centre of mass position
        self.centre = [x, y]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

    def add(self, mass, pos, dir):
        if pos[0] < self.centre[0] and pos[1] < self.centre[1]:
            if self.nw is None:
                self.nw = Body(mass, pos, dir)
            elif str(self.nw) == "IntNode":
                self.nw.add(mass, pos, dir)
            elif math.sqrt(pow(self.nw.pos[0] - pos[0], 2) + pow(self.nw.pos[1] - pos[1], 2)) > 1.e-5:
                t_mass = self.nw.mass
                t_pos = self.nw.pos
                t_dir = self.nw.dir
                self.nw = IntNode(self.centre[0] - self.size * 0.25, self.centre[1] - self.size * 0.25, self.size / 2)
                self.nw.add(t_mass, t_pos, t_dir)
                self.nw.add(mass, pos, dir)
        elif pos[0] >= self.centre[0] and pos[1] < self.centre[1]:
            if self.ne is None:
                self.ne = Body(mass, pos, dir)
            elif str(self.ne) == "IntNode":
                self.ne.add(mass, pos, dir)
            elif math.sqrt(pow(self.ne.pos[0] - pos[0], 2) + pow(self.ne.pos[1] - pos[1], 2)) > 1.e-5:
                t_mass = self.ne.mass
                t_pos = self.ne.pos
                t_dir = self.ne.dir
                self.ne = IntNode(self.centre[0] + self.size * 0.25, self.centre[1] - self.size * 0.25, self.size / 2)
                self.ne.add(t_mass, t_pos, t_dir)
                self.ne.add(mass, pos, dir)
        elif pos[0] < self.centre[0] and pos[1] >= self.centre[1]:
            if self.sw is None:
                self.sw = Body(mass, pos, dir)
            elif str(self.sw) == "IntNode":
                self.sw.add(mass, pos, dir)
            elif math.sqrt(pow(self.sw.pos[0] - pos[0], 2) + pow(self.sw.pos[1] - pos[1], 2)) > 1.e-5:
                t_mass = self.sw.mass
                t_pos = self.sw.pos
                t_dir = self.sw.dir
                self.sw = IntNode(self.centre[0] - self.size * 0.25, self.centre[1] + self.size * 0.25, self.size / 2)
                self.sw.add(t_mass, t_pos, t_dir)
                self.sw.add(mass, pos, dir)
        else:
            if self.se is None:
                self.se = Body(mass, pos, dir)
            elif str(self.se) == "IntNode":
                self.se.add(mass, pos, dir)
            elif math.sqrt(pow(self.se.pos[0] - pos[0], 2) + pow(self.se.pos[1] - pos[1], 2)) > 1.e-5:
                t_mass = self.se.mass
                t_pos = self.se.pos
                t_dir = self.se.dir
                self.se = IntNode(self.centre[0] + self.size * 0.25, self.centre[1] + self.size * 0.25, self.size / 2)
                self.se.add(t_mass, t_pos, t_dir)
                self.se.add(mass, pos, dir)

        if self.mass == 0:
            self.pos = pos
        else:
            self.pos = self.centre_of_mass(self.pos, self.mass, pos, mass)
        self.mass += mass

    def centre_of_mass(self, b1_p, b1_m, b2_p, b2_m):
        cx = (b1_p[0] * b1_m + b2_p[0] * b2_m) / (b1_m + b2_m)
        cy = (b1_p[1] * b1_m + b2_p[1] * b2_m) / (b1_m + b2_m)
        return [cx, cy]


class Simulation:
    def __init__(self):
        self.is_running = True
        self.G = 0.001
        self.THETA = 0.5
        self.MIN_WEIGHT = 100
        self.MAX_WEIGHT = 1000
        self.N_OF_BODIES = 200

    def run_simulation(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            pygame.display.set_caption(f"Gravitational N-body simulation FPS:{round(clock.get_fps(),2)}")
            screen.fill(black)
            dt = clock.get_time() / 1000
            root = IntNode(500, 500, 1000)
            for i in bodies:
                self.move_body(i)
                self.draw_body(i.mass, i.pos)
                root.add(i.mass, i.pos, i.dir)
            pygame.display.update()
            for i in bodies:
                self.barnes_hut(i, root, dt)
            clock.tick(game_speed)

    def draw_body(self, m, pos):
        r = ((m/3.1415)**(1/3))/1.5
        if r < 1:
            r = 1
        if m > (simulation.MAX_WEIGHT - simulation.MIN_WEIGHT) * 0.85:
            body_colour = yellow
        elif m > (simulation.MAX_WEIGHT - simulation.MIN_WEIGHT) * 0.6:
            body_colour = blue
        elif m > (simulation.MAX_WEIGHT - simulation.MIN_WEIGHT) * 0.35:
            body_colour = red
        else:
            body_colour = green
        pygame.draw.circle(screen, body_colour, pos, r)

    def move_body(self, body):
        body.pos[0] += body.dir[0]
        body.pos[1] += body.dir[1]

    def change_v(self, body1, body2, dt):
        if body1 == body2:
            a_vec = [0, 0]
        else:
            dist = self.get_dist(body1, body2)
            if dist <= 1:
                a_vec = [0, 0]
            else:
                v_vec = [-1 * (body1.pos[0] - body2.pos[0]) / dist, -1 * (body1.pos[1] - body2.pos[1]) / dist]
                # To apply the simulation to a 3D space, divide by distance on the power of 2 in the equation below
                f = (self.G * body1.mass * body2.mass) / pow(dist, 1)
                f_vec = [v_vec[0] * f, v_vec[1] * f]
                a_vec = [f_vec[0] / body1.mass, f_vec[1] / body1.mass]

        body1.dir = [body1.dir[0] + (a_vec[0] * dt), body1.dir[1] + (a_vec[1] * dt)]

    def get_dist(self, body1, body2):
        return math.sqrt(pow(body1.pos[0] - body2.pos[0], 2) + pow(body1.pos[1] - body2.pos[1], 2))

    def barnes_hut(self, body, node, dt):
        if body.pos == node.pos:
            return False
        elif str(node) == 'Body':
            self.change_v(body, node, dt)
        elif (node.size / self.get_dist(body, node)) < self.THETA:
            self.change_v(body, node, dt)
        else:
            if node.nw is not None:
                self.barnes_hut(body, node.nw, dt)
            if node.ne is not None:
                self.barnes_hut(body, node.ne, dt)
            if node.sw is not None:
                self.barnes_hut(body, node.sw, dt)
            if node.se is not None:
                self.barnes_hut(body, node.se, dt)


def rand_mass():
    return random.randint(simulation.MIN_WEIGHT, simulation.MAX_WEIGHT)


def rand_coord():
    ss = screen_size
    return [random.randint(int(ss*0.25), int(ss*0.75)), random.randint(int(ss*0.25), int(ss*0.75))]


def rand_dir():
    dir_x = random.randint(-50, 50) / 200
    dir_y = random.randint(-50, 50) / 200
    return [dir_x, dir_y]


if __name__ == '__main__':
    simulation = Simulation()

    bodies = [Body(rand_mass(), rand_coord(), rand_dir()) for i in range(simulation.N_OF_BODIES)]

    simulation.run_simulation()

    sys.exit(0)
