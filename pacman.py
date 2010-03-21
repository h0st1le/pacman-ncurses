#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pacman.py
#       
#       Copyright 2010 Raphael Michel <webmaster@raphaelmichel.de>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import curses

class Pacman:
	def __init__(self, scr, mscr):
		# make them global
		self.scr = scr
		self.mscr = mscr
		Y, X = self.scr.getmaxyx()
		self.X, self.Y = X-2, Y-2-1
		self.running = False
		
		# initialisation
		self.game = []
		self.empty = self.game
		self.gaming = False
		self.positions = {'pacman' : (16,13), 'blinky' : (None, None), 'pinky' : (None, None), 'inky' : (None, None), 'clyde' : (None, None) }
			# coordinates in format (y,x) !!!
		
		# colors initialisation
		curses.init_pair(1, curses.COLOR_YELLOW, 0)
		curses.init_pair(2, curses.COLOR_RED, 0)
		curses.init_pair(3, curses.COLOR_MAGENTA, 0)
		curses.init_pair(4, curses.COLOR_CYAN, 0)
		curses.init_pair(5, curses.COLOR_GREEN, 0)
		
		# instructions
		self.scr.erase()
		self.scr.addstr(0,0,u"""Welcome to pacman-curses, the python-powered pacman game in plain text.
ELEMENTS
  \u25A0  borders
  C  is your game figure
  \u00b7  dots to eat
  \u2639  the ghosts
  \u25c3\u25b9 teleporters
  \u25cc  home of the ghosts
KEYS
  arrow  keys to move
  S/R    start a new game
  O      show and edit some options
  H      show highscores
  C      show credits
  Q      quit game
  P      pause game
  B      return to game""".encode("utf-8"))
		self.scr.refresh()
		
	def back(self):
		# return to the game window after viewing for example the credits
		self.draw_game(self.game)
		
	def display_mainmenu(self, stdscr=None, menu_y = None):
		if menu_y == None:
			stdscr_y, stdscr_x = self.mscr.getmaxyx()
			menu_y = (stdscr_y-2)-1
		if stdscr == None:
			stdscr = self.mscr
		stdscr.addstr(menu_y, 4,'P)ause/Resume, R)estart Game, O)ptions, H)ighscores, C)redits, Q)uit')
		
	def display_startmenu(self, stdscr=None, menu_y = None):
		if menu_y == None:
			stdscr_y, stdscr_x = self.mscr.getmaxyx()
			menu_y = (stdscr_y-2)-1
		if stdscr == None:
			stdscr = self.mscr
		stdscr.addstr(menu_y, 4,'S)tart Game, O)ptions, H)ighscores, C)redits, Q)uit')
		
	def display_menu(self, stdscr=None, menu_y = None):
		if menu_y == None:
			stdscr_y, stdscr_x = self.mscr.getmaxyx()
			menu_y = (stdscr_y-2)-1
		if stdscr == None:
			stdscr = self.mscr
		stdscr.addstr(menu_y, 4,'B)ack to game, O)ptions, H)ighscores, C)redits, Q)uit')
		
	def pause_game(self):
		if not self.gaming: return False
		self.running = False
		
	def resume_game(self):
		if not self.gaming: return False
		self.running = True
		
	def toggle_pause(self):
		if not self.gaming: return False
		if self.running == False: self.running = True
		else: self.running = False
		
	def draw_game(self, field):
		if field == []:
			self.statusline('ERROR: Press R to start a game', 2)
			return False
		# draws the field
		self.scr.erase()
		y = 0
		x = 0
		try:
			for _x in field:
				for val in _x:
					drawn = None
					if val == False:
						char = u'\u25A0'.encode("utf-8")
						self.scr.addstr(y,x,char)
					elif val == '*':
						char = u'\u25cc'.encode("utf-8")
						self.scr.addstr(y,x,char)
					elif val == '<':
						char = u'\u25c3'.encode("utf-8")
						self.scr.addstr(y,x,char)
					elif val == '>':
						char = u'\u25b9'.encode("utf-8")
						self.scr.addstr(y,x,char)
					elif val == None:
						char = u'\u00b7'.encode("utf-8")
						self.scr.addstr(y,x,char)
					elif val == 'C':
						char = 'C'.encode("utf-8")
						self.scr.addstr(y,x,char,curses.color_pair(1))
					elif val == 'b':
						char = u'\u2639'.encode("utf-8")
						self.scr.addstr(y,x,char,curses.color_pair(2))
					elif val == 'p':
						char = u'\u2639'.encode("utf-8")
						self.scr.addstr(y,x,char,curses.color_pair(3))
					elif val == 'i':
						char = u'\u2639'.encode("utf-8")
						self.scr.addstr(y,x,char,curses.color_pair(4))
					elif val == 'c':
						char = u'\u2639'.encode("utf-8")
						self.scr.addstr(y,x,char,curses.color_pair(5))
					x += 1
				y += 1
				x = 0
		except curses.error:
			self.statusline('ERROR: Terminal too small?', 2)
		
		self.display_mainmenu()
		self.scr.refresh()
		
	def start_game(self, fieldfile):
		# reset and read file
		self.scr.erase()
		field = open(fieldfile, 'r').read().strip()
		self.game = []
		tmp = []
		self.gaming = True
		
		# lines
		y = 0
		x = 0
		try:
			for char in field:
				arr = char
				if char == 'X':
					arr = False
				elif char == 'v':
					arr = None
				elif char == '.':
					arr = None
				elif char == ' ':
					arr = ' '
				elif char == 'C':
					arr = 'C'
					pac = (y,x)
				elif ord(char) == 10 or ord(char) == 13:
					y += 1
					x = 0
					self.game.append(tmp)
					tmp = []
					continue
				tmp.append(arr)
				x += 1
		except:
			self.statusline('ERROR: Terminal too small?', 2)
			
		# Last line
		y += 1
		x = 0
		self.game.append(tmp)
		tmp = []
		self.empty = self.game
			
		# to small?
		if self.Y < len(self.game) or self.X < len(self.game[0]):
			self.scr.erase()
			self.scr.addstr(0,0,'ERROR: Terminal too small!',curses.color_pair(2))
			self.display_menu()
			self.scr.refresh()
			return False
			
		self.maxX = len(self.game[0])-1
		self.maxY = len(self.game)-1
			
		# draw!
		self.positions = {'pacman' : pac, 'blinky' : (None, None), 'pinky' : (None, None), 'inky' : (None, None), 'clyde' : (None, None) }
		
		self.draw_game(self.game)
		
	def getempty(self, y, x):
		# get original value of a field
		empty = self.empty[y][x]
		if empty in ('C', 'b', 'p', 'i', 'c'):
			empty = None
		return empty
			
		
	def move(self, key):
		# person hits a key ;)
		if not self.gaming: return False
		
		# key handlers
		if key == curses.KEY_LEFT:
			oldpos = self.positions['pacman']
			newpos = (oldpos[0], oldpos[1]-1)
		elif key == curses.KEY_RIGHT:
			oldpos = self.positions['pacman']
			newpos = (oldpos[0], oldpos[1]+1)
		elif key == curses.KEY_UP:
			oldpos = self.positions['pacman']
			newpos = (oldpos[0]-1, oldpos[1])
		elif key == curses.KEY_DOWN:
			oldpos = self.positions['pacman']
			newpos = (oldpos[0]+1, oldpos[1])
		else:
			return False
			
		# teleporters
		if self.empty[newpos[0]][newpos[1]] == '<':
			newpos = (oldpos[0], self.maxX-1)
		elif self.empty[newpos[0]][newpos[1]] == '>':
			newpos = (oldpos[0], 1)
			
		# a free field?
		if self.empty[newpos[0]][newpos[1]] in (None, ' '):
			self.game[oldpos[0]][oldpos[1]] = self.getempty(oldpos[0], oldpos[1])
			self.game[newpos[0]][newpos[1]] = 'C'
			self.positions['pacman'] = newpos
		
		self.draw_game(self.game)
			
		
	def statusline(self, str, col = None):
		stdscr_y, stdscr_x = self.mscr.getmaxyx()
		menu_y = (stdscr_y-2)-1
		try:
			if col == None:
				self.mscr.addstr(menu_y+1, 4, " "*len(self.statuslinestr))
			else:
				self.mscr.addstr(menu_y+1, 4, " "*len(self.statuslinestr), curses.color_pair(col))				
		except:
			pass
		self.statuslinestr = str
		self.mscr.addstr(menu_y+1, 4, str)
		return 0
		
	def display_credits(self):
		self.pause_game()
		self.scr.erase()
		self.statusline('')
		self.scr.addstr(0,0,"""COPYRIGHT
  Copyright 2010 geeks' factory <www.geeksfactory.de>
	
DEVELOPMENT
  Raphael Michel <pacman@raphaelmichel.de>
	
LICENSE
  pacman-ncurses is licensed under the terms of the GNU General Public license
	
THANKS
  to kiwi11000 for the idea ;-)""")
		self.display_menu()
		self.scr.refresh()
