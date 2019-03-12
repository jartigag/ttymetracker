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

echo "1. instalando el plugin vim-logbook (también podría obtenerse con vim-plug,
añadiendo:

call plug#begin('~/.vim/plugged')
Plug 'jartigag/vim-logbook'
call plug#end()

al fichero ~/.vimrc y ejecutando \":PlugInstall\" en vim)
"
mkdir -p ~/.vim ~/.vim/plugged ~/.vim/plugged/vim-logbook
cp install/vim-logbook/* ~/.vim/plugged/vim-logbook/

echo '2. añadiendo algunos alias de bash útiles: "lb" y "tmt"..'
echo "
lb() {
	vim $logbookDir/$(date '+%Y-%m-%d').md
}
tmtl () {
	python3 $PWD/ttymetracker.py $logbookDir
}
tmt () {
	python3 $PWD/ttymetracker.py $logbookDir -m todo-list
}
" | tee -a ~/.bash_aliases > /dev/null

echo "3. se incluirá algún fichero logbook de ejemplo.."
echo "
$(date)
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

$(date --date="+3 minutes")
---
> [ ] Seguir usando logbook
" > $logbookDir/$(date '+%Y-%m-%d').md
echo "$logbookDir/$(date '+%Y-%m-%d').md"
echo "(puedes sobreescribir este fichero luego)"

echo ''
echo 'hecho! pruébalo escribiendo "tmt" en tu terminal (primero recarga tus alias de bash ejecutando ". ~/.bashrc")'
