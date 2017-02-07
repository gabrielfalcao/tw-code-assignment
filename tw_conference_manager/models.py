from datetime import timedelta
from collections import OrderedDict

from .dateutils import parse_time


class Model(object):
    def __init__(self, *args, **properties):
        arguments = list(args)

        data = OrderedDict()
        for name, cast in self.__fields__:
            value = properties.get(name, arguments and arguments.pop(0) or None)

            if value is not None:
                data[name] = value
                setattr(self, name, cast(value))

        self.data = data
        self.initialize(**data)

    def initialize(self, **cast_fields):
        pass

    def __repr__(self):
        name = self.__class__.__name__
        fields = ", ".join(["{0}={1}".format(k, repr(v)) for k, v in self.data.items()])
        return '{name}({fields})'.format(**locals())


class Talk(Model):
    __fields__ = (
        ('description', unicode),
        ('duration', lambda duration: duration == 'lightning' and 5 or int(duration)),
    )


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

    def allocate_talks(self, talks):
        remaining = []
        # import ipdb;ipdb.set_trace()
        for talk in talks:
            if self.available_minutes < talk.duration:
                remaining.append(talk)
                continue

            humanized_next_slot = self.next_slot.strftime("%H:%M%p")
            self.talks[humanized_next_slot] = talk
            self.available_minutes -= talk.duration
            self.next_slot = self.next_slot + timedelta(minutes=talk.duration)

        return self.talks.values(), remaining
