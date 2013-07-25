# -*- coding: utf-8 -*-
from datetime import datetime

DAY_NAME = ("MO", "DI", "MI", "DO", "FR", "SA", "SO")


class TimeModule:
	# update interval (seconds)
	interval = 1.0
	
	def __init__(self, col):
		self.col = col
	
	def update(self, disp, x, y, w, h):
		t = datetime.now()
		putsSpecialLarge(disp, x, y, t.strftime("%H:%M"), self.col, 0)
		#x = disp.putstr(x, y, t.strftime("%H"), font, self.col, 0)
		#disp.box(x + 1, y + 1, x + 2, y + 2, 1)
		#disp.box(x + 1, y + 5, x + 2, y + 6, 1)
		#x += 3
		#x = disp.putstr(x, y, t.strftime("%M"), font, self.col, 0)
		#x = disp.putstr(x, y, t.strftime("%S"), font, 1, 0)


class DateModule:
	# update interval (seconds)
	interval = 1.0
	
	def __init__(self, col):
		self.col = col
	
	def update(self, disp, x, y, w, h):
		t = datetime.now()
		s = DAY_NAME[t.weekday()] + " " + t.strftime("%d.%m.%Y")
		putsSpecialSmall(disp, x, y, s, self.col, 0)


class SecondBarModule:
	# update interval (seconds)
	interval = 1.0
	
	def __init__(self, colBar, colMarker, markerWidth, colMarker2 = 0, markerWidth2 = 0):
		self.colBar = colBar
		self.colMarker = colMarker
		self.colMarker2 = colMarker2
		self.markerWidth = markerWidth
		self.markerWidth2 = markerWidth2
	
	def update(self, disp, x, y, w, h):
		disp.box(x, y, x + w - 1, y + h - 1, self.colBar)
		now = datetime.now()
		pos = now.second * (w - self.markerWidth) / 59
		disp.box(pos, y, pos + self.markerWidth - 1, y + h - 1, self.colMarker)
		if self.markerWidth2 > 0:
			pos2 = pos + (self.markerWidth - self.markerWidth2) / 2
			disp.box(pos2, y, pos2 + self.markerWidth2 - 1, y + h - 1, self.colMarker2)


# helper functions

def putsSpecialLarge(disp, x, y, s, col, bg):
	font = disp.font7x8num
	for c in s:
		if c == '.':
			disp.box(x + 1, y + 6, x + 2, y + 7, col)
			x += 2
		elif c == ':':
			disp.box(x + 1, y + 1, x + 2, y + 2, col)
			disp.box(x + 1, y + 5, x + 2, y + 6, col)
			x += 3
		else:
			x = disp.putchar(x, y, c, font, col, bg)
	return x

def putsSpecialSmall(disp, x, y, s, col, bg):
	font = disp.font4x5num
	for c in s:
		if c == ' ':
			x += 1
		elif c == '.':
			disp.plot(x + 1, y + 4, col)
			x += 2
		elif c == ':':
			disp.plot(x + 1, y + 1, col)
			disp.plot(x + 1, y + 3, col)
			x += 2
		else:
			x = disp.putchar(x, y, c, font, col, bg)
	return x
