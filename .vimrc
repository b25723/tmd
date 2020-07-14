" Specify a directory for plugins
" - For Neovim: stdpath('data') . '/plugged'
" - Avoid using standard Vim directory names like 'plugin'
call plug#begin('~/.vim/plugged')

" Make sure you use single quotes

" Shorthand notation; fetches https://github.com/junegunn/vim-easy-align
Plug 'junegunn/vim-easy-align'

" Any valid git URL is allowed
"Plug 'https://github.com/junegunn/vim-github-dashboard.git'

" Multiple Plug commands can be written in a single line using | separators
Plug 'SirVer/ultisnips' | Plug 'honza/vim-snippets'

" On-demand loading
"Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }
"Plug 'tpope/vim-fireplace', { 'for': 'clojure' }


" Using a tagged release; wildcard allowed (requires git 1.9.2 or above)
"Plug 'fatih/vim-go', { 'tag': '*' }

Plug 'w0rp/ale', { 'for': ['python', 'sh', 'vim'] }

" Plugin options
"Plug 'nsf/gocode', { 'tag': 'v.20150303', 'rtp': 'vim' , 'for': 'go' }

" Plugin outside ~/.vim/plugged with post-update hook
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'

" Unmanaged plugin (manually installed and updated)
"Plug '~/my-prototype-plugin'
Plug 'Valloric/ListToggle'

Plug 'mfukar/robotframework-vim', { 'for': 'robot' }
Plug 'mMontu/vim-RobotUtils', { 'for': 'robot' }

"Plug 'wesleyche/SrcExpl'

" Using a non-master branch
"Plug 'rdnetto/YCM-Generator', { 'branch': 'stable' }
Plug 'davidhalter/jedi-vim', { 'for': 'python' }
"Plug 'Valloric/YouCompleteMe', { 'do': './install.py --go-completer --clang-completer',  'for': ['c', 'cpp', 'go', 'python'] }
Plug 'preservim/nerdtree'

Plug 'majutsushi/tagbar', { 'for': ['python', 'robot', 'c', 'cpp', 'vim'] }
Plug 'vim-scripts/taglist.vim', { 'for': ['python', 'robot'] }

Plug 'jpalardy/vim-slime', { 'for': ['python','c','cpp','robot'] }
Plug 'hanschen/vim-ipython-cell', { 'for': 'python'}
"Plug 'ludovicchabant/vim-gutentags', { 'for': ['python', 'robot'] }
"Plug 'skywind3000/gutentags_plus', { 'for': ['python', 'robot'] }
"Plug 'chazy/cscope_maps'


" Initialize plugin system
call plug#end()


let mapleader=','
noremap <leader>E :qa!<CR>   " Quit all windows

if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

let g:python_host_prog = '/home/rex/.virtualenvs/py27/bin/python'
let g:python3_host_prog = '/home/rex/.virtualenvs/py36/bin/python'


map <C-j> :cnext<CR>
map <C-k> :cprev<CR>
map <C-n> :lnex<CR>
map <C-p> :lprev<CR>
map <C-j> :tn<CR>
map <C-k> :tp<CR>

map <C-UP> <C-W>w

