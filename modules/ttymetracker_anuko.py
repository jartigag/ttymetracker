#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ##########
# # ttymetracker: terminal time tracker
# ##########
#
# this module for ttymetracker copies your tasks to your instance of
# Anuko, the TimeTracker system
#
# usage: python3 ttymetracker.py logbooksDir --modules anuko

__author__ = "@jartigag"
__version__ = "0.4"

#TODO1: ttytracker_aliases.cfg: a config json that matches shortcuts with anuko projects and clients.
#                               for example: 
#                               for example: [{"shorcut": "soporteSamsung", "project": "I_207_SAMSUNG_19_Soporte_19", "client": "Samsung"}, {"shorcut": "devSamsung", ...}]
#                                            └── #soporteSamsung = I_207_SAMSUNG_19_Soporte_19 @ Samsung | #devSamsung = I_208_SAMSUNG_19_Desarrollo_19 @ Samsung
#
#TODO2: open a commit.tmp file in vim before posting data to anuko

from bs4 import BeautifulSoup
import urllib.request
import ssl
from ttymetracker_credentials import *
import json
from datetime import datetime
import os

ssl._create_default_https_context = ssl._create_unverified_context

def commit_today(logbooksDir, round_time_to_quarter_hour=False):
    try:
        today_short = datetime.now().strftime("%Y-%m-%d")
        today_file = "{}/{}.md".format(logbooksDir, today_short)
        with open(today_file) as f, open("commit.tmp","w") as c:
            c.write('''## Revisa tu registro de hoy {} antes de publicarlo en Anuko. Las líneas que empiezan
## con '##' serán ignoradas.\n
##~ Elimina esta línea para confirmar la publicación de este registro ~##\n\n'''.format(today_short))
            c.write("## DESDE - HASTA   | NOTA\n")
            lines = f.readlines()
            time = '09:00:00'
            for line in lines:
                i = lines.index(line)
                if i==len(lines)-1: break
                if lines[i+1]=='---\n': # if this line it's a timestamp:
                    if lines[i+2][0]=='>':    # if there's a note on this timestamp:
                        previous_time = time #TODO: optional argument to round time to quarter of an hour
                        time = ''.join( line.split(' ')[4] ) # line.split(' ')[4] takes something like '09:17:43'
                        c.write("{} - {}: {}".format(previous_time, time, lines[i+2][2:]))
        os.system("vim commit.tmp")
    except IOError as e:
        print("error: {}".format(e))

def push_note(start, end, project, client, task, note):
    r = urllib.request.Request(anuko_url, headers=anuko_cookie)
    print('{} - {} | project: {}, client: {}, task: {}, note: {}'.format(start, end, project, client, task, note))
    #WIP

def push_today(aliasesFile):
    print("\033[1m[[ notas del registro de HOY {} para publicar en Anuko: ]]\033[0m\n".format(datetime.now().strftime("%Y-%m-%d")))
    try:
        aliases = []
        if aliasesFile:
            aliases = json.load( open(aliasesFile) )
        with open("commit.tmp") as f:
            lines = f.readlines()
            project, client, task = '', '', ''
            for line in lines:
                line = line.rstrip() # remove '\n'
                if line=='##~ Elimina esta línea para confirmar la publicación de este registro ~##':
                    print('acción cancelada (porque la línea \'##~ ~##\' no fue eliminada)')
                    os.system("rm commit.tmp")
                    sys.exit()
                elif line=='' or line[:2]=='##':
                    continue
                for alias in aliases:
                    if "#{}".format(alias['shorcut']) in line:
                        project = alias['project']
                        client = alias['client']
                        task = alias['task']
                # from '16:00:00 - 17:00:00: [x] depurar Líneas Base',
                start = line.split(' - ')[0]   # it takes 16:00:00
                end = line.split(' - ')[1][:8] # it takes 17:00:00
                note = line[21:]               # it takes '[x] depurar Líneas Base'
                push_note(start, end, project, client, task, note)
        os.system("rm commit.tmp")
    except IOError as e:
        print("error: {}".format(e))

r = urllib.request.Request(anuko_url, headers=anuko_cookie)

html = urllib.request.urlopen(r).read()
soup = BeautifulSoup(html, 'html.parser')

clients = soup.findAll( lambda x: x.name=='option' and x.parent.attrs.get('name')=='client')
projects = soup.findAll( lambda x: x.name=='option' and x.parent.attrs.get('name')=='project')
tasks = soup.findAll( lambda x: x.name=='option' and x.parent.attrs.get('name')=='task')

'''
POST /timetracker/time.php HTTP/1.1
Host: localhost:8889
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://localhost:8889/timetracker/time.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 122
Connection: close
Cookie: tt_PHPSESSID=o99vjfr7ussbthrllp01jsk2v0; tt_login=jartiga
Upgrade-Insecure-Requests: 1

client=1&project=6&task=1&start=9%3A00&finish=13%3A30&date=2019-03-19&note=nota&btn_submit=Submit&browser_today=2019-03-19
'''
