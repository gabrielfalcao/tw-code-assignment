# -*- coding: utf-8 -*-
from itertools import chain
from datetime import timedelta
from collections import OrderedDict

from .dateutils import parse_time
from .dateutils import format_time

from .engine.readers import TextReader


class Model(object):
    __fields__ = ()

    def __init__(self, *args, **properties):
        arguments = list(args)

        data = OrderedDict()
        fields = OrderedDict(self.__fields__)

        for name in fields.keys():
            cast = fields.get(name, None)

            value = properties.get(
                name, arguments and arguments.pop(0) or None)

            if value is not None:
                value = cast(value)
            else:
                value = cast()

            data[name] = value
            setattr(self, name, value)

        self.data = data
        self.initialize(**data)

    def initialize(self, **cast_fields):
        pass

    def __repr__(self):
        name = self.__class__.__name__
        fields = ", ".join(["{0}={1}".format(k, repr(v))
                            for k, v in self.data.items()])
        return '{name}({fields})'.format(**locals())

    def to_dict(self):
        return dict([(k, v) for k, v in self.data.items()])


class Talk(Model):
    __fields__ = (
        ('description', unicode),
        ('duration', lambda duration: duration ==
         'lightning' and 5 or int(duration)),
    )

    def is_lightning(self):
        return self.duration == 5


class TalkList(list):

    def __init__(self, *talks):
        super(TalkList, self).__init__(
            [t for t in talks if isinstance(t, Talk)])

    @classmethod
    def from_text(cls, multiline_string):
        lines = multiline_string.strip().splitlines()
        reader = TextReader()
        return cls(*[Talk(**data) for data in reader.read_multiline(lines)])


class Session(Model):
    __fields__ = (
        ('starts_at', parse_time),
        ('ends_at', parse_time),
    )

    def initialize(self, starts_at, ends_at):
        start, end = self.starts_at, self.ends_at

        self.talks = OrderedDict()
        self.next_slot = start
        self.available_minutes = (end - start).seconds / 60

    @property
    def start_time(self):
        return format_time(self.starts_at)

    @property
    def end_time(self):
        return format_time(self.ends_at)

    def allocate_talks(self, talks):
        remaining = TalkList()
        number_of_lightning_talks = 0
        for talk in talks:
            duration = talk.duration

            if talk.is_lightning():
                if number_of_lightning_talks == 9:
                    number_of_lightning_talks = 0
                    duration += 10

                else:
                    number_of_lightning_talks += 1
            else:
                number_of_lightning_talks = 0

            if self.available_minutes < duration:
                remaining.append(talk)
                continue

            if not talk.is_lightning():
                duration += 10

            humanized_next_slot = self.next_slot.strftime("%I:%M%p")
            self.talks[humanized_next_slot] = talk

            self.available_minutes -= duration
            self.next_slot = self.next_slot + timedelta(minutes=duration)

        return TalkList(*self.talks.values()), remaining

    def to_lines(self):
        lines = []
        for start_time, talk in self.talks.items():
            description = talk.description
            duration = talk.duration == 5 and 'lightning' or '{}min'.format(
                talk.duration)
            lines.append(
                '{start_time} {description} {duration}'.format(**locals()))

        return lines


class Track(Model):
    __fields__ = (
        ('number', int),
    )

    def initialize(self, number):
        self.morning_session = Session(
            starts_at='09:00AM',
            ends_at='12:00PM',
        )
        self.afternoon_session = Session(
            starts_at='01:00PM',
            ends_at='05:00PM',
        )

    def allocate_talks(self, talks):
        allocated = TalkList()

        morning, remaining = self.morning_session.allocate_talks(list(talks))
        afternoon, remaining = self.afternoon_session.allocate_talks(
            list(remaining))

        allocated.extend(morning)
        allocated.extend(afternoon)

        return allocated, remaining

    def to_lines(self):
        lines = ['Track {}:'.format(self.number)]

        # morning talks
        lines.extend(self.morning_session.to_lines())

        # lunch break
        lines.append('12:00PM Lunch')

        # afternoon talks
        lines.extend(self.afternoon_session.to_lines())

        # networking event
        lines.append('05:00PM Networking Event')

        return lines


class ConferenceTrackManager(Model):
    __fields__ = (
        ('name', unicode),
        ('tracks', list),
    )

    def initialize(self, name, tracks=None):
        if not tracks:
            self.tracks = []

    def schedule_talks(self, talks):
        scheduled = TalkList()
        talks_remaining = talks

        while talks_remaining:
            current_track = Track(len(self.tracks) + 1)
            self.tracks.append(current_track)
            allocated, talks_remaining = current_track.allocate_talks(talks_remaining)
            scheduled.extend(allocated)

        return scheduled

    def to_lines(self):
        return list(chain(*[track.to_lines() for track in self.tracks]))
