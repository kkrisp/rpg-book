#!/usr/bin/env python

import sys
import os
import time
from datetime import datetime # for dating logfileElmenti a jatek ideje
import argparse
import curses # for visual commands
#import getch
import karakter as kar
import konyv as konyv_kalandokhoz

# arguments
argParser = argparse.ArgumentParser(description="Kaland es kockazat!")
argParser.add_argument("-l", "--log",
                        action="store_true",
                        default=False,
                        help='Megjegyzi a karakter valasztasait. (ez a funkcio meg nem mukodik)')
argParser.add_argument("-d", "--developer",
                        action="store_true",
                        default=False,
                        help='Fejlesztoi mod: oldalak szabad valtasa, extra infok megjelenitese.')
args = argParser.parse_args()
buttons = [
    "PRINT GRID",
    "SAVE GCODE"
]

valasz_betuk = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]  # a valaszok betujele


def szoveget_kiir(kepernyo, szoveg, x0, y0, maxhossz=80):
    sorszam = 0
    l_hossz = 0
    kiirando = ""
    for betu in szoveg:
        if betu == "\n" or l_hossz > maxhossz:
            if betu != "\n":
                kiirando += betu
            kepernyo.addstr(x0+sorszam, y0, kiirando)
            kiirando = ""
            l_hossz = 0
            sorszam += 1
        else:
            kiirando += betu
        l_hossz += 1
    kepernyo.addstr(x0+sorszam, y0, kiirando)


def sorokra_bont(szoveg):
    sor = ""
    bontott = []
    for k in szoveg:
        if k == "\n":
            bontott.append(sor)
            sor = ""
        else:
            sor += k
    return bontott

def hatteret_feltolt(fajlnev, hatter):
    hatter_fajl = open(fajlnev, 'r')
    for sor in hatter_fajl:
        hatter.append(sor)  # minden sor vegerol eltavolitva a newline karakter
    hatter_fajl.close()


def hatter_rajzolasa(kepernyo, hatter, x_pos=0, y_pos=0):
    x_szamlalo = 0
    for sor in hatter:
        kepernyo.addstr(x_pos + x_szamlalo, y_pos, sor)
        x_szamlalo += 1


def hatter_rajzolasa_kozepre(kepernyo, hatter):
    x_max, y_max = stdscr.getmaxyx()  # get size of the screen
    hatter_szelesseg = len(hatter[0])
    hatter_magassag = len(hatter)
    x_pos = int((x_max-hatter_magassag)/2)
    y_pos = int((y_max-hatter_szelesseg)/2)
    x_szamlalo = 0
    if hatter_magassag > x_max:
        print("nem eleg magas kepernyo")
    for sor in hatter:
        kepernyo.addstr(x_pos + x_szamlalo, y_pos, sor)
        x_szamlalo += 1


def hatter_szoveg_kordinata(kepernyo, hatter, x_belul=0, y_belul=0):
    x_max, y_max = stdscr.getmaxyx()  # get size of the screen
    hatter_szelesseg = len(hatter[0])
    hatter_magassag = len(hatter)
    x_pos = int((x_max-hatter_magassag)/2) + x_belul
    y_pos = int((y_max-hatter_szelesseg)/2) + y_belul
    return x_pos, y_pos

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

def ertekvaltoztato(ertek, valtoztatas, maxertek):
    kimeno_ertek = ertek + valtoztatas
    if kimeno_ertek > maxertek:
        kimeno_ertek = 0+valtoztatas
    elif kimeno_ertek < 1:
        kimeno_ertek = maxertek + valtoztatas + 1
    return kimeno_ertek


