#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 12:39:13 2020

@author: mberland
"""

import curses, random

WIDTH = 10
HEIGHT = 10
cursor_x = 0
cursor_y = 0
cell_buffer_x = 3
cell_buffer_y = 2
grid_buffer_x = 2
grid_buffer_y = 4
info_buffer_x = (grid_buffer_x * 2 + cell_buffer_x * WIDTH)
info_buffer_y = grid_buffer_y
info_buffer_height = 3
log_buffer_y = info_buffer_height + info_buffer_y
log_buffer_x = info_buffer_x

class GridCell:
    def __init__(self, char = ".", y=0,x=0,colorpair=1):
        self.char = char
        self.y = y
        self.x = x
        self.colorpair = colorpair
        self.info = "???"

def init_grid():
    return [[GridCell(char=".",y=j,x=i,colorpair=random.choice([1,2,3])) for j in range(HEIGHT)] for i in range(WIDTH)]

def xg2c(x):
    return (x * cell_buffer_x) + grid_buffer_x
def yg2c(y):
    return (y * cell_buffer_y) + grid_buffer_y



def draw_grid(stdscr,current_grid):
    for i in range(len(current_grid)):
        for j in range(len(current_grid[i])):
            stdscr.attron(curses.color_pair(current_grid[i][j].colorpair))
            stdscr.addstr(yg2c(j),xg2c(i),current_grid[i][j].char)
            stdscr.attroff(curses.color_pair(current_grid[i][j].colorpair))

def draw_info_panel(stdscr, current_grid):
    global cursor_x
    global cursor_y
    c_cell = current_grid[cursor_x][cursor_y]
    output = "[{:d},{:d}]: {:s}".format(c_cell.x,c_cell.y,c_cell.info)
    stdscr.addstr(info_buffer_y,info_buffer_x,output)

def make_random_log():
    return ["{:>02d}:{:>02d}:{:>02d} {:s} {:s}".format(random.randint(0,12), 
                                                       random.randint(0,12),
                                                       random.randint(0,12), 
                                                       random.choice(["p1","p2"]),
                                                       random.choice(["plantwatered","plantplanted"])) 
                                          for i in range (10)]

def draw_log_panel(stdscr, log):
    for i in range(len(log)):
        stdscr.addstr(log_buffer_y + i,log_buffer_x,log[i])


def key_action(k):
    global cursor_x
    global cursor_y
    if k == curses.KEY_DOWN:
        cursor_y += 1
    elif k == curses.KEY_UP:
        cursor_y -= 1
    elif k == curses.KEY_RIGHT:
        cursor_x += 1
    elif k == curses.KEY_LEFT:
        cursor_x -= 1
    cursor_x = max(0, cursor_x)
    cursor_x = min(WIDTH-1, cursor_x)   
    cursor_y = max(0, cursor_y)
    cursor_y = min(HEIGHT-1, cursor_y)

def init_curses_settings():
    curses.curs_set(2)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)


def draw_window(stdscr):
    k = 0
    current_grid = init_grid()
    init_curses_settings()
    fake_log = make_random_log()
    while (ord('q') != k):
        key_action(k)
        stdscr.addstr(2, 2, "RAINBOW VIEWER")
        draw_grid(stdscr, current_grid)
        draw_info_panel(stdscr, current_grid)
        draw_log_panel(stdscr,fake_log)        
        stdscr.move(yg2c(cursor_y), xg2c(cursor_x))
        stdscr.refresh()
        k = stdscr.getch()

curses.wrapper(draw_window)
