# -*- coding: utf-8 -*-

from tw_conference_manager.models import Talk
from tw_conference_manager.models import TalkList
from tw_conference_manager.models import Track
from tw_conference_manager.models import Session

from tests.functional.helpers import create_track_and_allocate_talks
from tests.functional.fixtures import default_proposed_talks


def test_track_has_sessions():
    "models.Track contains a morning and an afternoon session"

    # Given a Track instance
    track = Track(1)

    # When I check its properties
    track.should.have.property('number').being.equal(1)

    # It should have session instances
    track.should.have.property('morning_session').being.a(Session)
    track.should.have.property('afternoon_session').being.a(Session)

    # And its morning session should start at 9AM and end at noon
    track.morning_session.start_time.should.equal('09:00AM')
    track.morning_session.end_time.should.equal('12:00PM')

    # And its afternoon session should start at 9AM and end at noon
    track.afternoon_session.start_time.should.equal('01:00PM')
    track.afternoon_session.end_time.should.equal('05:00PM')


def test_track_filled_up():
    "models.Track.allocate_talks() fills up as much time as possible before networking event"

    ten_talks_of_60_minutes = [Talk('Talk {0}'.format(i), 60) for i in range(1, 11)]
    allocated, remaining = create_track_and_allocate_talks(ten_talks_of_60_minutes)
    allocated.should.have.length_of(5)
    remaining.should.have.length_of(5)


def test_minimize_open_time():
    "models.Track.allocate_talk() will search through remaining talks to fill available timeslot"

    allocated, remaining = create_track_and_allocate_talks([
        Talk("Long", 210),
        Talk("Too Long", 60),
        Talk("Just Right", 30),
        Talk("Long Afternoon", 195),
        Talk("Too Long Afternoon", 60),
        Talk("Closest Afternoon", 30)
    ])
    allocated.should.have.length_of(4)


def test_track_to_lines():
    "models.Track.to_lines() returns a string representing the track and all its talks"

    track1 = Track(1)

    allocated, remaining = track1.allocate_talks(default_proposed_talks)

    result = track1.to_lines()
    result.should.equal([
        'Track 1:',
        '09:00AM Writing Fast Tests Against Enterprise Rails 60min',
        '10:10AM Overdoing it in Python 45min',
        '11:05AM Lua for the Masses 30min',
        '11:45AM Rails for Python Developers lightning',
        '12:00PM Lunch',
        '01:00PM Ruby Errors from Mismatched Gem Versions 45min',
        '01:55PM Common Ruby Errors 45min',
        '02:50PM Communicating Over Distance 60min',
        '04:00PM Accounting-Driven Development 45min',
        '05:00PM Networking Event'
    ])
