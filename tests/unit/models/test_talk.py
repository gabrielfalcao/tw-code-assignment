from tw_conference_manager.models import Talk


def test_talk_properties():
    "models.Talk contains description and duration"

    model = Talk('Top-down TDD in Python with nose and sure', 60)

    model.should.have.property('description').being.equal(
        'Top-down TDD in Python with nose and sure'
    )

    model.should.have.property('duration').being.equal(
        60
    )


def test_talk_lightning_talk():
    "models.Talk accepts the string 'lightning' as duration"

    model = Talk('A DSL for expressive assertions', 'lightning')

    model.should.have.property('description').being.equal(
        'A DSL for expressive assertions'
    )

    model.should.have.property('duration').being.equal(
        5
    )
