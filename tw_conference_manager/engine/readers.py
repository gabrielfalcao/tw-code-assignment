# -*- coding: utf-8 -*-

import re


class TextReader(object):
    """Object that can parse lines containing descriptions and durations
    of proposed conference talks."""

    minute_regex = re.compile(r'^(?P<description>.+)\s+(?P<duration>\d+)min$')
    lightning_regex = re.compile(
        r'^(?P<description>.+)\s+(?P<duration>lightning)$')

    def read_line(self, line):
        """extracts metadata from a single line of text.

        :param line: a :py:class:`basestring`
        :returns: a :py:class:`dict` containing the keys ``description`` and ``duration``
        :raises: :py:exc:`InvalidLineError` when the line does not contain a valid duration.
        """
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
        """parses a multi-line string.
        :returns: a list of :py:class:`dict` as in :py:meth:`~TextReader.read_line`
        """
        return [self.read_line(l) for l in multiple_strings if l.strip()]


class InvalidLineError(Exception):
    """Domain-specific exception for when an input line describes a talk
    specifying duration."""
    def __init__(self, line):
        tmpl = 'could not parse duration in string: "{line}"'
        self.line = line
        super(InvalidLineError, self).__init__(tmpl.format(**locals()))
