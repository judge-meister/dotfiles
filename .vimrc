"
" .vimrc file
"_______________


" enable syntax highlighting, duh
:syntax enable

" set the current working folder to the same as the file shown
"		useful for then entering clearcase commands or using
"		% to get the current file and it works
:autocmd BufEnter * cd %:p:h

autocmd FileType yaml setlocal ai ts=2 sw=2 et
autocmd BufWritePre *.py :%s/\s\+$//e

" set the coloUr scheme
colorscheme pablo
set bg=dark
:hi Normal guibg=NONE ctermbg=NONE

" set the line numbering colours
:hi linenr guifg=grey guibg=black

" set the font and size
":set guifont=Monospace\ 9

" incrementally search
:set incsearch

:map <F1> :noh<CR>
:map <F9> :vertical wincmd f<CR>
		
:map <F12> :r! date<CR>
:map <C-T> :tabnew<CR>
:map <F11> :set noexpandtab<CR>:setlocal list<CR>:set listchars=tab:>~,trail:.<CR>

" paste from system '+' clipboard buffer
:map <c-v> "+P

" make return indent to the same as previous line
:set autoindent
:set smartindent

" only search case sensitive for something containing uppercase letters
:set smartcase
:set ignorecase
:set showmatch

" turn tabs into spaces
:set expandtab

" show line numbers
:set number

" set the indenting amount (for >> and <<)
:set shiftwidth=4

" set the tab amount
:set tabstop=4

:set wildmenu

:set scrolloff=2
:set guioptions=aegimrL
set hlsearch

autocmd! bufwritepost .vimrc source ~/.vimrc

" always show the line number and column width
:set ruler

" be able to use the mouse in the terminal
if has('mouse')
  :set mouse=a
endif

" execute a command for all buffers ther are shown in windows
fun! AllWindows(cmnd)
	let cmnd = a:cmnd
	let origw = winnr()
	let i = 1
	while (i <= bufnr(*$))
		if bufexists(i)
			let w = bufwinnr(i)
			if w != -1
				echo "=== window: " . w . " files " . bufname(i)
				execute "normal \<c-w>" . w . "w"
				execute cmnd
			endif
		endif
		let i = i+1
	endwhile
	execute "normal \<c-w>" . origw . "w"
endfun

" Adding those quotes is pretty boring. That is easy to fix. Just make a command like
command! -nargs=+ -complete=command AllBuf call AllWindows(<q-args>)


" Added 20/02/14 - for moving lines up and down using Alt+direction key, useful for re-ordering lists

nnoremap <A-j> :m .+1<CR>==
nnoremap <A-k> :m .-2<CR>==
inoremap <A-j> <Esc>:m .+1<CR>==gi
inoremap <A-k> <Esc>:m .-2<CR>==gi
vnoremap <A-j> :m '>+1<CR>gv=gv
vnoremap <A-k> :m '<-2<CR>gv=gv


set cursorline
set laststatus=2

" filetype_sh ------------{{{
augroup filetype_sh
    autocmd!
    autocmd Filetype sh iabbrev <buffer> ifa if<space>[[<space>]];<space>then<cr><cr><bs>fi<cr>
    autocmd Filetype sh iabbrev <buffer> getoptsa while<space>getopts<space":h"<space>opt;<cr>do<cr>case<space>${opt}<space>in<cr><space><space><space><space>h)<cr><space><space><space><space>;;<cr><bs><bs>esac<cr><cr><bs>done<cr>
augroup END
" }}}

" status bar and cursor ------------------ {{{
highlight StatusLine ctermbg=DarkGrey ctermfg=white
augroup statusbar
    autocmd!
    autocmd InsertEnter * highlight StatusLine ctermbg=5
    "autocmd InsertEnter * highlight CursorLine ctermbg=black
    autocmd InsertEnter * highlight FoldColumn ctermbg=5

    autocmd InsertLeave * highlight StatusLine ctermbg=DarkGrey ctermfg=white
    autocmd InsertLeave * highlight CursorLine ctermbg=NONE
    autocmd InsertLeave * highlight FoldColumn ctermbg=DarkGrey
augroup END
" }}}

function! GitBranch()
  return system("git rev-parse --abbrev-ref HEAD 2>/dev/null | tr -d '\n'")
endfunction

function! StatuslineGit()
  let l:branchname = GitBranch()
  return strlen(l:branchname) > 0?'  '.l:branchname.' ':''
endfunction

" switch cursor colour in insert mode, only works in right kind of terminal
if &term =~ "xterm"
    " colour when in insert mode
    let &t_SI = "\<Esc>]12;yellow\x7"
    " colour otherwise
    let &t_EI = "\<Esc>]12;grey\x7"
    " don't know the point of this line
    silent !echo -ne "\033]12;grey\007"
    " revert back to grey
    autocmd VimLeave * silent !echo -ne "\033]112\007"
endif

set statusline=
set statusline+=%{StatuslineGit()}>
set statusline+=\ %f                                                        " file name
"set statusline+=\ [%{strlen(&fenc)?&fenc:'none'},                       " encoding
"set statusline+=%{&ff}]                                                 " file format
set statusline+=\ %Y                                                     " file type
"set statusline+=\ [%{getbufvar(bufnv('%'),'&mod')?'modified':'saved'}]   " modified 
set statusline+=\ %{&modified?'[modified]':'[saved]'}
set statusline+=%r                                                       " read only
set statusline+=\ %=                                                     " right-align
set statusline+=\ Col:\ %c                                               " column number
set statusline+=\ Buf:\ %n                                               " buffer number
set statusline+=\ [%b/0x%B]                                              " ASCII and byte value under cursor
set statusline+=\ %l/%L\ [%p%%]                                          " line x of y [ percentage ]

" }}}

