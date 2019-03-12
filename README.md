# ttymetracker

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
```

### `vim-logbook`, huh?
this tools use the [vim-logbook](https://github.com/jamesroutley/vim-logbook) system, explained in its readme and in a [blogpost](https://routley.io/tech/2017/11/23/logbook.html).  
[i forked it](https://github.com/jartigag/vim-logbook) and tweaked it a little bit.

**vim-logbook** just helps you to log your activity in [.md](https://en.wikipedia.org/wiki/Markdown) files, like this:
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
so **ttymetracker** prints all your .md files in a specific logbook/ directory.  
for example, along with its `todo-list` module, it would look like that:
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
so you can know at a glance which tasks you've spent time on,  
and easily mark pending tasks as completed (that action will also be registered on your logbook).
