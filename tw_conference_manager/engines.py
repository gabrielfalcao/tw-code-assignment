# -*- coding: utf-8 -*-

import re


class TextParser(object):
    line_regex = re.compile(r'^(?P<description>.+)\s+(?P<duration>\d+)min$')

    def parse_line(self, line):
        found = self.line_regex.match(line.strip())
        result = None
        if found:
            result = found.groupdict()
            result['duration_in_minutes'] = int(result.pop('duration'))

        return result
