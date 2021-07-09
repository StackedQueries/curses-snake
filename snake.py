# -*- coding: utf-8 -*-
import curses
import locale
import random

BLOCK = u"\u2588"


#Snake sections (Also a super cool linked list node)
class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

#Draws apple in random location that is not snake related
def draw_apple(stdscr, snake):
    coords = []
    height, width = stdscr.getmaxyx()
    for i in range(height-2):
        for j in range(width-2):
            coords.append((i+1,j+1)) #This is a mess and needs work
    snakepoints=snake_points(snake)
    loc = random.choice([i for i in coords if i not in snakepoints])
    return (loc[0], loc[1])


#Returns a list of all current locations of the snakes body
def snake_points(snake):
    snakepoints=[]
    while snake.next != None:
        snakepoints.append(snake.data)
        snake = snake.next
    return snakepoints

#draws updated snake on screen
def draw_snake(stdscr, snake, data, head=False):
    y, x = data
    stdscr.addstr(y, x, BLOCK)
    nextdata = snake.data
    snake.data = (y,x)

    if snake.next == None:
        return True

    draw_snake(stdscr, snake.next, nextdata)

#draws game board
def draw_game(stdscr):

    k = 0
    height, width = stdscr.getmaxyx() # gets max terminal size

    #centers snake
    cursor_x = width// 2
    cursor_y = height //2

    #init snake with single node
    snake = Node((cursor_y,cursor_x))

    #init first apple location
    apple = draw_apple(stdscr, snake)

    # erase and refresh the screen for a blank canvas
    stdscr.erase()
    stdscr.refresh()

    #turns cursor off
    curses.curs_set(0)

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    #frame counter
    frame = 0

    while (k != ord('q')):
        frame += 1


        # Initialization
        stdscr.clear() #look into performance. redrawing screen can lead to flickering sometimes
        height, width = stdscr.getmaxyx()


        #get key presses. TODO: update so pressing a random key doesn't stop the snake
        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1


        #Set boundaries for snake inside the border
        cursor_x = max(1, cursor_x)
        cursor_x = min(width - 2, cursor_x)
        cursor_y = max(1, cursor_y)
        cursor_y = min(height - 2, cursor_y)

        #Collision detection
        sp = snake_points(snake)
        if sp.count((cursor_y,cursor_x)) > 0:
            exit()

        #Sets border
        stdscr.attron(curses.color_pair(1))
        stdscr.border();
        stdscr.attroff(curses.color_pair(1))

        #set location of cursor
        stdscr.move(cursor_y, cursor_x)

        #Apple detection
        if (cursor_y, cursor_x) == apple:
            snake = Node((cursor_y, cursor_x), snake) #add onto the snake
            apple = draw_apple(stdscr,snake) #draw new apple

        #Draw snake
        draw_snake(stdscr, snake, (cursor_y,cursor_x), True)

        #Draw apple
        stdscr.addstr(apple[0], apple[1], "*")

        # Refresh the screen
        stdscr.refresh()

        # set to continue without input
        curses.halfdelay(1)
        last=k
        k = stdscr.getch()
        if k == -1:
            k = last


def main():
    curses.wrapper(draw_game)

if __name__ == "__main__":
    main()