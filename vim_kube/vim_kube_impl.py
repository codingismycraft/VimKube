"""Lower level implementation details for the VimKube pluggin."""

import collections
import json
import os
import pathlib
import re
import subprocess

from kubernetes import client, config

import vim_kube.naming as naming
import vim_kube.contexts as contexts
import vim_kube.services as services
import vim_kube.tags as tags


_HOME_DIR = pathlib.Path.home()
_CONFIG_PATH = os.path.join(_HOME_DIR, ".kubelens.json")

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
    contexts_to_skip = _get_contexts_to_skip()
    config.load_kube_config()
    contexts = []
    for c in config.list_kube_config_contexts()[0]:
        name = c['name']
        if name not in contexts_to_skip:
            contexts.append(naming.makeContextName(name))
    active_context = config.list_kube_config_contexts()[1]['name']
    active_context = naming.makeContextName(active_context)
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
        service = labels.get('app')
        service = naming.makeServiceName(service)
        tag = labels.get("mw.release", 'n/a')
        tag = naming.makeTagName(tag)
        if service:
            tags[service] = str(tag)
    return tags


def _getDeployedTag(service, context, api_instance):
    """Returns the tag for a given service that is deployed to context."""
    setActiveContext(context)
    namespace = config.list_kube_config_contexts()[1]['context']["namespace"]
    pod_list = api_instance.list_namespaced_pod(namespace=namespace)
    tag = "n/a"
    for pod in pod_list.items:
        labels = pod.metadata.labels
        current_service = labels.get('app').strip().lower()
        if current_service == service.lower():
            tag = labels.get("mw.release", 'n/a').strip()
            print(service, context, tag) 
            return tag
    print(service, context, tag) 
    return tag 


def getAllDeployedTags(service):
    """Returns all the deployed tags for the passed in service.

    The returned value is a list of 2 dimensional tuples where the
    first element is the context name and  the second element is the
    deployed tag for the passed in service. Example:
    [  (context1, tag1), ... ]
    """
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    contexts_to_skip = _get_contexts_to_skip()
    contexts = []
    for c in config.list_kube_config_contexts()[0]:
        name = c['name']
        if name not in contexts_to_skip:
            contexts.append(name)
    active_context = config.list_kube_config_contexts()[1]['name']
    contexts.append(active_context)

    return [
        (context, _getDeployedTag(service, context, api_instance))
        for context in contexts
    ]