def karakterlapot_rajzol(kepernyo, karakter_in, x_pos=0, y_pos=0):
    nevsor = karakter_in.nev
    sorhossz = 22 + 2
    alahuzas = "-" * sorhossz
    sorszam = 0
    kepernyo.addstr(x_pos+sorszam, y_pos, nevsor)
    sorszam += 1
    kepernyo.addstr(x_pos+sorszam, y_pos, alahuzas)
    sorszam += 1
    eletero_sor = "  eletero          " + str(karakter_in.eletero) + "/" + str(karakter_in.max_eletero)
    kepernyo.addstr(x_pos+sorszam, y_pos, eletero_sor)
    sorszam += 1
    for tul in karakter_in.tulajdonsagok.keys():
        #alahuzas = " -" + "-" * sorhossz
        szunetek = (sorhossz - len(tul) - 7) * " "
        #tulajdonsagsor = " | " + tul + szunetek + "| " + str(karakter_in.tulajdonsagok[tul]) + " |"
        tulajdonsagsor = "  " + tul + szunetek + " " + str(karakter_in.tulajdonsagok[tul])
        kepernyo.addstr(x_pos+sorszam, y_pos, tulajdonsagsor)
        sorszam += 1
        #kepernyo.addstr(x_pos+sorszam, y_pos, alahuzas)
        #sorszam += 1
    x_pos = x_pos + 15
    sorszam = 0
    kepernyo.addstr(x_pos+sorszam, y_pos, "Targyak:         ")
    sorszam += 1
    for targy in karakter_in.targyak:
        kepernyo.addstr(x_pos+sorszam, y_pos, "  " + targy)
        sorszam += 1


def valasztasokat_kiir(kepernyo, valasz_lista, x0, y0, valasztott=1, szelesseg = 80):
    cnt = 0
    kijeloles = 1
    for val in valasz_lista:
        ki = valasz_betuk[cnt] + ") "
        n = 0
        for betu in val.szoveg:
            n += 1
            if betu == "\n" or n >= szelesseg:
                if betu != "\n":
                    ki += betu
                if kijeloles == valasztott:
                    kepernyo.addstr(x0 + cnt, y0, ki, curses.A_REVERSE)
                else:
                    kepernyo.addstr(x0 + cnt, y0, ki)
                ki = "   "
                cnt += 1
                n = 0
            else:
                ki += betu
        if kijeloles == valasztott:
            kepernyo.addstr(x0 + cnt, y0, ki, curses.A_REVERSE)
        else:
            kepernyo.addstr(x0 + cnt, y0, ki)
        cnt += 1
        kijeloles += 1


foszereplo = kar.Karakter()
foszereplo.nev = "Veer Istvan"
foszereplo.targyak.append("Alma")
foszereplo.targyak.append("Gyogyito ital")
foszereplo.targyak.append("Kotel")

egyszeru_hatter = []
hatteret_feltolt("jelenet_hatter.txt", egyszeru_hatter)

debug_mode = args.developer

# itt kezdodik a curses ablak
stdscr = curses.initscr() # returns a window object
curses.noecho()           # turns off automatic echoing keys to the screen
curses.cbreak()           # reacting to keypresses without pressing enter
stdscr.keypad(1)          # arrowkeys, etc are registered too

maxx, maxy = stdscr.getmaxyx()  # get size of the screen
curses.curs_set(0)              # set cursor out of the screen

k = konyv_kalandokhoz.Konyv()
konyv_kalandokhoz.beolvas("BekeX_csajozos.md", k)
kepernyore = ""  # a szoveg, amit az addstr paranccsal kinyomtatunk
nagy_szoveg = []
valaszlista = []  # valaszok listaja nyomtatashoz
jelenlegi_oldalszam = 1
jelenlegi_valasz = 1

c = ""
c_elozo = ""

