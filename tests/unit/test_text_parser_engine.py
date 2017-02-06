# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tw_conference_manager.engines import TextParser
from tw_conference_manager.engines import InvalidLineError


def test_parse_valid_line_with_minutes():
    "TextParser.parse_line() should receive a simple, valid line as string and return structured metadata"

    # Given an instance of TextParser
    parser = TextParser()

    # And a valid input in minutes
    target = 'Writing Fast Tests Against Enterprise Rails 60min'

    # When I parse the target line
    result = parser.parse_line(target)

    # Then it should have returned a dictionary
    result.should.be.a(dict)

    # And it should contain the description and duration
    result.should.have.key('description').being.a(basestring)
    result.should.have.key('duration_in_minutes').being.an(int)

    result['description'].should.equal('Writing Fast Tests Against Enterprise Rails')
    result['duration_in_minutes'].should.equal(60)


def test_parse_valid_line_lightning():
    "TextParser.parse_line() should parse lightning talks in minutes"

    # Given an instance of TextParser
    parser = TextParser()

    # And a valid lightning talk input line
    target = 'Rails for Python Developers lightning'

    # When I parse the target line
    result = parser.parse_line(target)

    # Then it should have returned a dictionary
    result.should.be.a(dict)

    # And it should contain the description and duration of 5 minutes
    result.should.have.key('description').being.a(basestring)
    result.should.have.key('duration_in_minutes').being.an(int)

    result['description'].should.equal('Rails for Python Developers')
    result['duration_in_minutes'].should.equal(5)


def test_parse_multiple_valid_lines():
    "TextParser.parse_multiline() should receive a list of valid line strings and return a list of structured metadata"

    # Given an instance of TextParser
    parser = TextParser()

    # And list with 3 valid lines
    target_lines = '''
    Writing Fast Tests Against Enterprise Rails 60min
    Lua for the Masses 30min
    Rails for Python Developers lightning
    '''.splitlines()

    # When I parse the list of lines
    result = parser.parse_multiline(target_lines)

    # Then it should have returned a list with 3 members
    result.should.be.a(list)
    result.should.have.length_of(3)
    FIRST_LINE, SECOND_LINE, THIRD_LINE = result

    FIRST_LINE.should.be.a(dict)
    SECOND_LINE.should.be.a(dict)
    THIRD_LINE.should.be.a(dict)

    result.should.equal([
        {'duration_in_minutes': 60, 'description': u'Writing Fast Tests Against Enterprise Rails'},
        {'duration_in_minutes': 30, 'description': u'Lua for the Masses'},
        {'duration_in_minutes': 5, 'description': u'Rails for Python Developers'},
    ])


def test_parse_invalid_line():
    "TextParser.parse_line() should raise an exception that points out an invalid line"

    # Given an instance of TextParser
    parser = TextParser()

    # And an invalid input line
    invalid_target = 'Some Invalid Line Without Duration'

    # When I try parse the target line
    when_called = parser.parse_line.when.called_with(invalid_target)

    # Then it should have raised InvalidLineError
    when_called.should.have.raised(
        InvalidLineError,
        'could not parse duration in string: "Some Invalid Line Without Duration"'
    )
