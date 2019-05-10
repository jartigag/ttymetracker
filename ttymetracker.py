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
# usage: python3 ttymetracker.py logbooksDir --modules [todo-list anuko chrono]

__author__ = "@jartigag"
__version__ = "0.5"

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

import os, sys
import re
import argparse
from modules.ttymetracker_todo_list import load_lists, print_list, mark_as_completed, session_event
from modules.ttymetracker_anuko import commit_today, push_today
from ttymetracker_credentials import *
from time import sleep

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
    parser.add_argument('-m','--modules',choices=['todo-list','anuko'],default='',
        help='funcionalidades que se van a cargar')
    parser.add_argument('-a','--aliasesFile',
            help='fichero JSON (.cfg) que asocia #etiquetas con clientes-proyectos-tareas')
    args = parser.parse_args()
    logbooksDir = args.logbooksDir
    if logbooksDir.endswith('/'): logbooksDir=logbooksDir[:-1]
    aliasesFile = args.aliasesFile
    try:
        while True:
            try:
                logbooks = sorted([f for f in os.listdir(logbooksDir) if re.match(r'[0-9]+.*\.md', f)])
            except FileNotFoundError:
                print('"{}" no existe'.format(logbooksDir))
                print("\ntaluego!")
                sys.exit(-1)
            load_files(args.list)
            if 'todo-list' in args.modules:
                todos, dones = load_lists(logbooks, logbooksDir)
                print_list(todos, dones)
                opt = input("Marcar como completada la tarea nº: ")
                try:
                    if int(opt)<len(todos) and int(opt)>=0: # that is, `opt` is a valid index of `todos`
                        mark_as_completed(int(opt), todos, logbooksDir)
                        print("La tarea {}:\n\t\033[1m{}\033[0m\nse ha marcado como completada\n".format(opt,todos[int(opt)]))
                        todos, dones = load_lists(logbooks, logbooksDir)
                        load_files()
                    else:
                        raise ValueError
                except ValueError:
                    if opt=='s':
                        session_event(logbooksDir, "start")
                        print("\033[1mSesión iniciada\033[0m")
                    elif opt=='S':
                        session_event(logbooksDir, "end")
                        print("\033[1mSesión terminada\033[0m")
                    elif opt=='':
                        pass
                    else:
                        print("\033[91m[!]\033[0m número inválido")
                    print("\033[1mRecargando..\033[0m")
                    sleep(0.5)
            elif 'anuko' in args.modules:
                commit_today(logbooksDir, aliasesFile)
                push_today(aliasesFile)
                opt = input("¿Abrir Anuko para revisar estas entradas en el navegador? [S/n] ")
                if opt=='' or opt.lower()=='s':
                    os.system("xdg-open {}".format(anuko_url))
    except KeyboardInterrupt:
        print("\ntaluego!")
        sys.exit(0)
    except Exception:
        print("\ntaluego!")
        sys.exit()
