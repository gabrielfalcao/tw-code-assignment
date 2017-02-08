# -*- coding: utf-8 -*-
from itertools import chain
from datetime import timedelta
from collections import OrderedDict

from .dateutils import parse_time
from .dateutils import format_time

from .engine.readers import TextReader


class Model(object):
    """Base model class, provides automatic attribute assignment, provides
    utilities for validating and transforming values of its fields.

    Example:

    ::

        from tw_conference_manager.models import Model

        class Person(Model):
            __fields__ = (
                ('name', unicode),
                ('email', bytes),
            )

        wole = Person('Wole', 'wole@thoughtworks.com')
        assert wole.to_dict() == {
            'name': 'Wole',
            'email': 'wole@thoughtworks.com',
        }
    """
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
        """this method gives an option for subclasses to take action upon
        instantiation.

        In other words this is a post-validation constructor method.
        """
        pass

    def __repr__(self):
        name = self.__class__.__name__
        fields = ", ".join(["{0}={1}".format(k, repr(v))
                            for k, v in self.data.items()])
        return '{name}({fields})'.format(**locals())

    def to_dict(self):
        """returns a :py:class:`dict` containing the model fields"""
        return dict([(k, v) for k, v in self.data.items()])


class Talk(Model):
    """Model for storing basic talk information: description and duration.

    Provides a utility function to check whether the talk is a
    "lightning" one.
    """
    __fields__ = (
        ('description', unicode),
        ('duration', lambda duration: duration ==
         'lightning' and 5 or int(duration)),
    )

    def is_lightning(self):
        """
        :returns: :py:obj:`True` if the duration is `5` or :py:obj:`True`
        """
        return self.duration == 5


class TalkList(list):
    """A subclass of :py:class:`list` with a shortcut method to parse a
    list of strings."""

    def __init__(self, *talks):
        super(TalkList, self).__init__(
            [t for t in talks if isinstance(t, Talk)])

    @classmethod
    def from_text(cls, multiline_string):
        """creates a new :py:class:`TalkList` instance with talks parsed from the given parameter.
        :param multiline_string: a list of strings
        :returns: a new :py:class:`TalkList` with :py:class:`Talk` members
        """
        lines = multiline_string.strip().splitlines()
        reader = TextReader()
        return cls(*[Talk(**data) for data in reader.read_multiline(lines)])


class Session(Model):
    """A model for declaring a session with start and end times.

    Provides utility methods and properties to allocate talks and
    generate human-readable output.
    """
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
        """Fills up an internal schedule with as many talks as possible.

        :returns: a 2-item tuple containing a :py:class:`TalkList`
            with **allocated** talks and another with **remaining** taiks.
        """
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

            humanized_next_slot = format_time(self.next_slot)
            self.talks[humanized_next_slot] = talk

            self.available_minutes -= duration
            self.next_slot = self.next_slot + timedelta(minutes=duration)

        return TalkList(*self.talks.values()), remaining

    def to_lines(self):
        """
        :returns: a human-readable list of strings with the allocated talks.
        """
        lines = []
        for start_time, talk in self.talks.items():
            description = talk.description
            duration = talk.duration == 5 and 'lightning' or '{}min'.format(
                talk.duration)
            lines.append(
                '{start_time} {description} {duration}'.format(**locals()))

        return lines


class Track(Model):
    """Model that contains 2 sessions, one holding a schedule for morning
    sessions and one for afternoon sessions, respectively.
    """
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
        """Fills up an internal schedule with as many talks as possible on
        both morning and afternoon sessions.
        """
        allocated = TalkList()

        morning, remaining = self.morning_session.allocate_talks(list(talks))
        afternoon, remaining = self.afternoon_session.allocate_talks(
            list(remaining))

        allocated.extend(morning)
        allocated.extend(afternoon)

        return allocated, remaining

    def to_lines(self):
        """
        :returns: a human-readable list of strings with the allocated talks.
        """

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
    """Model that takes care of all aspects of scheduling an unlimited
    list of talks into multiple tracks.
    """
    __fields__ = (
        ('name', unicode),
        ('tracks', list),
    )

    def initialize(self, name, tracks=None):
        if not tracks:
            self.tracks = []

    def schedule_talks(self, talks):
        """schedules all given talks into multiple tracks.
        :param talks: a :py:class:`TalkList` with :py:class:`Talk` instances
        :returns: a :py:class:`TalkList` with all tracks currently scheduled
        """
        scheduled = TalkList()
        talks_remaining = talks

        while talks_remaining:
            current_track = Track(len(self.tracks) + 1)
            self.tracks.append(current_track)
            allocated, talks_remaining = current_track.allocate_talks(talks_remaining)
            scheduled.extend(allocated)

        return scheduled

    def to_lines(self):
        """
        :returns: a human-readable list of strings with the currently scheduled talks.
        """
        return list(chain(*[track.to_lines() for track in self.tracks]))
