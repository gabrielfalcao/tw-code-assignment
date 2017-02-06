# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tw_conference_manager.engines import TextParser


def test_parse_line():
    "TextParser.parse_line() should receive a simple, valid line as string and return structured metadata"

    # Given an instance of TextParser
    parser = TextParser()

    # And a valid input in minutes
    target = 'Writing Fast Tests Against Enterprise Rails 60min'
    result = parser.parse_line(target)

    # Then it should have returned a dictionary
    result.should.be.a(dict)

    # And it should contain the description and duration
    result.should.have.key('description').being.a(basestring)
    result.should.have.key('duration_in_minutes').being.an(int)

    result['description'].should.equal('Writing Fast Tests Against Enterprise Rails')
    result['duration_in_minutes'].should.equal(60)
