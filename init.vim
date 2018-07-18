call plug#begin()
"Plug 'ternjs/tern_for_vim', { 'for': [ 'javascript', 'html' ] }
Plug 'w0rp/ale', { 'for':[ 'javascript', 'python', 'html', 'sh', 'c', 'cpp', 'vim', 'json', 'yaml', 'lua', 'go' ] }
"Plug 'Valloric/YouCompleteMe', { 'for': [ 'python', 'javascript', 'sh', 'html', 'c', 'cpp', 'vim', 'go' ] }
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'
Plug 'davidhalter/jedi-vim', { 'for': 'python' }
Plug 'jpalardy/vim-slime', { 'for': [ 'python', 'javascript', 'sh', 'lua' ] }
Plug 'junegunn/vim-easy-align', { 'for':[ 'text', 'yaml', 'sh', 'javascript', 'vim' ] }
Plug 'majutsushi/tagbar', { 'for':[ 'python', 'cpp', 'c', 'javascript', 'sh', 'vim', 'lua', 'go' ] }
"Plug 'rhysd/vim-grammarous', { 'for': [ 'text', 'markdown', 'vimwiki' ] }
Plug 'vimwiki/vimwiki'
Plug 'mattn/calendar-vim'
Plug 'xolox/vim-lua-ftplugin', { 'for': 'lua' }
Plug 'xolox/vim-misc', { 'for': 'lua' }
Plug 'rking/ag.vim', { 'for':[ 'javascript', 'python', 'html', 'sh', 'lua', 'c', 'cpp', 'vim', 'text', 'yaml', 'json' ] }
Plug 'mattn/emmet-vim', { 'for': [ 'html', 'javascript' ] }
Plug 'Valloric/ListToggle'
"Plug 'fatih/vim-go', { 'for': 'go'}
"Plug 'Blackrush/vim-gocode', { 'for': 'go'}
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'






call plug#end()


source /etc/vim/vimrc
syntax on
"colorscheme molokai
let mapleader=','
"let g:python3_host_prog = '/root/.virtualenvs/py3/bin/python'
let g:python_host_prog = '/root/.virtualenvs/py2/bin/python'
set nu
noremap <leader>E :qa!<CR>   " Quit all windows
set showcmd
set t_Co=256
"set bg=dark


tnoremap <A-h> <C-\><C-N><C-w>h
tnoremap <A-j> <C-\><C-N><C-w>j
tnoremap <A-k> <C-\><C-N><C-w>k
tnoremap <A-l> <C-\><C-N><C-w>l
inoremap <A-h> <C-\><C-N><C-w>h
inoremap <A-j> <C-\><C-N><C-w>j
inoremap <A-k> <C-\><C-N><C-w>k
inoremap <A-l> <C-\><C-N><C-w>l
nnoremap <A-h> <C-w>h
nnoremap <A-j> <C-w>j
nnoremap <A-k> <C-w>k
nnoremap <A-l> <C-w>l

map \ft :! sdcv <c-r><c-w><CR>
map <leader>dg :VimwikiDiaryGenerateLinks<cr>
map <F9> :w <CR> :%!python <CR>

let g:jedi#goto_command = "<leader>d"
let g:jedi#force_py_version = 2
let g:jedi#goto_assignments_command = "<leader>g"
let g:jedi#goto_definitions_command = ""
let g:jedi#documentation_command = "K"
let g:jedi#usages_command = "<leader>n"
let g:jedi#completions_command = "<leader><tab>"
let g:jedi#rename_command = "<leader>r"
let g:jedi#use_tabs_not_buffers = 0
let g:jedi#use_splits_not_buffers = "right"


let g:jedi#auto_vim_configuration = 0
let g:jedi#smart_auto_mappings = 0
let g:jedi#popup_on_dot = 0
let g:jedi#popup_select_first = 0
let g:jedi#show_call_signatures = 1
let g:jedi#show_call_signatures_delay = 0

let g:pymode_rope = 0



let g:ale_completion_enabled = 1
let g:ale_linters = {'html': ['htmlhint'], 'javascript': ['jshint'], 'css': ['csslint'], 'python': ['flake8'], 'lua': ['luacheck'], 'sh': ['shellcheck'] }

let g:ale_python_flake8_executable = 'python2'   " or 'python' for Python 2
"let g:ale_python_flake8_args = '--ignore=E302'
let g:ale_python_flake8_options = '--ignore=E302,W391,E501,E265,E402,F999,F403,E201,E241,E251,E211,E231,E202,E303,E401,E266,E226,E203'
let g:ale_open_list=0



" Set ultisnips triggers
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<tab>"
let g:UltiSnipsJumpBackwardTrigger="<s-tab>"

"tagbar
nmap <leader>b :TagbarToggle<CR>
let g:tagbar_autofocus = 1

"calendar
"nmap <leader>c :Calendar<CR>

"mouse mode copy/past with system clipboard
set clipboard=unnamedplus
set mouse=a
set fileformat=unix

let g:slime_target = "tmux"
"let g:slime_target = "neovim"


