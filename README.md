# ~$ ttymetracker

just a simple command-line tool that will help you to track your time  
and manage your pending and completed tasks.

## /content:

- [vim-logbook, huh?](#vim-logbook-huh)
- [ttymetracker, huh?](#ttymetracker-huh)

---------

```
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
```

### `vim-logbook`, huh?
this tool uses the [vim-logbook](https://github.com/jamesroutley/vim-logbook) system by [james routley](https://routley.io/), explained on his project's readme and on his [blogpost](https://routley.io/tech/2017/11/23/logbook.html).  
[i forked it](https://github.com/jartigag/vim-logbook) and tweaked it a little.

**vim-logbook** simply helps you to log your activity in [.md](https://en.wikipedia.org/wiki/Markdown) files, like this:
```
lun 04 mar 2019 15:05:54 CET
---
> Correcciones en las gráficas del dashboard "Consumo de memoria"

lun 04 mar 2019 15:40:02 CET
---
> Reunión con el equipo de Madrid y [ ] depurar los scripts que nos han pasado

- Faltan implementar las últimas funciones
- Habrá dos parámetros en el JSON de config:
        * Desde cuándo cortar
        * Hasta cuándo cortar
- Meter en crontab

lun 04 mar 2019 16:59:34 CET
---
> Completada la actualización de las bases de datos

En local (habiendo hecho `git clone` del repo de la herramienta y luego dentro de un `virtualenv`),
` ` `
python update.py
python tool.py --regenerate_databases
` ` `
```

### `ttymetracker`, huh?
**ttymetracker** prints all your .md files from a specific logbook/ directory.  
there are several modules which load different features.  
for example, along with ttymetracker's `todo-list` module, it would look like that:
```
$ python3 ttymetracker.py -m todo-list ~/logbook
=====

lun 04 mar 2019
---------------

15:05:54 > Correcciones en las gráficas del dashboard "Consumo de memoria"

15:40:02 > Reunión con el equipo de Madrid y [ ] depurar los scripts que nos han pasado

16:59:34 > Completada la actualización de las bases de datos

[[ lista de TO-DOs: ]]

0.[ ] depurar los scripts que nos han pasado
*****
13 tareas completadas
Marcar como completada la tarea nº: 
```
so now you can know at a glance when did you do any task and how much did it take you.  
in addition, you can easily mark pending tasks as completed (that action will also be registered on your logbook).
