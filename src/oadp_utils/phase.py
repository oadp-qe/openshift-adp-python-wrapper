def check_phase(resource, phase):
    try:
        return resource.instance.status == phase
    except AttributeError:
        return False