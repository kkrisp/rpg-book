#!/usr/bin/env python

import sys
import os
import time
from datetime import datetime # for dating logfileElmenti a jatek ideje
import argparse
import curses # for visual commands
#import getch

# arguments
argParser = argparse.ArgumentParser(description="Kaland es kockazat!")
argParser.add_argument('--log', "-l",
                        action="store_true",
                        default=False,
                        help='Does nothing yet.')
args = argParser.parse_args()
buttons = [
    "PRINT GRID",
    "SAVE GCODE"
]

def draw_layout(screen, x0, y0, fileName):
        layout = open(fileName, 'r')
        screen.addstr(x0, y0, layout.read())
        layout.close()

def draw_list(screen, x0, y0, elements, highlight, spacing=1, refresh=True):
    """Writes out list elements to the screen, highlights the ones
    marked with '1' in the highlight list
    refresh = makes menu appear instantly on the screen
    spacing = the number of empty lines between elements"""
    x = 0 # the list elements are in different lines, their x coordinate changes
    for el in elements:
        if x != highlight:
            screen.addstr(x0 + x*spacing, y0, " " + str(el) + " ")
        else:
            screen.addstr(x0 + x*spacing, y0, " " + str(el) + " ", curses.A_REVERSE)
        x += 1
    if refresh:
        screen.refresh()

def draw_table(screen, x0, y0, elements, highlight, width=2, x_spacing=1, y_spacing=16, refresh=True):
    """Prints elements on the screen in multiple columns, 
    width: number of columns"""

    for i in range(len(elements)/2):
        for j in range(width):
            if i != highlight:
                screen.addstr(x0+i*x_spacing, y0+j*y_spacing, " " + str(elements[i*width+j]) + " ")
            else:
                screen.addstr(x0+i*x_spacing, y0+j*y_spacing, " " + str(elements[i*width+j]) + " ", curses.A_REVERSE)
    if refresh:
        screen.refresh()

def draw_positions(screen, x0, y0, elements, highlight, spacing=1, refresh=True):
    x = 0 # the list elements are in different lines, their x coordinate changes
    for el in elements:
        if x != highlight:
            screen.addstr(x0 + x*spacing, y0, " " + el.toString() + " ")
        else:
            screen.addstr(x0 + x*spacing, y0, " " + el.toString() + " ", curses.A_REVERSE)
        x += 1
    if refresh:
        screen.refresh()

def selection_handler(nextIndex, listLength):
    """ Does not let counter step out of the index range
    expecting the step size to be smaller than the list length"""
    if nextIndex >= 0: return nextIndex % listLength
    else: return listLength+nextIndex # if the index goes negative

def value_changer(value, changeBy):
    """Inverts booleans, does not allow ints and floats be smaller than 0"""
    if type(value) is bool: return not value
    
    #'changeBy' is usually 1 or -1, floats are altered in smaller steps
    elif type(value) is int:
        if (value+changeBy) > 0 : return value + changeBy
        else: return 0
    else:
        changeBy = changeBy*0.1
        if (value+changeBy) > 0.0 : return value + changeBy
        else: return 0.0

def position_submenu(screen, x0, y0):
    screen.addstr(x0, y0,   "+-----------------------------+")
    screen.addstr(x0+1, y0, "| +-------------------------+ |")
    screen.addstr(x0+2, y0, "| |   GO   | RESET | CANCEL | |")
    screen.addstr(x0+3, y0, "| |  (g)   |  (r)  |  (c)   | |")
    screen.addstr(x0+4, y0, "| +-------------------------+ |")
    screen.addstr(x0+5, y0, "+-----------------------------+")
    while 1:
        c = screen.getch()
        if c == ord('g'):
            return 1
        elif c == ord('r'):
            return 2
        else:
            return 0

def value_from_user(screen, x0, y0, maxLength):
    """Gets a string from the user. Generates a 'write there' field
    at the given place with the length of the maximum available input length."""
    curses.echo()
    screen.addstr(x0, y0, ("_"*(maxLength+1)))
    s = screen.getstr(x0, y0+1, maxLength)
    curses.noecho()
    return s

