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


def test_talk_to_dict():
    "models.Talk should be pre-serializable to a dict"

    model = Talk('A DSL for expressive assertions', 'lightning')

    model.to_dict().should.equal(
        {'description': 'A DSL for expressive assertions', 'duration': 5})


def test_talk_is_lightning():
    "models.Talk.is_lightning() should return True if duration is 5 minutes"

    model = Talk('A DSL for expressive assertions', 'lightning')
    model.is_lightning().should.be.true
    
