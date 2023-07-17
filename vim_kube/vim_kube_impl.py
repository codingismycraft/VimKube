"""Lower level implementation details for the VimKube pluggin."""

import collections
import re
import subprocess

from kubernetes import client, config

ContextInfo = collections.namedtuple(
    'ContextInfo', ["active_context", "contexts"]
)

_CMD_SET_CONTEXT = "kubectl config use-context {context}"

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
    config.load_kube_config()
    contexts = [c['name'] for c in config.list_kube_config_contexts()[0]]
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

