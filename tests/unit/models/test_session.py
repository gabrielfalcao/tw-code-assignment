from tw_conference_manager.models import Session
from tw_conference_manager.models import Talk


def test_session_allocate_talks():
    "models.Session contains a list of talks"
    short_talk = Talk('Short Talk', 30)
    medium_talk = Talk('Medium Talk', 45)
    long_talk = Talk('Long Talk', 60)
    lightning_talk = Talk('Lightning', 'lightning')

    short_session = Session(
        starts_at='9:00AM',
        ends_at='10:30AM',
    )

    allocated, remaining = short_session.allocate_talks([
        long_talk,
        medium_talk,
        short_talk,
        lightning_talk,
    ])

    allocated.should.equal([
        long_talk,
        short_talk,
    ])

    remaining.should.equal([
        medium_talk,
        lightning_talk
    ])
