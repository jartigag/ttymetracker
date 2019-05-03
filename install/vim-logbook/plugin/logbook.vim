""
" Open today's logbook in the current buffer
command! -nargs=0 Lb call logbook#Execute()

""
" Insert a timestamp under the cursor
command! -nargs=0 Ts call logbook#Timestamp()

""
" Round time to quarter-hour (example: 00:17 -> 00:15)
command! -nargs=0 Round %s#:\d\d#\=":".15*(submatch(0)[1:]/15)#g | %s/:0/:00/g
