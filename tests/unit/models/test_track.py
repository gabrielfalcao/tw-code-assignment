# from tw_conference_manager.models import Talk
# from tw_conference_manager.models import Track
# from tw_conference_manager.models import Session


# def test_track_has_sessions():
#     "models.Track contains a morning and an afternoon session"

#     # Given a Track instance
#     track = Track(1)

#     # It should have session instances
#     track.should.have.property('morning_session').being.a(Session)
#     track.should.have.property('afternoon_session').being.a(Session)

#     # And its morning session should start at 9AM and end at noon
#     track.morning_session.start_time.should.equal('09:00AM')
#     track.morning_session.start_time.should.equal('12:00PM')

#     # And its afternoon session should start at 9AM and end at noon
#     track.afternoon_session.start_time.should.equal('01:00PM')
#     track.afternoon_session.end_time.should.equal('5:00PM')


# def test_track_allocate_talks():
#     "models.Track contains a list of talks"

#     track1 = Track(1)

#     talks = TalkList.from_text()
#     allocated, remaining = track1.allocate_talks()

#     allocated.should.equal([
#         long_talk,
#         short_talk,
#     ])

#     remaining.should.equal([
#         medium_talk,
#         lightning_talk
#     ])
