#!/usr/bin/env python

import os
import time
import curses
import curses.ascii



def init_colors():
  curses.start_color()
  curses.use_default_colors()
  
  curses.init_pair(1, curses.COLOR_WHITE, -1)
  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_CYAN)
  curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)


def make_titlebar():
  """
  Create title bar
  
  The title bar has a simple decorative and help purpose
  """
  win = curses.newwin(1, curses.COLS, 0, 0)
  
  win.bkgdset(ord(' '), curses.color_pair(2))
  win.insertln()
  win.addstr(0, 1, 'RTMilk')

  return win
  

def make_statusbar():
  """
  Create status bar
  
  The status bar lists available channels
  """
  win = curses.newwin(1, curses.COLS, curses.LINES-2, 0)
  
  win.bkgdset(ord(' '), curses.color_pair(2))
  win.insertln()
  win.addstr(0, 1, '(connected) [1] overview [2] work [3] system')

  return win



def make_inputbar():
  """
  Create input bar
  """
  win = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
  
  win.bkgdset(ord(' '), curses.color_pair(1))
  win.insertln()
  win.addstr('[channel] ')
  
  win.nodelay(0)
  win.timeout(0)
  
  curses.curs_set(1)
  
  return win

def make_contentwin():
  win = curses.newwin(curses.LINES-5, curses.COLS, 1, 0)
  
  win.bkgdset(ord(' '), curses.color_pair(1))
  win.insertln()

  return win
  
def main(stdscr):
  init_colors()
  
  # titlebar
  titlebar_win = make_titlebar()
  titlebar_win.refresh()
  
  # content window
  content_win = make_contentwin()
  content_win.refresh()
  
  # statusbar
  statusbar_win = make_statusbar()
  statusbar_win.refresh()
  
  # inputbar
  inputbar_win = make_inputbar()
  inputbar_win.refresh()  
  
  # main input buffer
  input_buffer = ""
  
  while True:
    # move to own thread
    time.sleep(0.01)
    ch = inputbar_win.getch()
    
    if(-1 == ch):
      continue
    elif(curses.ascii.isprint(ch)):
      inputbar_win.addch(chr(ch))
      input_buffer += chr(ch)
    elif ch == curses.KEY_BACKSPACE or ch == curses.ascii.BS or ch == curses.ascii.DEL:
      inputbar_win.delch(inputbar_win.getyx()[0], inputbar_win.getyx()[1]-1)
      input_buffer = input_buffer[:-1]
    elif ch == curses.KEY_UP or ch == curses.ascii.DLE:
      inputbar_win.addstr("<KEY_UP>")
    elif ch == curses.ascii.TAB:
      inputbar_win.addstr("<TAB>")
    elif ch == curses.ascii.NAK:  #CTRL+U
      inputbar_win.addstr("<CTRL+U>")
    elif ch == curses.ascii.ESC:
      inputbar_win.addstr("<ESC>")
    elif ch == curses.ascii.NL or ch == curses.KEY_ENTER:
      inputbar_win.erase()
      inputbar_win.addstr('[channel] ')
      
      input_buffer += "\n"
      content_win.addstr(input_buffer)
      content_win.refresh()
      
      input_buffer = ""
    elif curses.ascii.isctrl(ch):
      inputbar_win.addstr("<CTRL> %d [%s]" % (ch, curses.unctrl(ch)))
        
    inputbar_win.refresh()
  
  time.sleep(8)



if __name__ == '__main__':
  curses.wrapper(main)
