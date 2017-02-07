# -*- coding: utf-8 -*-

from tw_conference_manager.models import Talk
from tw_conference_manager.models import TalkList
from tw_conference_manager.models import Track
from tw_conference_manager.models import Session
from tests.unit.fixtures import TEST_INPUT


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


def test_track_allocate_talks():
    "models.Track.allocate_talks() fills up both morning and afternoon sessions"

    track1 = Track(1)

    talks = TalkList.from_text(TEST_INPUT)
    allocated, remaining = track1.allocate_talks(talks)

    allocated.should.have.length_of(4)
    remaining.should.have.length_of(15)
    allocated.should.equal(TalkList(
        Talk(description='Writing Fast Tests Against Enterprise Rails', duration=60),
        Talk(description='Overdoing it in Python', duration=45),
        Talk(description='Lua for the Masses', duration=30),
        Talk(description='Ruby Errors from Mismatched Gem Versions', duration=45)
    ))
    remaining.should.equal(TalkList(
        Talk(description='Common Ruby Errors', duration=45),
        Talk(description='Rails for Python Developers', duration=5),
        Talk(description='Communicating Over Distance', duration=60),
        Talk(description='Accounting-Driven Development', duration=45),
        Talk(description='Woah', duration=30),
        Talk(description='Sit Down and Write', duration=30),
        Talk(description='Pair Programming vs Noise', duration=45),
        Talk(description='Rails Magic', duration=60),
        Talk(description='Ruby on Rails: Why We Should Move On', duration=60),
        Talk(description='Clojure Ate Scala (on my project)', duration=45),
        Talk(description='Programming in the Boondocks of Seattle', duration=30),
        Talk(description='Ruby vs. Clojure for Back-End Development', duration=30),
        Talk(description='Ruby on Rails Legacy App Maintenance', duration=60),
        Talk(description='A World Without HackerNews', duration=30),
        Talk(description='User Interface CSS in Rails Apps', duration=30)
    ))


def test_track_to_lines():
    "models.Track.to_lines() returns a string representing the track and all its talks"

    track1 = Track(1)

    talks = TalkList.from_text('''
    Writing Fast Tests Against Enterprise Rails 60min
    Overdoing it in Python 45min
    Lua for the Masses 30min
    Ruby Errors from Mismatched Gem Versions 45min
    Common Ruby Errors 45min
    Rails for Python Developers lightning
    Communicating Over Distance 60min
    Accounting-Driven Development 45min
    Woah 30min
    Sit Down and Write 30min
    Pair Programming vs Noise 45min
    Rails Magic 60min
    Ruby on Rails: Why We Should Move On 60min
    Clojure Ate Scala (on my project) 45min
    Programming in the Boondocks of Seattle 30min
    Ruby vs. Clojure for Back-End Development 30min
    Ruby on Rails Legacy App Maintenance 60min
    A World Without HackerNews 30min
    User Interface CSS in Rails Apps 30min
    ''')
    allocated, remaining = track1.allocate_talks(talks)

    result = track1.to_lines()
    result.should.equal([
        'Track 1:',
        '09:00AM Writing Fast Tests Against Enterprise Rails 60min',
        '10:00AM Overdoing it in Python 45min',
        '10:45AM Lua for the Masses 30min',
        '11:15AM Ruby Errors from Mismatched Gem Versions 45min',
        '12:00PM Lunch',
        '05:00PM Networking Event'
    ])
