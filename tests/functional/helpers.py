# -*- coding: utf-8 -*-
from tw_conference_manager.models import Talk
from tw_conference_manager.models import TalkList
from tw_conference_manager.models import Session
from tw_conference_manager.models import Track
from tw_conference_manager.models import ConferenceTrackManager


def create_session_and_allocate_talks(starts_at, ends_at, talks):
    session = Session(starts_at, ends_at)
    return session.allocate_talks(talks)


def create_track_and_allocate_talks(talks):
    track = Track(1)
    return track.allocate_talks(talks)


def create_conference_and_schedule_talks(talks):
    conference = ConferenceTrackManager('TW Conf')
    return conference, conference.schedule_talks(talks)


def create_sequence_of_lightning_talks(count, template='Light {0}'):
    return TalkList(*[Talk(template.format(i), 'lightning') for i in range(1, count + 1)])
