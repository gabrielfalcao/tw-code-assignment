from tw_conference_manager.models import Talk
from tw_conference_manager.models import TalkList
from tests.unit.fixtures import TEST_INPUT


def test_talk_list_from_text():
    "models.TalkList.from_text() should parse lines into Talk model instances"

    # Given that I call TalkList.from_text() with a fixture
    talks = TalkList.from_text(TEST_INPUT)

    # Then it should returned a TalkList
    talks.should.be.a(TalkList)

    # And it should have parsed 19 items
    talks.should.have.length_of(19)

    # And every item should be a Talk instance
    [item.should.be.a(Talk) for item in talks]
