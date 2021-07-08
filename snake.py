# -*- coding: utf-8 -*-
import curses
import locale
import random

BLOCK = u"\u2588"

class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


def draw_apple(stdscr, snake):
    coords = []
    height, width = stdscr.getmaxyx()
    for i in range(height-2):
        for j in range(width-2):
            coords.append((i+1,j+1))
    snakepoints=snake_points(snake)
    loc = random.choice([i for i in coords if i not in snakepoints])
    return (loc[0], loc[1])

def snake_points(snake):
    snakepoints=[]
    while snake.next != None:
        snakepoints.append(snake.data)
        snake = snake.next
    return snakepoints

def draw_snake(stdscr, snake, data, head=False):


    y, x = data
    stdscr.addstr(y, x, BLOCK)
    nextdata = snake.data
    snake.data = (y,x)

    if snake.next == None:
        return True


    draw_snake(stdscr, snake.next, nextdata)

def draw_game(stdscr):

    k = 0
    height, width = stdscr.getmaxyx()
    cursor_x = width// 2
    cursor_y = height //2

    snake = Node((cursor_y,cursor_x))

    apple = draw_apple(stdscr, snake)
    # Clear and refresh the screen for a blank canvas
    stdscr.erase()
    stdscr.refresh()
    curses.curs_set(0)

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)

    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    frame = 0

    while (k != ord('q')):
        frame += 1
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1


        cursor_x = max(1, cursor_x)
        cursor_x = min(width - 2, cursor_x)

        cursor_y = max(1, cursor_y)
        cursor_y = min(height - 2, cursor_y)


        #stdscr.addstr(1, 1, "frame:{}".format(frame))
        #stdscr.addstr(2, 1, "key:{}".format(k))
        #stdscr.addstr(3, 1, "char:{}".format(BLOCK))

        stdscr.attron(curses.color_pair(1))
        stdscr.border();
        stdscr.attroff(curses.color_pair(1))

        stdscr.move(cursor_y, cursor_x)
        if (cursor_y, cursor_x) == apple:
            snake = Node((cursor_y, cursor_x), snake)
            apple = draw_apple(stdscr,snake)
        sp = snake_points(snake)

        draw_snake(stdscr, snake, (cursor_y,cursor_x), True)

        if sp.count((cursor_y,cursor_x)) > 0:
            exit()

        stdscr.addstr(apple[0], apple[1], "*")

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        curses.halfdelay(1)
        last=k
        k = stdscr.getch()
        if k == -1:
            k = last


def main():
    curses.wrapper(draw_game)

if __name__ == "__main__":
    main()