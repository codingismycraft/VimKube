"""Utility methods for naming kubernetes objects used in the plugin."""

_CONTEXT_DELIMITER = '"'
_SERVICE_DELIMITER = "'"
_TAG_OPEN_DELIMITER = "{"
_TAG_CLOSE_DELIMITER = "}"


def isContextName(name):
    """ Checks if the provided string is a context."""
    name = name.strip()
    return (
            len(name) >= 3 and
            name[0] == name[-1] and
            name[0] == _CONTEXT_DELIMITER
    )


def isServiceName(name):
    """ Checks if the provided string is a service."""
    name = name.strip()
    return (
            len(name) >= 3 and
            name[0] == name[-1] and
            name[0] == _SERVICE_DELIMITER
    )


def isTagName(name):
    """ Checks if the provided string is a tag."""
    name = name.strip()
    return (
            len(name) >= 3 and
            name[0] == _TAG_OPEN_DELIMITER and
            name[-1] == _TAG_CLOSE_DELIMITER
    )


def makeContextName(name):
    """Converts the passed in name to a context name."""
    return f"{_CONTEXT_DELIMITER}{name}{_CONTEXT_DELIMITER}"


def makeServiceName(name):
    """Converts the passed in name to a service name."""
    return f"{_SERVICE_DELIMITER}{name}{_SERVICE_DELIMITER}"


def makeTagName(name):
    """Converts the passed in name to a tag name."""
    return f"{_TAG_OPEN_DELIMITER}{name}{_TAG_CLOSE_DELIMITER}"


if __name__ == '__main__':
    # Self-test...

    assert isTagName("{abc}")
    assert isServiceName("'abc'")
    assert isContextName('"{abc}"')

    assert not isTagName("abc")
    assert not isServiceName("abc")
    assert not isContextName('abc}"')

    assert isTagName(makeTagName("abc"))
    assert isServiceName(makeServiceName("abc"))
    assert isContextName(makeContextName("abc"))
