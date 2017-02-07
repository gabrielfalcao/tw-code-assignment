# -*- coding: utf-8 -*-

from tw_conference_manager.models import Talk
from tw_conference_manager.models import Session
from tw_conference_manager.models import TalkList


def test_session_allocate_talks():
    "models.Session contains a list of talks"

    short_talk = Talk('Short Talk', 30)
    medium_talk = Talk('Medium Talk', 45)
    long_talk = Talk('Long Talk', 60)
    lightning_talk = Talk('Lightning', 'lightning')
    proposed_talks = TalkList(
        long_talk,
        medium_talk,
        short_talk,
        lightning_talk,
    )

    short_session = Session(
        starts_at='9:00AM',
        ends_at='10:30AM',
    )
    allocated, remaining = short_session.allocate_talks(proposed_talks)

    allocated.should.equal(TalkList(
        long_talk,
        short_talk,
    ))

    remaining.should.equal(TalkList(
        medium_talk,
        lightning_talk
    ))
