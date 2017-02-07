# -*- coding: utf-8 -*-

from tw_conference_manager.models import Track
from tw_conference_manager.models import Talk
from tw_conference_manager.models import TalkList
from tw_conference_manager.models import ConferenceTrackManager
from tests.unit.fixtures import TEST_INPUT


def test_track_has_sessions():
    "models.ConferenceTrackManager contains 2 tracks"

    # Given a Track instance
    mgr = ConferenceTrackManager('My Test Conference')

    # When I check its properties
    mgr.should.have.property('name').being.equal('My Test Conference')

    # It should have track instances
    mgr.should.have.property('track1').being.a(Track)
    mgr.should.have.property('track2').being.a(Track)


def test_track_allocate_talks():
    "models.Track.allocate_talks() fills up both morning and afternoon sessions"

    conference = ConferenceTrackManager('TWConf')

    talks = TalkList.from_text(TEST_INPUT)
    allocated, remaining = conference.allocate_talks(talks)

    allocated.should.have.length_of(19)
    remaining.should.have.length_of(0)
    