# -*- coding: utf-8 -*-
from datetime import datetime

DAY_NAME = ("MO", "DI", "MI", "DO", "FR", "SA", "SO")


class TimeModule:
	# update interval (seconds)
	interval = 1.0
	
	def __init__(self, font, col, format = "%H:%M"):
		self.font = font
		self.col = col
		self.format = format
	
	def update(self, disp, x, y, w, h):
		t = datetime.now()
		putsSpecial(disp, self.font, x, y, t.strftime(self.format), self.col, 0)


class DateModule:
	# update interval (seconds)
	interval = 1.0
	
	def __init__(self, font, col):
		self.font = font
		self.col = col
	
	def update(self, disp, x, y, w, h):
		t = datetime.now()
		s = DAY_NAME[t.weekday()] + " " + t.strftime("%d.%m.%Y")
		putsSpecial(disp, self.font, x, y, s, self.col, 0)


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

def putsSpecial(disp, font, x, y, s, col, bg):
	fontH = disp.fontheight(font)
	fontW = disp.fontwidth(font)
	if (fontH <= 6): # small fonts
		for c in s:
			if c == ' ':
				x += 1
			elif c == '.':
				disp.plot(x + 1, y + fontH - 1, col)
				x += 2
			elif c == ':':
				disp.plot(x + 1, y + 1, col)
				disp.plot(x + 1, y + fontH - 2, col)
				x += 2
			else:
				x = disp.putchar(x, y, c, font, col, bg)
	else: # large fonts
		for c in s:
			if c == ' ':
				x += 2
			elif c == '.':
				disp.box(x + 1, y + fontH - 2, x + 2, y + fontH - 1, col)
				x += 2
			elif c == ':':
				vpos = fontH / 5
				x += fontW / 10
				disp.box(x + 1, y + vpos, x + 2, y + vpos + 1, col)
				disp.box(x + 1, y + fontH - vpos - 2, x + 2, y + fontH - vpos - 1, col)
				x += 3 + fontW / 10
			else:
				x = disp.putchar(x, y, c, font, col, bg)
	return x
