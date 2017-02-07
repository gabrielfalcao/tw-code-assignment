# -*- coding: utf-8 -*-

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
        for name, cast in self.__fields__:
            value = properties.get(
                name, arguments and arguments.pop(0) or None)

            if value is not None:
                value = cast(value)
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

    def __eq__(self, other):
        return id(self) == id(other) \
            or isinstance(other, self.__class__) \
            and other.to_dict() == self.to_dict()


class Talk(Model):
    __fields__ = (
        ('description', unicode),
        ('duration', lambda duration: duration ==
         'lightning' and 5 or int(duration)),
    )


class TalkList(list):

    def __init__(self, *talks):
        super(TalkList, self).__init__(
            [t for t in talks if isinstance(t, Talk)])

    @classmethod
    def from_text(cls, multiline_string):
        lines = multiline_string.strip().splitlines()
        reader = TextReader()
        return cls(*[Talk(**data) for data in reader.read_multiline(lines)])

    def extend(self, talks):
        for talk in talks:
            if isinstance(talk, Talk) and talk in self:
                continue

            self.append(talk)


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
        for talk in talks:
            if self.available_minutes < talk.duration:
                remaining.append(talk)
                continue

            humanized_next_slot = self.next_slot.strftime("%H:%M%p")
            self.talks[humanized_next_slot] = talk
            self.available_minutes -= talk.duration
            self.next_slot = self.next_slot + timedelta(minutes=talk.duration)

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
        afternoon, remaining = self.morning_session.allocate_talks(
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
    )

    def initialize(self, name):
        self.track1 = Track(1)
        self.track2 = Track(2)

    def allocate_talks(self, talks):
        allocated = TalkList()
        track1, remaining = self.track1.allocate_talks(talks)
        track2, remaining = self.track2.allocate_talks(remaining)

        allocated.extend(track1)
        allocated.extend(track2)

        return allocated, remaining

    def to_lines(self):
        lines = []
        lines.extend(self.track1.to_lines())
        lines.extend(self.track2.to_lines())
        return lines
