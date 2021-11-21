from common import NotImplementedError
from pygame import Surface


class ClientBaseTask:
    def update(self, data: dict, screen:  Surface) -> None:
        raise NotImplementedError

    def get_data(self, keys) -> dict:
        raise NotImplementedError
