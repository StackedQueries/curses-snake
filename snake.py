# -*- coding: utf-8 -*-
import curses
import locale

def draw_game(stdscr):

    k = 0
    height, width = stdscr.getmaxyx()
    cursor_x = width// 2
    cursor_y = height //2

    # Clear and refresh the screen for a blank canvas
    stdscr.erase()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)

    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    frame = 0

    while (k != ord('q')):
        frame += 1
        # Initialization
        stdscr.erase()
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


        stdscr.addstr(1, 1, "frame:{}".format(frame))
        stdscr.addstr(2, 1, "key:{}".format(k))
        stdscr.addstr(3, 1, "char:{}".format(chr(219)))

        stdscr.attron(curses.color_pair(1))
        stdscr.border();
        stdscr.attroff(curses.color_pair(1))

        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        curses.halfdelay(5)
        last=k
        k = stdscr.getch()
        if k == -1:
            k = last


def main():
    curses.wrapper(draw_game)

if __name__ == "__main__":
    main()