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

ssl._create_default_https_context = ssl._create_unverified_context

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