def get_adventure_titles():
    title_list = []
    for file in os.listdir("./"):
        if file.split('.')[1] == "adv":
            title = ""
            for line in open(file, 'r'):
                words = line.split(' ')
                if words[0] == "TITLE":
                    for w in range(1, len(words)-1):
                        title += words[w] + " "
                    title += words[len(words)-1].split("\n")[0]
                    break
            title_list.append(title)
    return title_list

stdscr = curses.initscr() # returns a window object
curses.noecho()           # turns off automatic echoing keys to the screen
curses.cbreak()           # reacting to keypresses without pressing enter
stdscr.keypad(1)          # arrowkeys, etc are registered too

maxx, maxy = stdscr.getmaxyx()  # get size of the screen
curses.curs_set(0)              # set cursor out of the screen

welcome_text = "Valaszthato kalandok:"
available_adventures = get_adventure_titles()
currentlySelected = 0
maxindex = len(available_adventures)

try:
    while 1:
        stdscr.addstr(maxx/4, int(maxy/2-len(welcome_text)/2), welcome_text)
        draw_list(stdscr, maxx/4+1, int(maxy/2-len(welcome_text)/2), available_adventures, currentlySelected)
        c = stdscr.getch()
        # exit program
        if c == ord('q'):
            if args.log: lf.write(logf('q'))
            break  # Exit the while()

        # navigating the menu
        elif c == curses.KEY_UP:
            if args.log: lf.write(logf("UP"))
            currentlySelected = selection_handler(currentlySelected-1, maxindex)
        elif c == curses.KEY_DOWN:
            if args.log: lf.write(logf("DOWN"))
            currentlySelected = selection_handler(currentlySelected+1, maxindex)
            
except: # closes the functions properly in case of error
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    # restoring terminal to its original mode
    curses.endwin()
    raise

#shutting down curses
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
# restoring terminal to its original mode
curses.endwin()
sys.exit()