currentlySelected = 0
szoveg_x, szoveg_y = hatter_szoveg_kordinata(stdscr, egyszeru_hatter, 3, 4)
aktiv_karakterlap = False
try:
    while 1:
        # megjeleno elemek
        for i in range(20):
            stdscr.addstr(i, 0, " "*100)
        osz = jelenlegi_oldalszam-1  # a termeszetes oldalszamozas miatt... igy mar tombindex
        nagy_szoveg = sorokra_bont(k.oldalak[osz].szoveg)
        hatter_rajzolasa_kozepre(stdscr, egyszeru_hatter)
        if jelenlegi_oldalszam < 0:
            stdscr.addstr(szoveg_x+6, szoveg_y+36, "A jateknak vege!")
            stdscr.addstr(szoveg_x+8, szoveg_y+29, "A kilepeshez nyomj meg egy gombot!")
            c = stdscr.getch()
            break
        elif aktiv_karakterlap:
            karakterlapot_rajzol(stdscr, foszereplo, szoveg_x, szoveg_y)
        else:
            szoveget_kiir(stdscr, k.oldalak[osz].szoveg, szoveg_x, szoveg_y)
            valasztasokat_kiir(stdscr, k.oldalak[osz].valaszok, szoveg_x+15, szoveg_y, jelenlegi_valasz)
        if debug_mode:
            l_i = 1
            debug_text = "[n]<<oldal>>[m]"
            stdscr.addstr(l_i, 2, debug_text)
            l_i += 1
            debug_text = "oldal: " + str(jelenlegi_oldalszam)
            stdscr.addstr(l_i, 2, debug_text)
            l_i += 1
            debug_text = "valasz: " + str(jelenlegi_valasz)
            stdscr.addstr(l_i, 2, debug_text)
            l_i -= 1
            debug_text = "a jelenlegi valasz:"
            stdscr.addstr(l_i, 20, debug_text)
            if len(k.oldalak[osz].valaszok) < 1:
                l_i += 1
                debug_text = "   ezen az oldalon nincsenek valaszlehetosegek"
                stdscr.addstr(l_i, 20, debug_text)
            else:
                l_i += 1
                debug_text = "   ide vezet: " + str(k.oldalak[osz].valaszok[jelenlegi_valasz-1].celoldal)
                stdscr.addstr(l_i, 20, debug_text)
                l_i += 1
                debug_text = "   lathato, ha van: " + str(k.oldalak[osz].valaszok[jelenlegi_valasz-1].feltetel_ha_van)
                stdscr.addstr(l_i, 20, debug_text)
                l_i += 1
                debug_text = "   lathato, ha nincs: " + str(k.oldalak[osz].valaszok[jelenlegi_valasz-1].feltetel_ha_nincs)
                stdscr.addstr(l_i, 20, debug_text)
                l_i += 1

        # akciok kiadasa
        c = stdscr.getch()
        # exit program
        if c == ord('q') or c == ord('Q'):
            break  # Exit the while()

        # navigating the menu
        elif c == curses.KEY_UP:
            jelenlegi_valasz = ertekvaltoztato(jelenlegi_valasz, -1, len(k.oldalak[osz].valaszok))
        elif c == curses.KEY_DOWN:
            jelenlegi_valasz = ertekvaltoztato(jelenlegi_valasz, +1, len(k.oldalak[osz].valaszok))
        elif c == curses.KEY_LEFT:
            pass
        elif c == curses.KEY_RIGHT:
            pass
        elif c == ord('\n'):
            jelenlegi_oldalszam = k.oldalak[osz].valaszok[jelenlegi_valasz-1].celoldal
            jelenlegi_valasz = 1

        # karakterlap
        elif c == ord('c') or c == ord('C'):
            aktiv_karakterlap = not aktiv_karakterlap

        elif debug_mode:
            if c == ord('n') or c == ord('N'):
                jelenlegi_oldalszam = ertekvaltoztato(jelenlegi_oldalszam, -1, len(k.oldalak))
                jelenlegi_valasz = 1
            elif c == ord('m') or c == ord('M'):
                jelenlegi_oldalszam = ertekvaltoztato(jelenlegi_oldalszam, +1, len(k.oldalak))
                jelenlegi_valasz = 1

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

# ez itt lent csak peldak ezkoztara
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