let g:grammarous#hooks = {}
function! g:grammarous#hooks.on_check(errs) abort
    nmap <buffer><C-n> <Plug>(grammarous-move-to-next-error)
    nmap <buffer><C-p> <Plug>(grammarous-move-to-previous-error)
endfunction

function! g:grammarous#hooks.on_reset(errs) abort
    nunmap <buffer><C-n>
    nunmap <buffer><C-p>
endfunction

let g:grammarous#show_first_error = 1

let g:vimwiki_list = [{"template_path":"~/vimwiki/template","syntax":"default","template_default":"default1.tpl"},{"path": "~/Wiki/", "path_html": "~/Sites/wiki/","template_path":"~/vimwiki/template","template_default":"default.tpl","ext":".md","syntax":"markdown","auto_export":0 },{"path": "~/Dropbox/KM/wiki", "path_html": "~/Dropbox/KM/Sites/html/", "auto_export":0 }]



"autocmd FileType c          nnoremap <buffer> <C-]> :YcmCompleter GoTo<CR>
"autocmd FileType javascript nnoremap <buffer> <C-]> :TernDef<CR><Paste>
"autocmd FileType lua map <leader-,> :TernDef<CR><Paste>
autocmd FileType lua inoremap <leader><tab> <C-x><C-u>
"inoremap <leader><tab> <C-x><C-u>


"let g:ale_lua_luac_executable='/usr/bin/local/luacheck'
"let g:ale_lua_luacheck_executable='/usr/local/bin/luacheck'
let g:lua_complete_dynamic=0
let g:lua_check_syntax = 0
let g:lua_check_globals = 0

autocmd BufWritePre * :%s/\s\+$//e


map <leader>t :wincmd gf<cr>

"nmap <silent> <C-k> <Plug>(ale_previous_wrap)
"nmap <silent> <C-j> <Plug>(ale_next_wrap)
map <C-j> :cnext<cr>
map <C-k> :cprevious<cr>
map <C-n> :lnext<cr>
map <C-p> :lprevious<cr>


"let g:ale_set_loclist = 1
let g:ale_set_quickfix = 1

let g:ale_sign_error = '>>'
let g:ale_sign_warning = '--'

let g:lt_location_list_toggle_map = '<leader>l'
let g:lt_quickfix_list_toggle_map = '<leader>q'
let g:lt_height = 10

"set path='.,/usr/include/**,'
"set path=''
autocmd FileType python set path=.,,**,/usr/lib/python2.7,/root/.virtualenvs/trex/lib/python2.7/site-packages,/root/.virtualenvs/trex/lib/python2.7,/usr/lib/python2.7/dist-packages,/opt/trex-core/scripts/automation/**
"
"python
"set path=.,,**,/usr/lib/python2.7,/root/.virtualenvs/trex/lib/python2.7/site-packages,/root/.virtualenvs/trex/lib/python2.7,/usr/lib/python2.7/dist-packages
"lua
"set path+=

"autocmd FileType lua set path=.,,**,/usr/share/lua/5.1/luarocks,/opt/MoonGen/libmoon/lua
"
set laststatus=2
set statusline=\ %f%m%r%h%w\ %=%({%{&ff}\|%{(&fenc==\"\"?&enc:&fenc).((exists(\"+bomb\")\ &&\ &bomb)?\",B\":\"\")}%k\|%Y}%)\ %([%l,%v][%p%%]\ %)





"let g:go_fmt_command = "goimports"
"let g:go_highlight_functions = 1
"let g:go_highlight_methods = 1
"let g:go_highlight_structs = 1
"" vim-go custom mappings
"au FileType go nmap <Leader>s <Plug>(go-implements)
"au FileType go nmap <Leader>i <Plug>(go-info)
"au FileType go nmap <Leader>gd <Plug>(go-doc)
"au FileType go nmap <Leader>gv <Plug>(go-doc-vertical)
"au FileType go nmap <leader>r <Plug>(go-run)
""au FileType go nmap <leader>b<Plug>(go-build)
"au FileType go nmap <leader>t <Plug>(go-test)
"au FileType go nmap <leader>c <Plug>(go-coverage)
"au FileType go nmap <Leader>ds <Plug>(go-def-split)
"au FileType go nmap <Leader>dv <Plug>(go-def-vertical)
"au FileType go nmap <Leader>dt <Plug>(go-def-tab)
"au FileType go nmap <Leader>e <Plug>(go-rename)
"let g:go_template_autocreate = 1
"

"highlight MatchParen ctermbg=blue guibg=lightblue<Paste>
set cursorline cursorcolumn
let g:netrw_preview=1

"nnoremap <leader>\ :call fzf#vim#tags(expand('<cword>'), {'options': '--exact --select-1 --exit-0'})<CR>

map <C-\>sw : call jedi#force_py_version_switch()<cr>
"nmap <C-\>s :cs find s <C-R>=expand("<cword>")<CR><CR>
"

"python with virtualenv support
"py << EOF
"import os
"import sys
"if 'VIRTUAL_ENV' in os.environ:
"  project_base_dir = os.environ['VIRTUAL_ENV']
"  activate_this = os.path.join(project_base_dir, 'bin/activate_this.py')
"  execfile(activate_this, dict(__file__=activate_this))
"EOF
