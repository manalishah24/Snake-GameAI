import os
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from Snake import Snake
from Cube import Cube
import time
import sys
import datetime

def draw_grid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, w))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (w, y))


def redraw_window(surface, score):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)

    # Display the score on the game window
    font = pygame.font.SysFont(None, 20)  # Setting the font size to 15
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    surface.blit(score_text, (10, 10))

    pygame.display.update()


def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def game_over(s, argv):
    print('Score: ', len(s.body))
    scores.append(len(s.body))
    folder_path = 'data'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(os.path.join(folder_path, argv[0][2:] + '_lifetime_log.txt'), 'a+') as f:
        f.write('%s\n' % len(s.body))
    s.clear_visited()
    s.reset((random.randrange(rows), random.randrange(rows)))


def main(mode):
    global width, rows, s, snack, scores
    width = 500
    scores = []
    rows = 20

    pygame.init()
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, s), color=(0, 255, 0))
    flag = True
    redraw_window(win, 0)  # Initialize the score to 0
    clock = pygame.time.Clock()
    count = 0

    while flag and count < 50:
        pygame.time.delay(8)
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        if mode == "--shortest":
            s.move_shortest(snack)
        elif mode == "--better-shortest":
            s.move_shortest_enhanced(snack)
        else:
            s.move_keys()

        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(rows, s), color=(0, 255, 0))

        if ((s.body[0].pos[0] == -1) or
            (s.body[0].pos[0] == rows) or
            (s.body[0].pos[1] == -1) or
            (s.body[0].pos[1] == rows)):
            game_over(s, [mode])
            count += 1

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                game_over(s, [mode])
                count += 1
                break

        redraw_window(win, len(s.body))

    folder_path = 'data'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(os.path.join(folder_path, mode + datetime.datetime.today().strftime('%d-%m-%Y') + '.txt'), 'w') as f:
        for listitem in scores:
            f.write('%s\n' % listitem)


if __name__ == "__main__":
    main("--shortest")
    main("--better-shortest")
