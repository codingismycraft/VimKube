"""Exposes the functionality to handle the contexts."""


import json
import os
import pathlib
import re
import subprocess

try:
    import vim_kube.naming as naming
except ModuleNotFoundError:
    import naming 

_CMD_GET_CONTEXTS = "kubectl config  get-contexts"
_HOME_DIR = pathlib.Path.home()
_CONFIG_PATH = os.path.join(_HOME_DIR, ".kubelens.json")


def getContextsToSkip():
    """Gets to context to skip reading the config file."""
    try:
        with open(_CONFIG_PATH, 'r') as fin:
            data = fin.read()
            config = json.loads(data)
            return set(config['contexts-to-skip'])
    except Exception as ex:
        print(ex)
        return []


def getContexts():
    """Returns all the available Kubernetes contexts."""
    context_to_skip = getContextsToSkip()
    
    contexts = []
    active_context = None
    output = subprocess.getoutput(_CMD_GET_CONTEXTS)
    for index, line in enumerate(output.splitlines()):
        if index == 0:
            continue
        line = re.sub(" +", " ", line)
        tokens = line.split(" ")
        is_active, name, *unused = tokens
        if name not in context_to_skip:
            name = naming.makeContextName(name)
            if is_active:
                active_context = name
            else:
                contexts.append(name)
    return active_context, contexts

