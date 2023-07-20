"""Exposed a function to gather the deployed tags on all contexts."""

try:
    import vim_kube.contexts as contexts
    import vim_kube.services as services
except ModuleNotFoundError:
    import contexts 
    import services 

def getTagsPerService(service_name_to_lookup):
    """Returns tuple list of context and tag for given service."""
    context_to_skip = contexts.getContextsToSkip()
    current_context, other_contexts = contexts.getContexts()
    all_contexts = [current_context] + other_contexts
    deployments = []
    for context_name in all_contexts:
        if context_name in context_to_skip:
            continue
        for service_name, tag in services.getServices(context_name, False):
            if service_name_to_lookup == service_name:
                deployments.append((context_name, tag))
    return deployments

