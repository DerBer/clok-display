#!/usr/bin/python3
# -*- coding: utf-8 -*-

import httplib
import xml.etree.ElementTree as ET
import datetime

data_providers = [
        {
                'host' : 'www.sportal.de',
                'path' : '/emessage/fixtures/%s/buli1_Spieltag_%s.xml' # %s is replaced by season and match_day
        },
        {
                'host' : 'www.sportal.de',
                'path' : '/emessage/fixtures/%s/buli2_Spieltag_%s.xml'
        }
]

MATCH_STATUS_RUNNING = 1
MATCH_STATUS_BREAK = 2
MATCH_STATUS_FINISHED = 3
MATCH_STATUS_NOT_YET_STARTED = 4
MATCH_STATUS_UNKNOWN = 0xff

# color codes
COL_BLACK  = 0
COL_GREEN  = 1
COL_RED    = 2
COL_ORANGE = 3
COL_TRANSPARENT = 0xff

# mapping match status to color code
color_mapping = { MATCH_STATUS_RUNNING : COL_RED, MATCH_STATUS_BREAK : COL_ORANGE, MATCH_STATUS_FINISHED : COL_GREEN, MATCH_STATUS_NOT_YET_STARTED : COL_GREEN }
status_mapping = { 'FIRSTHALF' : MATCH_STATUS_RUNNING, 'SECONDHALF' : MATCH_STATUS_RUNNING, 'BREAK' : MATCH_STATUS_BREAK, 'PRE' : MATCH_STATUS_NOT_YET_STARTED, 'FIN' : MATCH_STATUS_FINISHED}

class BundesligaModule:
        # update interval (seconds)
        interval = 1.0

        def __init__(self, font, time_per_match):
                self.font = font
                self.format = format
                self.updated_match_day = datetime.date.today() - datetime.timedelta(days = 1)
                self.updated = datetime.datetime.now() - datetime.timedelta(days = 1)
                self.match_day = [0] * len(data_providers)
                self.current_matches = [False] * len(data_providers)
                self.match_list = []
                self.time_per_match = time_per_match
  
        def init_match_day(self):
                # Determine (guess) the current season
                today = datetime.date.today()
                self.updated_match_day = today
                if (today.month < 7):
                        baseyear = today.year - 1
                else:
                        baseyear = today.year
                self.season = '%s%s' % (baseyear % 100, (baseyear + 1) % 100)
                # Perform binary search to find the current match day
                for (provno,provider) in enumerate(data_providers):
                        min = 0
                        max = 34
                        while (max >= min):
                                mid = (min + max) // 2
                                xmlroot = fetch_xml_data(provider['host'], provider['path'] %(self.season,mid))
                                for fixture in xmlroot.findall('FIXTURE'):
                                        start = datetime.date(*map(int,fixture.get('START').split('-')))
                                        end = datetime.date(*map(int,fixture.get('END').split('-')))
                                        if start > today:
                                                max = mid - 1
                                                break
                                        if end < today:
                                                min = mid + 1
                                                break
                                else:
                                        print('Match day is %s' %mid)
                                        self.match_day[provno] = mid
                                        self.current_matches[provno] = True
                                        break
                        else:
                                print('No match day, next one is %s' %min)
                                self.match_day[provno] = min
                                self.current_matches[provno] = False
                                return min
        
        def init_match_list(self):
                if self.updated_match_day != datetime.date.today():
                        self.init_match_day()
#                if not True in self.current_matches and self.updated.date() == datetime.date.today():
#                        return
                match_list = []
                for (provno,provider) in enumerate(data_providers):
                        xmlroot = fetch_xml_data(provider['host'],provider['path'] % (self.season, self.match_day[provno]))
                        for fixture in xmlroot.findall('FIXTURE'):
                                for match in fixture.findall('MATCH'):
                                        result=['',0,'',0,0]
                                        for team in match.findall('TEAM'):
                                                if team.get('side') == 'HOME':
                                                        result[0] = team.find('NAME_3').text
                                                        result[1] = int(team.find('FULLTIME').text)
                                                else:
                                                        result[2] = team.find('NAME_3').text
                                                        result[3] = int(team.find('FULLTIME').text)
                                        result[4] = status_mapping.get(match.get('currentstatus'),MATCH_STATUS_UNKNOWN)
                                        match_list.append(tuple(result))
                self.updated = datetime.datetime.now()
                match_list.sort(key=(lambda x: x[4]))
                self.match_list = match_list

        def update(self, disp, x, y, w, h):
                if self.updated < datetime.datetime.now() - datetime.timedelta(seconds = 30):
                        self.init_match_list()
                current_match = self.match_list[(getMillisecondsSince1970() % (9 * self.time_per_match)) // self.time_per_match]
                disp.putstr_metric(x, y, u'{0} {1} : {3} {2} '.format(*current_match) + (' ' * 10), self.font, color_mapping.get(current_match[4],COL_GREEN), COL_BLACK)

# helper functions

def fetch_xml_data(host, path):
        connection = httplib.HTTPConnection(host)
        connection.request('GET',path)
        response = connection.getresponse()
        if response.status != 200:
                print('Fehler %s' % response.status)
                return None
        xmldata = response.read()
        root = ET.fromstring(xmldata)
        return root

def getMillisecondsSince1970():
        now = datetime.datetime.now()
        return int(now.strftime('%s'))*1000+now.microsecond/1000
