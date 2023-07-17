"""Lower level implementation details for the VimKube pluggin."""

import collections

from kubernetes import client, config

ContextInfo = collections.namedtuple(
    'ContextInfo', ["active_context", "contexts"]
)


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

