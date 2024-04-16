from Cube import Cube
import pygame
import random

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)

class Snake(object):
    body = []
    visited = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.visited.append(pos)

    def clear_visited(self):
        self.visited.clear()

    def update_dir(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny

    def move_body(self):
        for i, c in enumerate(self.body):
            p = c.pos[:]

            # If there is a turn
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)  # If we haven't reached the edge just move in our current direction

    def move_with_mode(self, mode, fruit):
        if mode == "--shortest":
            self.move_shortest(fruit)
        elif mode == "--better-shortest":
            self.move_shortest_enhanced(fruit)
        else:
            self.move_keys()

    def move_shortest(self, fruit):
        for e in pygame.event.get():
            None
        currDir = (self.dirnx, self.dirny)
        rDist = (fruit.dist_to_cube(self.body[0].get_right_cube_coords()), RIGHT)
        lDist = (fruit.dist_to_cube(self.body[0].get_left_cube_coords()), LEFT)
        upDist = (fruit.dist_to_cube(self.body[0].get_up_cube_coords()), UP)
        downDist = (fruit.dist_to_cube(self.body[0].get_down_cube_coords()), DOWN)

        if currDir == RIGHT:
            res = min([rDist, upDist, downDist], key=lambda i: i[0])[1]
        elif currDir == LEFT:
            res = min([lDist, upDist, downDist], key=lambda i: i[0])[1]
        elif currDir == UP:
            res = min([rDist, upDist, lDist], key=lambda i: i[0])[1]
        elif currDir == DOWN:
            res = min([rDist, lDist, downDist], key=lambda i: i[0])[1]

        self.update_dir(res[0], res[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def body_to_list(self):
        return list(map(lambda i: i.pos, self.body))

    def move_shortest_enhanced(self, fruit):
        for e in pygame.event.get():
            None

        lst = [(self.body[0].get_right_cube_coords(), RIGHT), (self.body[0].get_left_cube_coords(), LEFT),
               (self.body[0].get_up_cube_coords(), UP), (self.body[0].get_down_cube_coords(), DOWN)]

        available_dirs = list(filter(lambda i: i[0] not in self.body_to_list(), lst))
        # Reduces bias in picking direction of snake when it cannot get closer to the snack
        random.shuffle(lst)

        # Snake has closed itself in. Choose any direction and restart
        if len(available_dirs) == 0:
            res = UP
        else:
            res = min(available_dirs, key=lambda i: fruit.dist_to_cube(i[0]))[1]
        self.update_dir(res[0], res[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def move_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.update_dir(-1, 0)

                elif keys[pygame.K_RIGHT]:
                    self.update_dir(1, 0)

                elif keys[pygame.K_UP]:
                    self.update_dir(0, -1)

                elif keys[pygame.K_DOWN]:
                    self.update_dir(0, 1)

                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
