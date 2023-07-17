" Implemets the functionality of the VimKube pluggin.

let s:plugin_path = expand('<sfile>:p:h')
let s:path_was_added = 0
let s:kubectl_file = "kubeinfo"

function! VimKube#ActivateKubernetesWindow()
" Activates the kubernetes buffer.
    let windowNr = bufwinnr(s:kubectl_file)
    if windowNr > 0
        execute windowNr 'wincmd w'
        execute "normal! ggdG"
    else
        execute "vsplit ". s:kubectl_file
        setlocal buftype=nofile
        setlocal bufhidden=hide
    endif  
endfunction

python3 << endpython
import os
import sys
import vim

def preparePythonPath():
    """Adds the path of the related code to the python path.

    The path is added only once since we rely on a script scoped
    variable (path_was_added) as the import guard.
    """
    was_added = int(vim.eval("s:path_was_added"))
    if not was_added:
        path = vim.eval("s:plugin_path")
        path = os.path.dirname(path)
        sys.path.insert(0, path)
        vim.command("let s:path_was_added = 1")

def addLineToBuffer(line):
    """Adds the pass in text (line) to the active buffer."""
    vim.command(f"let @a= '{line}'")
    vim.command("put a")
endpython

function! VimKube#GetContexts()
" Prints all the available contexts. 
" similar to kubectl config get-contexts
call VimKube#ActivateKubernetesWindow()
python3 << endpython
preparePythonPath()
import vim_kube.vim_kube_impl as vk
current_context, contexts = vk.getContexts()
vim.command(f"let @a= 'Current Context: {current_context}'")
vim.command("put a")
vim.command(f"let @a= '\nContexts'")
vim.command("put a")
for c in contexts:
    vim.command(f"let @a='{c}'")
    vim.command("put a")
endpython
execute "normal! gg"
endfunction



function! VimKube#GetTagPerApplication()
" Prints all the apps and their deployed tags for the active context.
call VimKube#ActivateKubernetesWindow()
python3 << endpython
preparePythonPath()
import vim_kube.vim_kube_impl as vk
current_context, contexts = vk.getContexts()
addLineToBuffer('[Deployed Tags Per Application]')
addLineToBuffer('-' * 80)
addLineToBuffer(f'Current Context: {current_context}')
addLineToBuffer('-' * 80)
for app, tag in vk.getTagPerApplication().items():
    addLineToBuffer(f'{app:40} {tag}')
endpython
execute "normal! gg"
endfunction


function! VimKube#SetActiveContext()
" Sets the active context to what is currently in the default register.    
let l:context = getreg()
python3 << endpython
preparePythonPath()
import vim_kube.vim_kube_impl as vk
context = vim.eval("l:context")
vk.setActiveContext(context)
endpython
call VimKube#GetContexts()
endfunction

