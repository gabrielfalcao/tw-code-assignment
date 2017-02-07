# -*- coding: utf-8 -*-

from tw_conference_manager.dateutils import parse_time
from tw_conference_manager.dateutils import UnknownTimeFormat


def test_parse_time_with_minutes():
    "parse_time() should parse '09:00am'"

    result = parse_time('09:00am')
    result.should.be.a('datetime.datetime')


def test_parse_time_without_minutes():
    "parse_time() should parse '9PM'"

    result = parse_time('9AM')
    result.should.be.a('datetime.datetime')
    result.hour.should.equal(9)
    result.minute.should.equal(0)


def test_parse_time_colon():
    "parse_time() should parse '0900'"

    result = parse_time('0900')
    result.should.be.a('datetime.datetime')
    result.hour.should.equal(9)
    result.minute.should.equal(0)


def test_parse_time_unknown_format():
    "parse_time() should raise exception if no result was parsed appropriately"

    when_called = parse_time.when.called_with('invalidtime')
    when_called.should.have.raised(
        UnknownTimeFormat,
        'the string "invalidtime" does not match any of the formats %I%M, %I:%M%p, %I%p',
    )
