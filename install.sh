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

logbookDir="$PWD/$1"
mkdir -p $logbookDir

echo "vamos a instalar ttymetracker!"
echo "1. instalando el plugin vim-logbook (también podría obtenerse con vim-plug,
añadiendo:

call plug#begin('~/.vim/plugged')
Plug 'jartigag/vim-logbook'
call plug#end()

al fichero ~/.vimrc y ejecutando \":PlugInstall\" en vim)
"
mkdir -p ~/.vim ~/.vim/plugged ~/.vim/plugged/vim-logbook ~/.vim/plugged/vim-logbook/autoload ~/.vim/plugged/vim-logbook/doc ~/.vim/plugged/vim-logbook/plugin
echo "
\"\"
\" Open today's logbook in the current buffer
function! logbook#Execute()
        let logfile = \"~/logbook/\" . strftime(\"%F\") . \".md\"
        execute \"edit \" . logfile
endfunction

\"\"
\" Insert a timestamp under the cursor
function! logbook#Timestamp()
        execute \"normal! GA\n\n\" . strftime(\"%c\") . \"\n---\n\<ESC>\"
endfunction
" >> ~/.vim/plugged/vim-logbook/autoload/logbook.vim

echo "
\"\"
\" Open today's logbook in the current buffer
command! -nargs=0 Lb call logbook#Execute()

\"\"
\" Insert a timestamp under the cursor
command! -nargs=0 Ts call logbook#Timestamp()
" >> ~/.vim/plugged/vim-logbook/plugin/logbook.vim

echo "
:Lb     vim-logbook.txt /*:Lb*
:Ts     vim-logbook.txt /*:Ts*
vim-logbook     vim-logbook.txt /*vim-logbook*
vim-logbook-commands    vim-logbook.txt /*vim-logbook-commands*
vim-logbook-contents    vim-logbook.txt /*vim-logbook-contents*
vim-logbook.txt vim-logbook.txt /*vim-logbook.txt*
" >> ~/.vim/plugged/vim-logbook/doc/tags

echo "
*vim-logbook.txt*
                                                                 *vim-logbook*

==============================================================================
CONTENTS                                                *vim-logbook-contents*
  1. Commands...........................................|vim-logbook-commands|

==============================================================================
COMMANDS                                                *vim-logbook-commands*

:Lb                                                                      *:Lb*
  Open today's logbook in the current buffer

:Ts                                                                      *:Ts*
  Insert a timestamp under the cursor


vim:tw=78:ts=8:ft=help:norl:
" > ~/.vim/plugged/vim-logbook/doc/vim-logbook.txt

echo "
# vim-logbook

vim-logbook is a minimalist vim plugin which makes keeping a programming logbook
easier. I find that keeping a logbook improves my learning, debugging and focus.

I've [blogged about keeping a
logbook](https://routley.io/tech/2017/11/23/logbook.html), and I highly
recommend [Peter Lyons](https://peterlyons.com/)' [article on the same
topic](https://peterlyons.com/leveling-up#your-work-journal).

vim-logbook assumes the following structure:
- Each day's logs are stored in a separate file, stored at
  \`~/logbook/yyyy-mm-dd.md\`
- Each logbook entry is marked with a timestamp

## Commands

vim-logbook implements two commands:
- \`:Lb\` - open today's logbook in the current buffer
- \`:Ts\` - insert a timestamp under the cursor

## Example log file

\`\`\`markdown
Tue 23 Jan 23:24:00 2018
- TODO:
- Write README for vim-logbook
- Write help doc for vim-logbook

Tue 23 Jan 23:27:57 2018
- Vim help doc guidelines can be found with \`:help help-writing\`
- http://stevelosh.com/blog/2011/09/writing-vim-plugins/#write-a-vim-help-document

Tue 23 Jan 23:38:55 2018
- Updated vim-logbook readme with logbook example
\`\`\`

## Install

vim-logbook can be installed with your favourite plugin manager.

- [vim-plug](https://github.com/junegunn/vim-plug):
        1. Add \`Plug 'jamesroutley/vim-logbook'\` to your \`.vimrc\`
        2. Run \`:PlugInstall\`
" >> ~/.vim/plugged/vim-logbook/README.md

echo "
Copyright 2018 James Routley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
" >> ~/.vim/plugged/vim-logbook/LICENSE.txt

echo '2. añadiendo algunos alias de bash útiles: "lb" y "tmt"..'
echo "
lb() {
	vim $logbookDir/$(date '+%Y-%m-%d').md
}
tmt () {
	python3 $logbookDir/ttymetracker/ttymetracker.py $logbookDir -m todo-list
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
