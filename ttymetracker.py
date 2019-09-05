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
# usage: python3 ttymetracker.py logbooksDir --modules [todo-list anuko sharepoint] --git --percent --aliasesFile ttymetracker_aliases.cfg

__author__ = "@jartigag"
__version__ = "1.1"

import os, sys
import re
import argparse
from modules.ttymetracker_todo_list import load_lists, print_list, mark_as_completed, mark_as_wip, session_event
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

def load_files(listFormat,percent=False):
    logbooks = sorted([f for f in os.listdir(logbooksDir) if re.match(r'[0-9]+.*\.md', f)])
    if percent: tags = {}
    for lb in logbooks:
        try:
            with open('{}/{}'.format(logbooksDir,lb)) as f:
                lines = f.readlines()
                day = ''
                if percent: time = starting_hour
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
                            if lines[i+2][0]=='> Inicio de sesión\n':
                                time = timestamp[:-3]

                            if percent:
                                previous_time = time
                                time = timestamp[:-3]
                                hours = float("{0:.2f}".format((datetime.strptime(time,"%H:%M") - datetime.strptime(previous_time,"%H:%M")).total_seconds()/3600))
                                if '#' in lines[i+2]:
                                    tag = lines[i+2].split('#')[-1].rsplit(' ')[0]
                                    tag = re.sub(r'[^a-zA-Z ]+', '',tag).lower()
                                    if any(tag==x for x in ['todo','fixme','debug','g']): continue
                                    if tag not in tags.keys(): tags[tag]=0
                                    else: tags[tag]+=hours

                        if not listFormat:
                            print('{}{}'.format(timestamp,lines[i+2])) # print timestamp and note
                        else:
                            print('{}- {}{}'.format(day,timestamp,lines[i+2])) # print day, timestamp and note
        except IOError:
            continue

    if percent:
        total_hours = 0
        tags_sorted_by_value = sorted(tags.items(), key=lambda kv: kv[1])
        for t in tags_sorted_by_value:
            rounded_hours = int(round(t[1]))
            print('{}h\t{}'.format(rounded_hours,t[0]))
            total_hours+=rounded_hours
        print('---')
        print('{}h\ttotal'.format(total_hours))
    return logbooks

def update_git():
    os.chdir(logbooksDir)
    # check if git config is correct:
    git_localName = os.popen("git config --local user.name").read().strip()
    git_localEmail = os.popen("git config --local user.email").read().strip()
    if git_configName!=git_localName or git_configEmail!=git_localEmail:
        print("\033[1m[-]\033[0m Usando las variables de ttymetracker_credentials.py,\nse configurará user.name \"{}\" y user.email \"{}\" para este repositorio de git\n".format(git_configName,git_configEmail))
        os.system("git config user.name '{}'; git config user.email '{}'".format(git_configName,git_configEmail))

    # git push:
    today_short = datetime.now().strftime("%Y-%m-%d")
    os.system("git pull origin master; git add .; git commit -m '{}'; git push origin master".format(today_short))
    print("\n\033[1m[-]\033[0m El repositorio de git {} se ha actualizado\n".format(git_remoteURL))

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
    parser.add_argument('-g','--git',action='store_true',
        help='llevar los .md de cada día en un repositorio git')
    parser.add_argument('-p','--percent',action='store_true',
        help='imprimir el porcentaje de tiempo dedicado a cada #etiqueta')
    args = parser.parse_args()
    logbooksDir = args.logbooksDir
    if logbooksDir.endswith('/'): logbooksDir=logbooksDir[:-1]
    aliasesFile = args.aliasesFile
    try:
        logbooks = load_files(args.list,args.percent)
        if args.git:
            os.chdir(logbooksDir)
            if not os.path.isdir(".git"): #if logbooksDir is not a git directory:
                os.chdir("..")
                os.system("git clone {}".format(git_remoteURL))
                gitDir = git_remoteURL.split('/')[-1].strip('.git') # e.g.: mydoma.in/repos/logbooks-john-doe.git -> logbooks-john-doe
                gitDir = "{}/{}".format("/".join(logbooksDir.split('/')[:-1]),gitDir) # e.g.: /home/user/logbooks-john-doe
                print("\n\033[1mAVISO\033[0m: Para llevar el control de los .md de cada día en el repositorio que se acaba de clonar,\
                        \nla próxima vez se debe ejecutar \033[1mpython3 ttymetracker.py {}\033[0m\n".format(gitDir))
                logbooksDir = gitDir # note that, next time ttymetracker.py will be executed, the arg logbooksDir must be the new directory (which is a git dir),
                                     #  so these lines under `if not os.path.isdir(".git")` won't apply
                update_git()
        if 'todo-list' in args.modules:
            while True:
                logbooks = load_files(args.list,args.percent)
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
                    elif len(opt)>1:
                        if opt[0]=='.':
                            if int(opt[1:])<len(todos) and int(opt[1:])>=0: # `opt` is a valid index of `todos`
                                mark_as_wip(int(opt[1:]), todos, logbooksDir)
                                print("La tarea {}:\n\t\033[1m{}\033[0m\nse ha marcado como 'en progreso'\n".format(opt[1:],todos[int(opt[1:])]))
                                todos, dones = load_lists(logbooks, logbooksDir)
                                load_files(args.list)
                    elif opt=='':
                        pass
                    else:
                        print("\033[91m[!]\033[0m número inválido")
                        sleep(0.5)
                        load_files(args.list)
                        continue
                    print("\033[1mRecargando..\033[0m")
                    sleep(0.5)
                    load_files(args.list)
        if 'anuko' in args.modules:
            modules.ttymetracker_anuko.commit_today(logbooksDir, aliasesFile)
            modules.ttymetracker_anuko.push_today(aliasesFile)
            opt = input("¿Abrir Anuko para revisar estas entradas en el navegador? [S/n] ")
            if opt=='' or opt.lower()=='s':
                os.system("xdg-open '{}'".format(anuko_url))
            if args.git:
                update_git()
        elif 'sharepoint' in args.modules:
            print('Iniciando autenticación en el Sharepoint {}'.format(sharepoint_url))
            ctxAuth = AuthenticationContext(sharepoint_url)
            if ctxAuth.acquire_token_for_user(sharepoint_username, sharepoint_password):
                print('Autenticación válida')
                ctx = ClientContext(sharepoint_url, ctxAuth)
                modules.ttymetracker_sharepoint.commit_today(logbooksDir, aliasesFile)
                modules.ttymetracker_sharepoint.push_today(ctx, aliasesFile)
                opt = input("¿Abrir Sharepoint para revisar estas entradas en el navegador? [S/n] ")
                if opt=='' or opt.lower()=='s':
                    os.system("xdg-open '{}'".format(sharepoint_check_url))
                if args.git:
                    update_git()
            else:
                print('Autenticación fallida')
                print(ctxAuth.get_last_error())
    except KeyboardInterrupt:
        print("\ntaluego!")
    #except Exception as e:
    #    print("\033[91m[!]\033[0m {}".format(e))
