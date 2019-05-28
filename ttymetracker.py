#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ##########
# # ttymetracker: terminal time tracker
# ##########
#
# basically a script to list the tasks you wrote down in your logbook directory
# and manage them with some modules, like the todo-list one.
#
# usage: python3 ttymetracker.py logbooksDir --modules [todo-list anuko sharepoint]

__author__ = "@jartigag"
__version__ = "0.6"

#changelog:
#
# -- v0.2 --:
# * --modules todo-list
#
# -- v0.3 --:
# * modularization
# * exit gracefully
# * install.sh
#
# -- v0.4 --:
# * --list
# * --modules anuko
# * --aliasesFile
#
# -- v0.5 --:
# * start/stop session from todo-list
# * while True
#
# -- v0.6 --:
# * --modules sharepoint
# * pause session from todo-list
#
# -- v0.7 --:
# * --git

import os, sys
import re
import argparse
from modules.ttymetracker_todo_list import load_lists, print_list, mark_as_completed, session_event
import modules.ttymetracker_anuko
import modules.ttymetracker_sharepoint
from ttymetracker_credentials import *
from time import sleep
from datetime import datetime
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

'''
Ejemplo de tarea:

lun 04 mar 2019 15:05:54 CET
---
> Correcciones en las gráficas de amazonDashboard
'''

def load_files(listFormat):
    for lb in logbooks:
        try:
            with open('{}/{}'.format(logbooksDir,lb)) as f:
                lines = f.readlines()
                day = ''
                for line in lines:
                    i = lines.index(line)
                    if i==len(lines)-1: break
                    if lines[i+1]=='---\n': # if this line it's a timestamp:
                        if lines[i+2][0]=='>':    # if there's a note on this timestamp:
                            actual_day = ''.join( line.split(':')[0][:-2] ) # line.split(':')[0][:-2] takes something like 'lun 04 mar 2019 '
                            if actual_day!=day:
                                day = actual_day
                                if not listFormat:
                                    if day[:3]=='lun':
                                        print("=====\n")
                                    print('\033[4m{}\033[0m'.format(day))
                            timestamp = ':'.join([ line.split(':')[0][-2:], line.split(':')[1], line.split(':')[2][:2] ]) # this takes something like '10:23:01'
                        if not listFormat:
                            print('{}{}'.format(timestamp,lines[i+2])) # print timestamp and note
                        else:
                            print('{}- {}{}'.format(day,timestamp,lines[i+2])) # print day, timestamp and note
        except IOError:
            continue

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="imprime una lista con tus tareas, para que puedas gestionarlas fácilmente. v{} por {}".format(__version__, __author__))
    parser.add_argument('logbooksDir')
    parser.add_argument('-l','--list',action='store_true',
        help='imprimir lista en formato plano')
    parser.add_argument('-m','--modules',choices=['todo-list','anuko','sharepoint'],default='',
        help='funcionalidades que se van a cargar')
    parser.add_argument('-a','--aliasesFile',
            help='fichero JSON (.cfg) que asocia #etiquetas con clientes-proyectos-tareas')
    parser.add_argument('-g','--git',
            help='')
    args = parser.parse_args()
    logbooksDir = args.logbooksDir
    if logbooksDir.endswith('/'): logbooksDir=logbooksDir[:-1]
    aliasesFile = args.aliasesFile
    try:
        logbooks = sorted([f for f in os.listdir(logbooksDir) if re.match(r'[0-9]+.*\.md', f)])
        load_files(args.list)
        if args.git:
            #WIP: `cd args.logbook`
            os.chdir(args.logbook)
            #WIP: if not .git/:
            if not os.path.isdir('.git'):
                os.system("git init && git remote add origin {}".format(git_remoteURL))
                os.system("git fetch --all && ( git checkout {0} 2>/dev/null || git checkout -b {0} ) && git pull origin {0}".format(git_userBranch)) #create branch if not exists https://stackoverflow.com/a/35683029
            #WIP: if gitconfig local != ($git_config_name & $git_config_email): gitconfig local
            git_localName = os.popen('git config --local user.name').read().strip()
            git_localEmail = os.popen('git config --local user.email').read().strip()
            if git_configName!=git_localName or git_configEmail!=git_localEmail:
                #WIP: git_config_local()
                pass
        if 'todo-list' in args.modules:
            while True:
                todos, dones = load_lists(logbooks, logbooksDir)
                print_list(todos, dones)
                opt = input("Marcar como completada la tarea nº: ")
                try:
                    if int(opt)<len(todos) and int(opt)>=0: # that is, `opt` is a valid index of `todos`
                        mark_as_completed(int(opt), todos, logbooksDir)
                        print("La tarea {}:\n\t\033[1m{}\033[0m\nse ha marcado como completada\n".format(opt,todos[int(opt)]))
                        todos, dones = load_lists(logbooks, logbooksDir)
                        load_files(args.list)
                    else:
                        raise ValueError
                except ValueError:
                    if opt=='s':
                        session_event(logbooksDir, "start")
                        print("\033[1mSesión iniciada\033[0m")
                    elif opt=='S':
                        session_event(logbooksDir, "end")
                        print("\033[1mSesión terminada\033[0m")
                    elif opt=='p':
                        session_event(logbooksDir, "start_pause")
                        print("\033[1mInicio pausa\033[0m")
                    elif opt=='P':
                        session_event(logbooksDir, "end_pause")
                        print("\033[1mFin pausa\033[0m")
                    elif opt=='':
                        pass
                    else:
                        print("\033[91m[!]\033[0m número inválido")
                        continue
                    print("\033[1mRecargando..\033[0m")
                    sleep(0.5)
                    load_files(args.list)
        elif 'anuko' or 'sharepoint' in args.modules:
            if 'anuko' in args.modules:
                modules.ttymetracker_anuko.commit_today(logbooksDir, aliasesFile)
                modules.ttymetracker_anuko.push_today(aliasesFile)
                opt = input("¿Abrir Anuko para revisar estas entradas en el navegador? [S/n] ")
                if opt=='' or opt.lower()=='s':
                    os.system("xdg-open '{}'".format(anuko_url))
            elif 'sharepoint' in args.modules:
                ctxAuth = AuthenticationContext(sharepoint_url)
                if ctxAuth.acquire_token_for_user(sharepoint_username, sharepoint_password):
                    ctx = ClientContext(sharepoint_url, ctxAuth)
                    modules.ttymetracker_sharepoint.commit_today(logbooksDir, aliasesFile)
                    modules.ttymetracker_sharepoint.push_today(ctx, aliasesFile)
                    opt = input("¿Abrir Sharepoint para revisar estas entradas en el navegador? [S/n] ")
                    if opt=='' or opt.lower()=='s':
                        os.system("xdg-open '{}'".format(sharepoint_check_url))
                else:
                    print(ctxAuth.get_last_error())
            if args.git:
                #WIP: `git add .; git commit -m "{} #{}".format(today, numOfCommit); git push origin master`
                today_short = datetime.now().strftime("%Y-%m-%d")
                os.chdir(args.logbook)
                os.system("git add .; git commit -m '{}'; git push origin {}".format(today_short,git_userBranch))
    except FileNotFoundError:
        print("\033[91m[!]\033[0m {} no existe".format(logbooksDir))
    except KeyboardInterrupt:
        print("\ntaluego!")
    except Exception as e:
        print("\033[91m[!]\033[0m {}".format(e))
