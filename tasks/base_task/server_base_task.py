from common import NotImplementedError


class ServerBaseTask:
    def __init__(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    @property
    def data():
        raise NotImplementedError
