# -*- coding: utf-8 -*-
from datetime import datetime

class TimeModule:
	# update interval (seconds)
	interval = 1.0
	
	def update(self, disp, x, y):
		#disp.clear()
		#disp.plot(0, 0, 2); disp.plot(1, 0, 2); disp.plot(0, 1, 2)
		#disp.plot(63, 0, 2); disp.plot(62, 0, 2); disp.plot(63, 1, 2)
		#disp.plot(0, 15, 2); disp.plot(1, 15, 2); disp.plot(0, 14, 2)
		#disp.plot(63, 15, 2); disp.plot(62, 15, 2); disp.plot(63, 14, 2)
		t = datetime.now()
		#print t
		font = disp.font7x12
		#y = 2
		#x = 5
		x = disp.putstr(x, y, t.strftime("%H"), font, 1, 0) + 4
		x = disp.putstr(x, y, t.strftime("%M"), font, 1, 0) + 4
		x = disp.putstr(x, y, t.strftime("%S"), font, 1, 0)
		disp.sendframe()