try:
    while False:
        maxindex = 16 + lb + len(myPositions)+1
        #stdscr.addstr(10, 1, str(currentlySelected)) # show currently selected
        draw_layout("window-layout.txt")
        draw_table(14, 2, settings, currentlySelected)
        draw_list(14, 28, buttons, currentlySelected-13, 2)
        draw_list(2, 37, stepSizes, currentlySelected-13-lb, 3)
        draw_list(32, 2, myPosName, currentlySelected-16-lb, 1)
        draw_positions(32, 15, myPositions, currentlySelected-16-lb, 1)
        if currentlySelected == 12+lb: stdscr.addstr(28, 8, " ", curses.A_REVERSE)
        if currentlySelected == (maxindex-1): stdscr.addstr(32+len(myPosName), 2, " <add new> ", curses.A_REVERSE)
        else: stdscr.addstr(32+len(myPosName), 2, " <add new> ")
        c = stdscr.getch()
        
        # exit program
        if c == ord('q'):
            if args.log: lf.write(logf('q'))
            break  # Exit the while()

        # navigating the menu
        elif c == curses.KEY_UP:
            if args.log: lf.write(logf("UP"))
            currentlySelected = selection_handler(currentlySelected-1, maxindex)
        elif c == curses.KEY_DOWN:
            if args.log: lf.write(logf("DOWN"))
            currentlySelected = selection_handler(currentlySelected+1, maxindex)
        elif c == ord('\t'):
            if args.log: lf.write(logf("TAB"))
            if currentlySelected >= bigsteps[len(bigsteps)-1]: currentlySelected = bigsteps[0]
            else:
                for i in range(len(bigsteps)):
                    if bigsteps[i] > currentlySelected:
                        currentlySelected = bigsteps[i]
                        break

        # quickly changing values
        elif c == curses.KEY_LEFT:
            if args.log: lf.write(logf("LEFT"))
            if currentlySelected < 13:
                settings[currentlySelected*2+1] = value_changer(settings[currentlySelected*2+1], -1)
            elif currentlySelected == 13+lb:
                stepSizes[0] = stepSizes[0]*0.1
            elif currentlySelected == 14+lb:
                stepSizes[1] = stepSizes[1]*0.1
            elif currentlySelected == 15+lb:
                stepSizes[2] = stepSizes[2]*0.1
        elif c == curses.KEY_RIGHT:
            if args.log: lf.write(logf("RIGHT"))
            if currentlySelected < 13:
                settings[currentlySelected*2+1] = value_changer(settings[currentlySelected*2+1], 1)
            elif currentlySelected == 13+lb:
                stepSizes[0] = stepSizes[0]*10.0
            elif currentlySelected == 14+lb:
                stepSizes[1] = stepSizes[1]*10.0
            elif currentlySelected == 15+lb:
                stepSizes[2] = stepSizes[2]*10.0

        # manual control of the printer
        elif c == ord('w'):
            g.send(s, header, "G1 Y" + str(-stepSizes[0]), False)
        elif c == ord('a'):
            g.send(s, header, "G1 X" + str(-stepSizes[0]), False)
        elif c == ord('s'):
            g.send(s, header, "G1 Y" + str(stepSizes[0]), False)
        elif c == ord('d'):
            g.send(s, header, "G1 X" + str(stepSizes[0]), False)
        elif c == ord('j'):
            g.send(s, header, "G1 Z" + str(-stepSizes[1]), False)
        elif c == ord('k'):
            g.send(s, header, "G1 Z" + str(stepSizes[1]), False)
        elif c == ord('u'):
            g.send(s, header, "G1 E" + str(stepSizes[2]), False)
        elif c == ord('i'):
            g.send(s, header, "G1 E" + str(-stepSizes[2]), False)

        # giving exact value from keyboard
        elif c == ord('\n'):
            try:
                if currentlySelected < 13:
                    n = currentlySelected*2+1
                    if type(settings[n]) is bool: settings[n] = not settings[n]
                    else: settings[n] = type(settings[n])(value_from_user(14+currentlySelected, 18, 5))
                elif currentlySelected == 13+lb:
                    stepSizes[0] = float(value_from_user(2, 37, 5))
                elif currentlySelected == 14+lb:
                    stepSizes[1] = float(value_from_user(5, 37, 5))
                elif currentlySelected == 15+lb:
                    stepSizes[2] = float(value_from_user(8, 37, 5))
                elif currentlySelected == 13: # print grid
                    stdscr.addstr(10, 15, myPositions[0].getz())
                    if position_submenu(stdscr, 17, 9) == 1: printGrid(s, settings, myPositions[0])
                elif currentlySelected == 12 + lb: # send command, dont wait
                    g.send(s, header, value_from_user(28, 8, 38), False)
                elif currentlySelected == (maxindex-1): # add new position
                    newName = value_from_user(32+len(myPositions), 2, 10)
                    x, y, z = parsePosition(s)
                    if x and y and z:
                        myPositions.append(g.Position(x, y, z))
                        myPosName.append(newName)

                elif currentlySelected >= 16+lb: # currently in position list
                    stdscr.addstr(10, 10, myPositions[currentlySelected - 16-lb].getz())
                    com = position_submenu(stdscr, 22, 10) 
                    if com == 1:
                        #stdscr.addstr(10, 15, myPositions[currentlySelected-16-lb].getz())
                        goToPosition(s, myPositions[currentlySelected-16-lb], myPositions[0])
                    if com == 2:
                        x, y, z = parsePosition(s)
                        if x and y and z:
                            myPositions[currentlySelected-16-lb] = g.Position(x, y, z)
            except:
                pass

    #savedGcode.close()
except: # closes the functions properly in case of error
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    # restoring terminal to its original mode
    curses.endwin()
    raise

#shutting down curses
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
# restoring terminal to its original mode
curses.endwin()
