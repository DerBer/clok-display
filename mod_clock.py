# -*- coding: utf-8 -*-
from datetime import datetime

class TimeModule:
	# update interval (seconds)
	interval = 1.0
	
	def __init__(self, font):
		self.font = font
	
	def update(self, disp, x, y, w, h):
		#disp.clear()
		#disp.plot(0, 0, 2); disp.plot(1, 0, 2); disp.plot(0, 1, 2)
		#disp.plot(63, 0, 2); disp.plot(62, 0, 2); disp.plot(63, 1, 2)
		#disp.plot(0, 15, 2); disp.plot(1, 15, 2); disp.plot(0, 14, 2)
		#disp.plot(63, 15, 2); disp.plot(62, 15, 2); disp.plot(63, 14, 2)
		t = datetime.now()
		x = disp.putstr(x, y, t.strftime("%H"), self.font, 1, 0) + 2
		x = disp.putstr(x, y, t.strftime("%M"), self.font, 1, 0) + 2
		x = disp.putstr(x, y, t.strftime("%S"), self.font, 1, 0)

#class DateModule:
