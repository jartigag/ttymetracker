#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ##########
# # ttymetracker: terminal time tracker
# ##########
#
# this module for ttymetracker prints a todo-list and allows to mark
# pending tasks as completed, registering it on your logbook.
#
# usage: python3 ttymetracker.py logbooksDir --modules todo-list

__author__ = "@jartigag"
__version__ = "1.0"

import os
from datetime import datetime

'''
Ejemplo de tarea con un TO-DO:

lun 04 mar 2019 15:05:54 CET
---
> [ ] Probar líneas base en el nuevo dashboard
'''

# let's avoid locale issues, at least spanish ones 😇:
months_dict = {'ene':'01', 'feb':'02', 'mar':'03', 'abr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'ago': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'}
weekdays_dict = {'0': 'dom', '1':'lun', '2': 'mar', '3': 'mié', '4': 'jue', '5': 'vie', '6': 'sáb'}

def load_lists(logbooks, logbooksDir):
    todos = []
    dones = []
    for lb in logbooks:
        try:
            with open('{}/{}'.format(logbooksDir,lb)) as f:
                lines = f.readlines()
                day = ''
                for line in lines:
                    i = lines.index(line)
                    day = ''.join( line.split(':')[0][:-2] ) # line.split(':')[0][:-2] takes something like 'lun 04 mar 2019 '
                    if i==len(lines)-1: break
                    if lines[i+1]=='---\n': # if this line it's a timestamp:
                        if lines[i+2][0]=='>':    # if there's a note on this timestamp:
                            if '[ ]' in lines[i+2]:
                                lin=lines[i+2] # just for readability
                                task = '{} ( desde {})'.format(lin[lin.index('['):][:-1],day) # from '[ ] one task\n', it takes 'one task'
                                todos.append(task)
                            elif '[x]' in lines[i+2]:
                                lin=lines[i+2] # just for readability
                                task = lin[lin.index('['):][:-1] # from '[x] one finished task\n', it takes 'one finished task'
                                dones.append(task)
        except IOError:
            continue
    return todos, dones

def print_list(todos, dones):
    print("\033[1m[[ lista de TO-DOs: ]]\033[0m\n")
    for t in todos: print("{}.{}".format(todos.index(t),t))
    print("*****")
    print("{} tareas completadas".format(len(dones)))

def mark_as_completed(i, todos, logbooksDir):
    #1. take date of the task
    task_date = todos[i].split('( desde ')[1][4:-2] # from '( desde vie 08 mar 2019 )', it takes '08 mar 2019'
    task_file = "{}/{}-{}-{}.md".format(logbooksDir, task_date.split()[2], months_dict[task_date.split()[1]], task_date.split()[0]) #year-num_month-day.md

    #2. open logbook of that date and a temp outfile to write on
    with open(task_file) as inf, open("{}.tmp".format(task_file),"w") as outf:
        for line in inf.readlines(): 
            if todos[i].split(' ( desde ')[0] in line:

            #3. overwrite '[ ] that task' with '[-] that task'
                outf.write(line.replace('[ ]', '[-]'))
            else:
                outf.write(line)
    os.system("mv {}.tmp {}".format(task_file, task_file)) # this overwrites the old task_file with the new version

    #4. write on today's logbook: '[x] that task'
    today = datetime.now().strftime("%Y %m %d %w %H %M %S")
    today_file = "{}/{}-{}-{}.md".format(logbooksDir, today.split()[0], today.split()[1], today.split()[2])
    with open(today_file, "a") as f:
        timestamp = "\n{} {} {} {} {}:{}:{} CET\n---\n".format(
            weekdays_dict[today.split()[3]], today.split()[2],
            list(months_dict.keys())[list(months_dict.values()).index(today.split()[1])], # what a hack to get a key by its value in a dict, huh? 😜
            today.split()[0], today.split()[4], today.split()[5], today.split()[6]
        )
        # timestamp is something like:
        #
        #vie 09 mar 2019 15:28:01 CET
        #---
        f.write(timestamp)
        f.write("> [x] {}\n".format(todos[i][4:].split(" ( desde")[0])) # from '[ ] Tarea de prueba ( desde vie 09 mar 2019 )', it takes 'Tarea de prueba'

def session_event(logbooksDir, event):
    today = datetime.now().strftime("%Y %m %d %w %H %M %S")
    today_file = "{}/{}-{}-{}.md".format(logbooksDir, today.split()[0], today.split()[1], today.split()[2])
    with open(today_file, "a") as f:
        timestamp = "\n{} {} {} {} {}:{}:{} CET\n---\n".format(
            weekdays_dict[today.split()[3]], today.split()[2],
            list(months_dict.keys())[list(months_dict.values()).index(today.split()[1])], # what a hack to get a key by its value in a dict, huh? 😜
            today.split()[0], today.split()[4], today.split()[5], today.split()[6]
        )
        # timestamp is something like:
        #
        #vie 09 mar 2019 15:28:01 CET
        #---
        f.write(timestamp)
        if event=="start":
            f.write("> Inicio de sesión\n")
        elif event=="end":
            f.write("> Fin de sesión\n")
        elif event=="start_pause":
            f.write("> Inicio pausa\n")
        elif event=="end_pause":
            f.write("> Fin pausa\n")
