# -*- coding: utf-8 -*-

import re


class TextReader(object):
    minute_regex = re.compile(r'^(?P<description>.+)\s+(?P<duration>\d+)min$')
    lightning_regex = re.compile(
        r'^(?P<description>.+)\s+(?P<duration>lightning)$')

    def read_line(self, line):
        found = None
        result = None
        line = line.strip()

        for regex in (self.minute_regex, self.lightning_regex):
            found = regex.match(line.strip())
            if found:
                break

        if not found:
            raise InvalidLineError(line)

        result = found.groupdict()
        duration = result.pop('duration')
        if duration == 'lightning':
            result['duration'] = 5
        else:
            result['duration'] = int(duration)

        return result

    def read_multiline(self, multiple_strings):
        return [self.read_line(l) for l in multiple_strings if l.strip()]


class InvalidLineError(Exception):

    def __init__(self, line):
        tmpl = 'could not parse duration in string: "{line}"'
        self.line = line
        super(InvalidLineError, self).__init__(tmpl.format(**locals()))
