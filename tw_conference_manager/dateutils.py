from datetime import datetime

TIME_FORMATS = ('%I%M', '%I:%M%p', '%I%p')


def format_time(datetime_object):
    """
    :param datetime_object: a :py:class:`~datetime.datetime` object
    :returns: a string in the format: ``09:00AM``
    """
    return datetime_object.strftime("%I:%M%p")


def parse_time(string):
    """parses a string into a :py:class:`~datetime.datetime` object
    :param string: a :py:class:`basestring`
    :returns: a :py:class:`~datetime.datetime` object
    :raises: :py:exc:`UnknownTimeFormat` if the string is invalid.
    """
    result = None

    for fmt in TIME_FORMATS:
        try:
            result = datetime.strptime(string, fmt)

        except ValueError:
            continue

    if not result:
        raise UnknownTimeFormat(string)

    return result


class UnknownTimeFormat(Exception):
    """Domain-specific exception for when an input time string is invalid."""
    def __init__(self, string):
        supported = ", ".join(TIME_FORMATS)
        tmpl = (
            'the string "{string}" does '
            'not match any of the formats {supported}'
        )
        super(UnknownTimeFormat, self).__init__(tmpl.format(**locals()))
