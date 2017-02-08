# -*- coding: utf-8 -*-

from tw_conference_manager.models import Talk
from tw_conference_manager.models import Session
from tw_conference_manager.models import TalkList


def test_session_allocate_talks():
    "models.Session.allocate_talks() returns the allocated and the remaining talks"

    short_talk = Talk('Short Talk', 30)
    medium_talk = Talk('Medium Talk', 45)
    long_talk = Talk('Long Talk', 60)
    lightning_talk = Talk('Lightning', 5)

    proposed_talks = TalkList(
        long_talk,
        medium_talk,
        short_talk,
        lightning_talk,
    )

    short_session = Session(
        starts_at='9:00AM',
        ends_at='10:50AM',
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


def test_session_to_lines():
    "models.Session.to_lines() returns a list of lines"

    short_talk = Talk('Short Talk', 30)
    medium_talk = Talk('Medium Talk', 45)
    long_talk = Talk('Long Talk', 60)
    lightning_talk = Talk('Lightning', 5)
    proposed_talks = TalkList(
        long_talk,
        medium_talk,
        short_talk,
        lightning_talk,
    )

    short_session = Session(
        starts_at='9:00AM',
        ends_at='10:50AM',
    )
    short_session.allocate_talks(proposed_talks)
    result = short_session.to_lines()

    result.should.equal([
        '09:00AM Long Talk 60min',
        '10:10AM Short Talk 30min',
    ])


def test_session_to_lines_with_2_regular_talk():
    "Session should have 10-minute breaks between regular talks"

    short_talk = Talk('Short Talk', 30)
    medium_talk = Talk('Medium Talk', 45)
    proposed_talks = TalkList(
        short_talk,
        medium_talk,
    )
    short_session = Session(
        starts_at='9:00AM',
        ends_at='10:25AM',
    )
    short_session.allocate_talks(proposed_talks)
    short_session.to_lines().should.equal([
        '09:00AM Short Talk 30min',
        "09:40AM Medium Talk 45min"
    ])


def test_session_to_lines_with_9_consecutive_lightning():
    "Session should not have breaks between 2 consecutive lightning talks"

    # Given a 30-minute session
    short_session = Session(
        starts_at='9:00AM',
        ends_at='9:30AM',
    )
    # And 2 sequential lightning talks proposed
    proposed_talks = TalkList(*[Talk('Light {0}'.format(i), 'lightning') for i in range(1, 3)])

    # When I allocate_talks the talks
    short_session.allocate_talks(proposed_talks)

    # Then it should have 2 talks without breaks
    short_session.to_lines().should.equal([
        '09:00AM Light 1 lightning',
        "09:05AM Light 2 lightning",
    ])


def test_session_to_lines_with_10_consecutive_lightning():
    "Session should not have breaks between 2 consecutive lightning talks"

    # Given a 50-minute session
    short_session = Session(
        starts_at='9:00AM',
        ends_at='9:50AM',
    )

    # And 10 sequential lightning talks proposed to that session
    proposed_talks = TalkList(*[Talk('Light {0}'.format(i), 'lightning') for i in range(1, 11)])

    # When I allocate the talks
    _, remaining = short_session.allocate_talks(proposed_talks)

    # Then it should have 9 allocated talks
    short_session.to_lines().should.equal([
        '09:00AM Light 1 lightning',
        "09:05AM Light 2 lightning",
        "09:10AM Light 3 lightning",
        "09:15AM Light 4 lightning",
        "09:20AM Light 5 lightning",
        "09:25AM Light 6 lightning",
        "09:30AM Light 7 lightning",
        "09:35AM Light 8 lightning",
        "09:40AM Light 9 lightning",
    ])

    # And one talk should have remained unscheduled
    remaining.should.have.length_of(1)
