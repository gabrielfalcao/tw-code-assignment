# -*- coding: utf-8 -*-

import re


class TextParser(object):
    minute_regex = re.compile(r'^(?P<description>.+)\s+(?P<duration>\d+)min$')
    lightning_regex = re.compile(r'^(?P<description>.+)\s+(?P<duration>lightning)$')

    def parse_line(self, line):
        found = None
        result = None
        line = line.strip()

        for regex in (self.minute_regex, self.lightning_regex):
            found = regex.match(line.strip())
            if found:
                break

        if not found:
            return

        result = found.groupdict()
        duration = result.pop('duration')
        if duration == 'lightning':
            result['duration_in_minutes'] = 5
        else:
            result['duration_in_minutes'] = int(duration)

        return result

    def parse_multiline(self, multiple_strings):
        return [self.parse_line(line) for line in multiple_strings if line.strip()]
