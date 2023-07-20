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
    if "'" in line:
        vim.command(f"let @a= \"{line}\"")
        vim.command("put a")
    else:
        vim.command(f"let @a= '{line}'")
        vim.command("put a")
endpython


function! VimKube#ProcessUserSelection()
    " Open the scratch buffer if needed.
    let l:curfile = expand("%:t")

    " If currently not in the scrath pad then open it and show contexts.
    if l:curfile  != s:kubectl_file
        " The user is editing a file other than the buffer 
        " just show the contexts for the currently active context.
        call VimKube#GetContexts(1)
        return
    endif

    " The user is on the pluggin's window. 
    
    " 1. Check if the user is clicking a Context.
    let @"="" 
    execute 'normal! yi"' 
    let l:context_name = @"

    if l:context_name != ""
        " The user selected a context..
        " - Will change the current context to the selected one.
        " - et all the services and tags and print them to the buffer.
        call VimKube#ShowServicesForContext(l:context_name)
        return
    endif


    " 2. Check if the user is clicking a Service.
    let @"="" 
    execute "normal! yi'" 
    let l:service_name = @"

    if l:service_name!= ""
        " The user selected a service
        call VimKube#ShowAllDeployedTags(service_name)
        return
    endif

    " 3. Check if the user is clicking a Tag.
endfunction



function! VimKube#GetContexts(clearScreen)
" Prints all the available contexts. 
" similar to kubectl config get-contexts
call VimKube#ActivateKubernetesWindow()
if a:clearScreen == 1
    execute "normal! ggdG"
endif
python3 << endpython
preparePythonPath()
import vim_kube.contexts as vk
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

function VimKube#ShowAllDeployedTags(service)
call VimKube#ActivateKubernetesWindow()
python3 << endpython
preparePythonPath()
import vim_kube.tags as tags
service = vim.eval("a:service")
addLineToBuffer(f'[Deployed Tags for service: {service} ]')
addLineToBuffer('-' * 80)
for context, tag in tags.getTagsPerService(service):
    line = f"{context:40} {tag}"
    addLineToBuffer(line)
addLineToBuffer('-' * 80)
endpython
execute "normal! gg"
endfunction


function! VimKube#ShowServicesForContext(context_name)
" Prints all the apps and their deployed tags for the active context.
call VimKube#ActivateKubernetesWindow()
python3 << endpython
preparePythonPath()
import vim_kube.services as services
import vim_kube.contexts as contexts

context_name = vim.eval("a:context_name")
addLineToBuffer('[Deployed Tags Per Application]')
addLineToBuffer('-' * 80)
addLineToBuffer(f'Current Context: {context_name}')
addLineToBuffer('-' * 80)

for app, tag in services.getServices(context_name):
    addLineToBuffer(f'{app:40} {tag}')
 
current_context, other_contexts = contexts.getContexts()

addLineToBuffer('-' * 80)
addLineToBuffer('[Other Contexts]')
addLineToBuffer('-' * 80)
for c in other_contexts:
    addLineToBuffer(c)

endpython
execute "normal! gg"
endfunction


