from datetime import datetime

TIME_FORMATS = ('%H%M', '%H:%M%p', '%H%p')


def parse_time(string):
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
    def __init__(self, string):
        supported = ", ".join(TIME_FORMATS)
        tmpl = 'the string "{string}" does not match any of the formats {supported}'
        super(UnknownTimeFormat, self).__init__(tmpl.format(**locals()))
