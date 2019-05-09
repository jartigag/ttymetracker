#!/bin/bash
# -*- coding: utf-8 -*-
#author: @jartigag
#date: 10/03/2019
#version: 0.2
#
# install ttymetracker, the terminal time tracker
# usage: bash install.sh logbookDir

# check if logbookDir is provided:
if [[ $# -eq 0 ]] ; then
    echo 'usage: bash install.sh logbookDir'
    exit 1
fi

if [[ "$1"==/* ]]; then # if $1 it's an absolute path
    logbookDir=$1
else
    logbookDir="$PWD/$1"
fi
mkdir -p $logbookDir

echo "vamos a instalar ttymetracker!"

echo "1. instalando el plugin vim-logbook"

echo "
call plug#begin('~/.vim/plugged')
Plug 'jartigag/vim-logbook'
call plug#end()
" >> ~/.vimrc

mkdir -p ~/.vim ~/.vim/plugged ~/.vim/plugged/vim-logbook
cp -r install/vim-logbook/* ~/.vim/plugged/vim-logbook/

echo '2. añadiendo algunos alias de bash útiles: "lb" y "tmt"..'
echo "
lb() {
    vim $logbookDir/$(date '+%Y-%m-%d').md
}
tmt () {
    echo -ne "\033]30;tmt ⏱\007"
    python3 $PWD/ttymetracker.py $logbookDir -m todo-list
}
tmtl () {
    echo -ne "\033]30;tmtl ⏱L\007"
    python3 ~/ttymetracker/ttymetracker.py $logbookDir -l
}
tmta () {
    echo -ne "\033]30;tmta ⏱🡅\007"
    python3 $PWD/ttymetracker.py $logbookDir -m anuko -a ~/ttymetracker/ttymetracker_aliases.cfg
}
" | tee -a ~/.bash_aliases > /dev/null

echo "3. se incluirá algún fichero logbook de ejemplo.."
echo "
$(date +%c)
---
> Tu primera entrada

Aquí va una descripción más detallada de lo que has hecho en la
primera entrada de tu logbook. Quizás quieras usar **negrita**, [enlaces](https://jartigag.xyz),
\`\`\`
if youWant==True:
    print(\"fragmentos de código\")
\`\`\`
o cualquier otro de los recursos que permite [Markdown](https://es.wikipedia.org/wiki/Markdown), el lenguaje de marcado ligero ;)

Puedes abrir en vim el logbook de hoy ejecutando \"lb\" desde la terminal,
y añadir la fecha y hora actual para empezar una nueva entrada con \":Ts\" desde vim.

$(date +%c --date="+3 minutes")
---
> [ ] Seguir usando logbook
" > $logbookDir/$(date '+%Y-%m-%d').md
echo "$logbookDir/$(date '+%Y-%m-%d').md"
echo "(puedes sobreescribir este fichero luego)"

echo ''
echo 'hecho! pruébalo escribiendo "tmt" en tu terminal (primero recarga tus alias de bash ejecutando ". ~/.bashrc")'
