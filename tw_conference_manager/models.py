class Talk(object):
    def __init__(self, description, duration):
        self.description = description
        self.duration = duration == 'lightning' and 5 or int(duration)
