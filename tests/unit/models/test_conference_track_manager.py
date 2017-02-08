# -*- coding: utf-8 -*-

from tw_conference_manager.models import ConferenceTrackManager
from tests.unit.fixtures import default_proposed_talks
from tests.unit.helpers import create_conference_and_schedule_talks


def test_track_has_sessions():
    "models.ConferenceTrackManager contains 2 tracks"

    # Given a Track instance
    mgr = ConferenceTrackManager('My Test Conference')

    # When I check its properties
    mgr.should.have.property('name').being.equal('My Test Conference')
    mgr.should.have.property('tracks').being.a(list)

    # And it should be empty by default
    mgr.tracks.should.be.empty


def test_conference_track_manager_allocate_talks():
    "models.ConferenceTrackManager.allocate_talks() fills up multiple tracks automatically"

    conference, scheduled = create_conference_and_schedule_talks(default_proposed_talks)

    # The conference should have 3 tracks
    conference.tracks.should.have.length_of(3)

    # And scheduled a total of 19 talks
    scheduled.should.have.length_of(19)


def test_conference_track_manager_to_lines():
    "models.ConferenceTrackManager.to_lines() outputs the entire conference schedule"

    conference, scheduled = create_conference_and_schedule_talks(default_proposed_talks)

    conference.to_lines().should.equal([
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
        '05:00PM Networking Event',
        'Track 2:',
        '09:00AM Woah 30min',
        '09:40AM Sit Down and Write 30min',
        '10:20AM Pair Programming vs Noise 45min',
        '11:15AM Clojure Ate Scala (on my project) 45min',
        '12:00PM Lunch',
        '01:00PM Rails Magic 60min',
        '02:10PM Ruby on Rails: Why We Should Move On 60min',
        '03:20PM Programming in the Boondocks of Seattle 30min',
        '04:00PM Ruby vs. Clojure for Back-End Development 30min',
        '05:00PM Networking Event',
        'Track 3:',
        '09:00AM Ruby on Rails Legacy App Maintenance 60min',
        '10:10AM A World Without HackerNews 30min',
        '10:50AM User Interface CSS in Rails Apps 30min',
        '12:00PM Lunch',
        '05:00PM Networking Event'
    ])
