
def validate(request, handlers):
    if 'resource' not in request:
        return False, _error("missing parameter: {}".format("resource"))
    if 'action' not in request:
        return False, _error("missing parameter: {}".format("action"))
    resource = request['resource']
    if resource not in handlers:
        return False, _error("invalid parameter: {}".format(resource))
    action = request['action']
    if action not in handlers[resource]:
        return False, _error("invalid action: {} for resource: {}".format(action, resource))
    for arg in handlers[resource][resource][action][1]:
        if arg not in request:
            return False, _error("invalid parameter: {}".format(arg))
    return True, request


def _error(msg):
    return {"error": msg}
