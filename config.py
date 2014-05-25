# -*- coding: utf-8 -*-

from mod_clock import TimeModule
from mod_clock import DateModule
from mod_clock import DateModuleVertical
from mod_clock import SecondBarModule
from mod_weather import WeatherModule
from mod_weather import WeatherModuleColored
from mod_anniversary import AnniversaryModule

# location settings
CITY = 'Münster'
COUNTRY = 'DE'

# display settings
NUM_PANELS = 2

# color codes
COL_BLACK  = 0
COL_GREEN  = 1
COL_RED    = 2
COL_ORANGE = 3

# calendar settings
# Note: you will need a file 'mod_anniversary_credentials.dat' that
# can be created using an external script by logging into your google
# account and permitting mod_anniversary access to your calendar.
# The module also needs the google calendar api to be installed.
# This can usually be done by running
#
#   easy_install --upgrade google-api-python-client

CALENDARS = [
  {
    'name' : '*',
    'id' : 'someid@group.calendar.google.com',
    'font' : (lambda disp: disp.font4x6)
  },
  {
    'name' : 'Jahrestag',
    'id' : 'someotherid@group.calendar.google.com',
    'font' : (lambda disp: disp.font4x6)
  }
]

SCREENS = [
	{
		# display rotation (multiples of 90° clockwise)
		'rotation': 0,
		# screen configuration
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font7x8num, COL_GREEN), 'x': 16, 'y': 0, 'w': 46, 'h': 8  },
			{ 'moduleFn': lambda disp: SecondBarModule(COL_RED, COL_BLACK, 5, COL_ORANGE, 3), 'x': 0, 'y': 9, 'w': 64, 'h': 1  },
			{ 'moduleFn': lambda disp: DateModule(disp.font4x5num, COL_GREEN), 'x': -1, 'y': 11, 'w': 46, 'h': 5  },
			{ 'moduleFn': lambda disp: WeatherModule(CITY, COUNTRY, COL_ORANGE), 'x': 47, 'y': 11, 'w': 17, 'h': 5  },
		]
	},
	{
		'rotation': 0,
		# screen configuration
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font7x8num, COL_GREEN), 'x': 16, 'y': 0, 'w': 31, 'h': 8  },
			{ 'moduleFn': lambda disp: DateModuleVertical(disp.font3x4num, COL_GREEN), 'x': 0, 'y': 0, 'w': 16, 'h': 10  },
			{ 'moduleFn': lambda disp: WeatherModuleColored(CITY, COUNTRY), 'x': 47, 'y': 0, 'w': 17, 'h': 5  },
			{ 'moduleFn': lambda disp: AnniversaryModule(disp.font4x6, COL_GREEN, 100, CALENDARS), 'x': 0, 'y': 10, 'w': 64, 'h': 6  },
		]
	},
	{
		'rotation': 0,
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font12x16, COL_GREEN), 'x': 5, 'y': 1, 'w': 53, 'h': 15  },
		]
	},
	{
		'rotation': 1,
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font8x12, COL_ORANGE, "%H"), 'x': 1, 'y': 0, 'w': 15, 'h': 12  },
			{ 'moduleFn': lambda disp: TimeModule(disp.font8x12, COL_ORANGE, "%M"), 'x': 1, 'y': 12, 'w': 15, 'h': 12  },
			{ 'moduleFn': lambda disp: TimeModule(disp.font8x12, COL_GREEN, "%S"), 'x': 1, 'y': 24, 'w': 15, 'h': 12  },
			{ 'moduleFn': lambda disp: WeatherModule(CITY, COUNTRY, COL_RED), 'x': -1, 'y': 48, 'w': 17, 'h': 5  },
		]
	},
	{
		# display rotation (multiples of 90° clockwise)
		'rotation': 2,
		# screen configuration
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font7x8num, COL_GREEN), 'x': 16, 'y': 0, 'w': 46, 'h': 8  },
			{ 'moduleFn': lambda disp: SecondBarModule(COL_RED, COL_BLACK, 5, COL_ORANGE, 3), 'x': 0, 'y': 9, 'w': 64, 'h': 1  },
			{ 'moduleFn': lambda disp: DateModule(disp.font4x5num, COL_GREEN), 'x': -1, 'y': 11, 'w': 46, 'h': 5  },
			{ 'moduleFn': lambda disp: WeatherModule(CITY, COUNTRY, COL_ORANGE), 'x': 47, 'y': 11, 'w': 17, 'h': 5  },
		]
	},
]
