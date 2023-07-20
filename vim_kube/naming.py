"""Utility methods for naming kubernetes objects used in the plugin."""

CONTEXT_DELIMITER = '"'
SERVICE_DELIMITER = "'"
TAG_OPEN_DELIMITER = "{"
TAG_CLOSE_DELIMITER = "}"


def isContextName(name):
    """ Checks if the provided string is a context."""
    name = name.strip()
    return (
            len(name) >= 3 and
            name[0] == name[-1] and
            name[0] == CONTEXT_DELIMITER
    )


def isServiceName(name):
    """ Checks if the provided string is a service."""
    name = name.strip()
    return (
            len(name) >= 3 and
            name[0] == name[-1] and
            name[0] == SERVICE_DELIMITER
    )


def isTagName(name):
    """ Checks if the provided string is a tag."""
    name = name.strip()
    return (
            len(name) >= 3 and
            name[0] == TAG_OPEN_DELIMITER and
            name[-1] == TAG_CLOSE_DELIMITER
    )


def makeContextName(name):
    """Converts the passed in name to a context name."""
    return f"{CONTEXT_DELIMITER}{name}{CONTEXT_DELIMITER}"


def makeServiceName(name):
    """Converts the passed in name to a service name."""
    return f"{SERVICE_DELIMITER}{name}{SERVICE_DELIMITER}"


def makeTagName(name):
    """Converts the passed in name to a tag name."""
    return f"{TAG_OPEN_DELIMITER}{name}{TAG_CLOSE_DELIMITER}"


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
