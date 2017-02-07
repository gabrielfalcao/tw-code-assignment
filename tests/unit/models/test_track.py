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

def test_track_filled_up():
    "models.Track.allocate_talks() fills up as much time as possible before networking event"

    track1 = Track(1)
    talks = TalkList(*[Talk('Talk {0}'.format(i), 60) for i in range(1, 11)])
    allocated, remaining = track1.allocate_talks(talks)
    allocated.should.have.length_of(5)


def test_minimize_open_time():
    "models.Track.allocate_talk() will search through remaining talks to fill available timeslot"

    track1 = Track(1)
    talks = TalkList(
        Talk("Long", 210),
        Talk("Too Long", 60),  # not fit
        Talk("Just Right", 30), # end morning
        Talk("Long Afternoon", 195), 
        Talk("Too Long Afternoon", 60),
        Talk("Closest Afternoon", 30)
    )

    allocated, remaining = track1.allocate_talks(talks)
    allocated.should.have.length_of(4)