set path+=/home/rex/.virtualenvs/py36/trex/**,/home/rex/.virtualenvs/py36/ICS_QA/**
"set path+=/home/rex/.virtualenvs/py36/trex/**,/home/rex/.virtualenvs/py36/ICS_QA/**
"set isfname+=32
"autocmd BufRead,BufNewFile *.robot set filetype=text syntax=text
"wincmd = <C-W>

" Start interactive EasyAlign in visual mode (e.g. vipga)
xmap ga <Plug>(EasyAlign)

" Start interactive EasyAlign for a motion/text object (e.g. gaip)
nmap ga <Plug>(EasyAlign)

"set tags+=~/.vim/tags/tx.tags;~/.vim/tags/python.tags

nmap <Leader>tb :TagbarToggle<CR>
nmap <Leader>tl :TlistToggle<CR>

noremap <Leader>ts :ts 

let g:tagbar_width = 50
let g:tagbar_autoclose=1
let g:tagbar_autofocus=0
"let g:tagbar_left=1
let g:tagbar_right=1

set mouse+=a
nnoremap <leader>fl :Lines 
nnoremap <leader>fb :BLines 
nnoremap <leader>ff :Files 
nnoremap <leader>fg :GFiles 
nnoremap <leader>f? :GFiles? 
nnoremap <leader>ft :Tags<cr>
nnoremap <leader>fa :Ag 
nnoremap <leader>fr :Rg 

"set listchars=eol:¬,tab:>·,trail:~,extends:>,precedes:<,space:␣
"set list

"inoremap <leader><tab> <C-x><C-o>	"keyword completion

set t_Co=256
syntax on
colorscheme molokai
set wildignore+=**/node_modules/**
"set autochdir
"let Tlist_Auto_Open=1

set splitbelow
"set splitright
"set cursorline cursorcolumn
let g:netrw_preview=1		"set the Ex file browser to open a vsplit pane
let g:netrw_winsize=20
let g:jedi#use_splits_not_buffers = "right"
let g:jedi#show_call_signatures = "1"

map <F5> <C-W>_<C-W><Bar>	"vim current window maximize
nnoremap <leader>c :pc<CR>	"preview close

let g:ale_completion_enabled = 1
"let g:ale_open_list=1
"let g:ale_linters = {'html': ['htmlhint'], 'javascript': ['jshint'], 'css': ['csslint'], 'python': ['flake8'], 'lua': ['luacheck'], 'sh': ['shellcheck'] }
"
set completeopt=menu,menuone,preview,noselect,noinsert

let g:ycm_global_ycm_extra_conf='~/.vim/plugged/YouCompleteMe/third_party/ycmd/.ycm_extra_conf.py'
let g:ycm_confirm_extra_conf=0
let g:ycm_collect_identifiers_from_tag_files=1
let g:ycm_key_invoke_completion = '<leader><tab>'
let g:ycm_seed_identifiers_with_syntax=1
let g:ycm_min_num_of_chars_for_completion = 2
let g:ycm_auto_trigger = 1

nnoremap <leader>d :YcmCompleter GoToDefinitionElseDeclaration<CR>

"nnoremap <leader>jd :YcmCompleter GoToDefinitionElseDeclaration<CR>
"nnoremap <leader>jdf :YcmCompleter GoToDefinition<CR>
"nnoremap <leader>jdc :YcmCompleter GoToDeclaration<CR>
"nnoremap <leader>st :YcmCompleter GetType<CR>
"
"
"

"autocmd vimenter * NERDTree  "自动开启Nerdtree
let g:NERDTreeWinSize = 25 "设定 NERDTree 视窗大小
"开启/关闭nerdtree快捷键
map <C-d> :NERDTreeToggle<CR>
"let NERDTreeShowBookmarks=1  " 开启Nerdtree时自动显示Bookmarks
"打开vim时如果没有文件自动打开NERDTree
autocmd vimenter * if !argc()|NERDTree|endif
"当NERDTree为剩下的唯一窗口时自动关闭
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
"设置树的显示图标
let g:NERDTreeDirArrowExpandable = '▸'
let g:NERDTreeDirArrowCollapsible = '▾'
let NERDTreeIgnore = ['\.pyc$']  " 过滤所有.pyc文件不显示
"let g:NERDTreeShowLineNumbers=1  " 是否显示行号
let g:NERDTreeHidden=0     "不显示隐藏文件
"Making it prettier
let NERDTreeMinimalUI = 1
let NERDTreeDirArrows = 1

augroup rungroup
    autocmd!
    autocmd BufRead,BufNewFile *.go nnoremap <F6> :exec '!go run' shellescape(@%, 1)<cr>
    autocmd BufRead,BufNewFile *.py nnoremap <F6> :exec '!python' shellescape(@%, 1)<cr>
augroup END

let g:jedi#completions_enabled = 0
let g:kite_auto_complete=1
let g:kite_supported_languages = ['python', 'javascript', 'go']
let g:kite_tab_complete=1
set completeopt+=menuone   " show the popup menu even when there is only 1 match
set completeopt+=noinsert  " don't insert any text until user chooses a match
set completeopt-=longest   " don't insert the longest common text

set completeopt+=preview
autocmd CompleteDone * if !pumvisible() | pclose | endif
set belloff+=ctrlg  " if vim beeps during completion
let g:kite_snippets=0
"let g:kite_previous_placeholder = '<C-H>'
"let g:kite_next_placeholder = '<C-L>'
nmap <silent> <buffer> gK <Plug>(kite-docs)
"let g:kite_documentation_continual=1

"set completeopt=longest,menu
let g:slime_target = "tmux"
let g:slime_python_ipython = 1

"set statusline=%<%f\ %h%m%r%{kite#statusline()}%=%-14.(%l,%c%V%)\ %P
"set laststatus=2  " always display the status line
"
let g:ale_python_flake8_options = '--ignore=F401,E225,E231,W391,E401,E402,E211,E266,E501,E302,E305'
