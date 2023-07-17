"""Lower level implementation details for the VimKube pluggin."""

import collections
import json
import os
import pathlib
import re
import subprocess

from kubernetes import client, config

_HOME_DIR = pathlib.Path.home()
_CONFIG_PATH = os.path.join(_HOME_DIR, ".kubelens.json")

ContextInfo = collections.namedtuple(
    'ContextInfo', ["active_context", "contexts"]
)

_CMD_SET_CONTEXT = "kubectl config use-context {context}"


def _get_contexts_to_skip():
    """Gets to context to skip reading the config file."""
    try:
        with open(_CONFIG_PATH, 'r') as fin:
            data = fin.read()
            config = json.loads(data)
            return set(config['contexts-to-skip'])
    except Exception as ex:
        return []

def setActiveContext(context):
    """Sets the active context."""
    cmd = _CMD_SET_CONTEXT.format(context=context)
    output = subprocess.getoutput(cmd)
    for line in output.splitlines():
        line = line.strip().lower()
        if "error" in line:
            print(line)


def getContexts():
    """Returns a ContextInfo object.

    Used to retrieve the active and the non-active contexts similarly
    to calling the following:

    kubectl config get-contexts
    """
    contexts_to_skip = _get_contexts_to_skip()
    config.load_kube_config()
    contexts = []
    for c in config.list_kube_config_contexts()[0]:
        name = c['name']
        if name not in contexts_to_skip:
            contexts.append(name)
    active_context = config.list_kube_config_contexts()[1]['name']
    return ContextInfo(active_context, contexts)


def getTagPerApplication():
    """Returns a mapping from the application name to its deployed tag."""
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    context = config.list_kube_config_contexts()[1]['context']["namespace"]
    pod_list = api_instance.list_namespaced_pod(namespace=context)
    tags = {}
    for pod in pod_list.items:
        labels = pod.metadata.labels
        app = labels.get('app')
        tag = labels.get("mw.release", 'n/a')
        if app:
            tags[app] = str(tag)
    return tags

