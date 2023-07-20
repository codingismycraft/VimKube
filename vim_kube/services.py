"""Exposes the get_services function."""

import re
import subprocess

try:
    import vim_kube.naming as naming
except ModuleNotFoundError:
    import naming 

_CMD_GET_SERVICES = "kubectl get pods --show-labels"
_CMD_SET_CONTEXT = "kubectl config use-context {context}"
_CMD_CURRENT_CONTEXT = """kubectl config current-context"""


def _get_tag(line):
    """Parses the line and returns the tag branch."""
    matched = re.search('mw.release=([^,]+)', line)
    if matched:
        return matched.groups()[0]


def _get_service_name(line):
    """Parses the line and returns the service name."""
    matched = re.search('app=([^,]+)', line)
    if matched:
        return matched.groups()[0]


def _set_active_context(context):
    """Sets the active context."""
    _CMD_SET_CONTEXT = "kubectl config use-context {context}"
    cmd = _CMD_SET_CONTEXT.format(context=context)
    output = subprocess.getoutput(cmd)
    for line in output.splitlines():
        line = line.strip().lower()
        if "error" in line:
            raise ValueError(f"Invalid context: {context}")


def _get_active_context():
    """Returns the active context."""
    output = subprocess.getoutput(_CMD_CURRENT_CONTEXT)
    for line in output.splitlines():
        line = line.strip()
        return line


def getServices(context_name, use_delimeters=True):
    """Returns the detailed description for the services for the context.

    If the passed in context name is not the current the it was changed
    to it and will remain for the rest of the application.
    """
    original_context = _get_active_context()
    if context_name != original_context:
        _set_active_context(context_name)
    services = {}
    output = subprocess.getoutput(_CMD_GET_SERVICES)
    for index, line in enumerate(output.splitlines()):
        if index == 0:
            continue
        line = re.sub(" +", " ", line)
        service_name = _get_service_name(line)
        if not service_name:
            continue
        tag = _get_tag(line)
        if use_delimeters:
            tag = naming.makeTagName(tag)
            service_name = naming.makeServiceName(service_name)
        services[service_name] = tag
    return [(k, v) for k, v in services.items()]

