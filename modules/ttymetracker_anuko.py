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

# ttytracker_aliases.cfg: a config json that matches shortcuts with anuko projects and clients.
#                         for example:
#                         for example: [{"shorcut": "soporteSamsung", "project": "I_207_SAMSUNG_19_Soporte_19", "client": "Samsung"}, {"shorcut": "devSamsung", ...}]
#                                       └── #soporteSamsung = I_207_SAMSUNG_19_Soporte_19 @ Samsung | #devSamsung = I_208_SAMSUNG_19_Desarrollo_19 @ Samsung
#

from bs4 import BeautifulSoup
import urllib.request, urllib.parse
import ssl
from ttymetracker_credentials import *
import json
from datetime import datetime
import os
import sys

ssl._create_default_https_context = ssl._create_unverified_context

def commit_today(logbooksDir, aliasesFile, round_time_to_quarter_hour=False):
    try:
        today_short = datetime.now().strftime("%Y-%m-%d")
        today_file = "{}/{}.md".format(logbooksDir, today_short)
        with open(today_file) as f, open("commit.tmp","w") as c:
            c.write("## Revisa tu registro de hoy {} antes de publicarlo en Anuko.\n## Las líneas que empiezan con '##' serán ignoradas.\n".format(today_short))
            if aliasesFile: c.write("##\n## Las notas con #etiquetas configuradas en {} se completarán con sus datos correspondientes.\n".format(aliasesFile))
            c.write('\n##~ Elimina esta línea para confirmar la publicación de este registro ~##\n\n')
            c.write("## DESDE - HASTA   | NOTA\n")
            lines = f.readlines()
            time = '09:00'
            for line in lines:
                i = lines.index(line)
                if i==len(lines)-1: break
                if lines[i+1]=='---\n': # if this line it's a timestamp:
                    if lines[i+2][0]=='>': # if there's a note on this timestamp:
                        #TODO: optional argument to round time to quarter of an hour. possible implementations:
                        #   1 - use dictionaries https://superuser.com/a/102359
                        #           set dictionary+=~/ttymetracker/modules/dict_round_time.txt
                        #   2 - use regex and commands http://vim.1045645.n5.nabble.com/rounding-numbers-td3339491.html
                        #           :%s/.../\=float2nr(round(str2float(substitute(submatch(1), ',', '.', '')))) # this rounds decimals
                        # in vim:
                        #           :range s[ubstitute]/pattern/string
                        # so here:
                        #           %              = the whole file. The same as 1,$
                        #           /.../          = /pattern/
                        #           \=float2nr(..) = string
                        previous_time = time
                        time = ''.join( line.split(' ')[4][:-3] ) # line.split(' ')[4] takes something like '09:17'
                        c.write("{} - {}: {}".format(previous_time, time, lines[i+2][2:]))
        os.system("vim commit.tmp")
    except IOError as e:
        print("\033[91m[!]\033[0m error: {}".format(e))

def push_note(start, end, project, client, task, note):
    try:
        r = urllib.request.Request(anuko_url, headers=anuko_cookie)
        print('[post] {} - {} {} | {} | project: {}, client: {}, task: {}'.format(start, end, datetime.now().strftime("%Y-%m-%d"), note, project, client, task))
        html = urllib.request.urlopen(r).read()
        soup = BeautifulSoup(html, 'html.parser')
        post_data = 'client={}&project={}&task={}&start={}&finish={}&date={}&note={}&btn_submit=Submit'.format(
                    client, project, task, start.replace(':','%3A'), end.replace(':','%3A'), datetime.now().strftime("%Y-%m-%d"), urllib.parse.quote(note)
                ).encode('utf8')
        req = urllib.request.Request(anuko_url, headers=anuko_headers, data=post_data)
        ans = urllib.request.urlopen(req)
    except IOError as e:
        print("\033[91m[!]\033[0m error: {}".format(e))

def push_today(aliasesFile):
    print("\033[1m[[ notas del registro de HOY {} para publicar en Anuko: ]]\033[0m\n".format(datetime.now().strftime("%Y-%m-%d")))
    try:
        aliases = []
        if aliasesFile:
            aliases = json.load( open(aliasesFile) )
        with open("commit.tmp") as f:
            lines = f.readlines()
            for line in lines:
                project, client, task = '""', '""', '""'
                line = line.rstrip() # remove '\n'
                if line=='##~ Elimina esta línea para confirmar la publicación de este registro ~##':
                    print('acción cancelada (porque la línea \'##~ ~##\' no fue eliminada)')
                    os.system("rm commit.tmp")
                    sys.exit()
                elif line=='' or line[:2]=='##':
                    continue
                for alias in aliases:
                    if "#{}".format(alias['shorcut']) in line.lower():
                        if 'project' in alias: project = alias['project']['value']
                        if 'client' in alias:  client = alias['client']['value']
                        if 'task' in alias:    task = alias['task']['value']
                # from '16:00:00 - 17:00:00: [x] depurar Líneas Base',
                start = line.split(' - ')[0]   # it takes 16:00
                end = line.split(' - ')[1][:5] # it takes 17:00
                note = line[15:]               # it takes '[x] depurar Líneas Base'
                push_note(start, end, project, client, task, note)
        os.system("rm commit.tmp")
    except Exception as e:
        print("\033[91m[!]\033[0m error: {}".format(e))
