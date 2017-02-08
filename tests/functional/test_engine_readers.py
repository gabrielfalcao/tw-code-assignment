# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tw_conference_manager.engine.readers import TextReader
from tw_conference_manager.engine.readers import InvalidLineError


def test_read_valid_line_with_minutes():
    "TextReader.read_line() should receive a simple, valid line as string and return structured metadata"

    # Given an instance of TextReader
    parser = TextReader()

    # And a valid input in minutes
    target = 'Writing Fast Tests Against Enterprise Rails 60min'

    # When I parse the target line
    result = parser.read_line(target)

    # Then it should have returned a dictionary
    result.should.be.a(dict)

    # And it should contain the description and duration
    result.should.have.key('description').being.a(basestring)
    result.should.have.key('duration').being.an(int)

    result['description'].should.equal('Writing Fast Tests Against Enterprise Rails')
    result['duration'].should.equal(60)


def test_read_valid_line_lightning():
    "TextReader.read_line() should parse lightning talks in minutes"

    # Given an instance of TextReader
    parser = TextReader()

    # And a valid lightning talk input line
    target = 'Rails for Python Developers lightning'

    # When I parse the target line
    result = parser.read_line(target)

    # Then it should have returned a dictionary
    result.should.be.a(dict)

    # And it should contain the description and duration of 5 minutes
    result.should.have.key('description').being.a(basestring)
    result.should.have.key('duration').being.an(int)

    result['description'].should.equal('Rails for Python Developers')
    result['duration'].should.equal(5)


def test_read_multiple_valid_lines():
    "TextReader.read_multiline() should receive a list of valid line strings and return a list of structured metadata"

    # Given an instance of TextReader
    parser = TextReader()

    # And list with 3 valid lines
    target_lines = '''
    Writing Fast Tests Against Enterprise Rails 60min
    Lua for the Masses 30min
    Rails for Python Developers lightning
    '''.splitlines()

    # When I parse the list of lines
    result = parser.read_multiline(target_lines)

    # Then it should have returned a list with 3 members
    result.should.be.a(list)
    result.should.have.length_of(3)
    FIRST_LINE, SECOND_LINE, THIRD_LINE = result

    FIRST_LINE.should.be.a(dict)
    SECOND_LINE.should.be.a(dict)
    THIRD_LINE.should.be.a(dict)

    result.should.equal([
        {'duration': 60, 'description': u'Writing Fast Tests Against Enterprise Rails'},
        {'duration': 30, 'description': u'Lua for the Masses'},
        {'duration': 5, 'description': u'Rails for Python Developers'},
    ])


def test_read_invalid_line():
    "TextReader.read_line() should raise an exception that points out an invalid line"

    # Given an instance of TextReader
    parser = TextReader()

    # And an invalid input line
    invalid_target = 'Some Invalid Line Without Duration'

    # When I try parse the target line
    when_called = parser.read_line.when.called_with(invalid_target)

    # Then it should have raised InvalidLineError
    when_called.should.have.raised(
        InvalidLineError,
        'could not parse duration in string: "Some Invalid Line Without Duration"'
    )
