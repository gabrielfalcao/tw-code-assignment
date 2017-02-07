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

    allocated.should.have.length_of(8)
    remaining.should.have.length_of(11)
    allocated.should.equal(TalkList(
        Talk(description=u'Writing Fast Tests Against Enterprise Rails', duration=60),
        Talk(description=u'Overdoing it in Python', duration=45),
        Talk(description=u'Lua for the Masses', duration=30),
        Talk(description=u'Ruby Errors from Mismatched Gem Versions', duration=45),
        Talk(description=u'Common Ruby Errors', duration=45),
        Talk(description=u'Rails for Python Developers', duration=5),
        Talk(description=u'Communicating Over Distance', duration=60),
        Talk(description=u'Accounting-Driven Development', duration=45)
    ))
    remaining.should.equal(TalkList(
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
