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
__version__ = "0.2"

#changelog:
#
# -- v0.2 --:
# * TO-DO list
#
# -- v0.3 --:
# * modularization
# * exit gracefully
# * install.sh

import os, sys
import re
import argparse
from modules.ttymetracker_todo_list import load_lists, print_list, mark_as_completed

'''
Ejemplo de tarea:

lun 04 mar 2019 15:05:54 CET
---
> Correcciones en las gráficas de amazonDashboard
'''

def load_files(): 
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
                                if day[:3]=='lun':
                                    print("=====\n")
                                print('\033[4m{}\033[0m'.format(day))
                            timestamp = line[-13:-4] # this takes something like '15:05:54'
                            print('{}{}'.format(timestamp,lines[i+2])) # print timestamp and note
        except IOError:
            continue

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="imprime una lista con tus tareas, para que puedas gestionarlas fácilmente. v%s por %s".format(__version__, __author__))
    parser.add_argument('logbooksDir')
    parser.add_argument('-m','--modules',choices=['todo-list'],default='',
        help='funcionalidades que se van a cargar')
    args = parser.parse_args()
    logbooksDir = args.logbooksDir
    try:
        logbooks = sorted([f for f in os.listdir(logbooksDir) if re.match(r'[0-9]+.*\.md', f)])
    except FileNotFoundError:
        print('"{}" no existe'.format(logbooksDir))
        print("\ntaluego!")
        sys.exit(-1)
    try:
        load_files()
        if 'todo-list' in args.modules:
            todos, dones = load_lists(logbooks, logbooksDir)
            print_list(todos, dones)
            opt = input("Marcar como completada la tarea nº: ")
            while opt!='':
                if int(opt)<len(todos) and int(opt)>=0: # that is, `opt` is a valid index of `todos`
                    mark_as_completed(int(opt), todos, logbooksDir)
                    print("La tarea {}:\n\t\033[1m{}\033[0m\nse ha marcado como completada\n".format(opt,todos[int(opt)]))
                    todos, dones = load_lists(logbooks, logbooksDir)
                    load_files()
                else:
                    print("[\033[91m!\033[0m] número inválido")
                print_list(todos, dones)
                opt = input("Marcar como completada la tarea nº: ")
    except KeyboardInterrupt:
        pass
    finally:
        print("\ntaluego!")
        sys.exit(0)
