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

class Pacman:
	def __init__(self, scr, mscr):
		self.scr = scr
		self.mscr = mscr
		Y, X = self.scr.getmaxyx()
		self.X, self.Y = X-2, Y-2-1
		
	def statusline(self, str):
		stdscr_y, stdscr_x = self.mscr.getmaxyx()
		menu_y = (stdscr_y-3)-1
		try:
			self.mscr.addstr(menu_y+1, 4, " "*len(self.statuslinestr))
		except:
			pass
		self.statuslinestr = str
		self.mscr.addstr(menu_y+1, 4, str)
		return 0
		
	def display_credits(self):
		self.statusline('')
		self.scr.addstr(0,0,"COPYRIGHT")
		self.scr.addstr(1,5,"Copyright 2010 geeks' factory <www.geeksfactory.de>")
		self.scr.addstr(3,0,"DEVELOPMENT")
		self.scr.addstr(4,5,"Raphael Michel <pacman@raphaelmichel.de>")
		self.scr.addstr(6,0,"LICENSE")
		self.scr.addstr(7,5,"pacman.py is licensed under the terms of the GNU General Public license")
		self.scr.addstr(9,0,"THANKS")
		self.scr.addstr(10,5,"to kiwi11000 for the idea ;-)")
		self.scr.refresh()
