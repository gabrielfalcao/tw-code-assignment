# -*- coding: utf-8 -*-

# from tw_conference_manager.models import Track
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
    mgr.should.have.property('tracks').being.a(list)

    # And it should be empty by default
    mgr.tracks.should.be.empty


def test_conference_track_manager_allocate_talks():
    "models.ConferenceTrackManager.allocate_talks() fills up multiple tracks automatically"

    conference = ConferenceTrackManager('TWConf')

    talks = TalkList.from_text(TEST_INPUT)
    scheduled = conference.schedule_talks(talks)

    # The conference should have 3 tracks
    conference.tracks.should.have.length_of(3)

    # And scheduled a total of 19 talks
    scheduled.should.have.length_of(19)


def test_conference_track_manager_to_lines():
    "models.ConferenceTrackManager.to_lines() outputs the entire conference schedule"

    conference = ConferenceTrackManager('TWConf')

    talks = TalkList.from_text(TEST_INPUT)
    scheduled = conference.schedule_talks(talks)

    scheduled.should.have.length_of(19)

    scheduled.should.equal(TalkList(
        Talk(description=u'Writing Fast Tests Against Enterprise Rails', duration=60),
        Talk(description=u'Overdoing it in Python', duration=45),
        Talk(description=u'Lua for the Masses', duration=30),
        Talk(description=u'Rails for Python Developers', duration=5),
        Talk(description=u'Ruby Errors from Mismatched Gem Versions', duration=45),
        Talk(description=u'Common Ruby Errors', duration=45),
        Talk(description=u'Communicating Over Distance', duration=60),
        Talk(description=u'Accounting-Driven Development', duration=45),
        Talk(description=u'Woah', duration=30),
        Talk(description=u'Sit Down and Write', duration=30),
        Talk(description=u'Pair Programming vs Noise', duration=45),
        Talk(description=u'Clojure Ate Scala (on my project)', duration=45),
        Talk(description=u'Rails Magic', duration=60),
        Talk(description=u'Ruby on Rails: Why We Should Move On', duration=60),
        Talk(description=u'Programming in the Boondocks of Seattle', duration=30),
        Talk(description=u'Ruby vs. Clojure for Back-End Development', duration=30),
        Talk(description=u'Ruby on Rails Legacy App Maintenance', duration=60),
        Talk(description=u'A World Without HackerNews', duration=30),
        Talk(description=u'User Interface CSS in Rails Apps', duration=30),
    ))
