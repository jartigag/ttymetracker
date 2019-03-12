""
" Open today's logbook in the current buffer
function! logbook#Execute()
	let logfile = "~/logbook/" . strftime("%F") . ".md"
	execute "edit " . logfile
endfunction

""
" Insert a timestamp under the cursor
function! logbook#Timestamp()
	execute "normal! GA\n\n" . strftime("%c") . "\n---\n\<ESC>"
endfunction


