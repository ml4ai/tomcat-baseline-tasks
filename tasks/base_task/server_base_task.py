from common import NotImplementedError


class ServerBaseTask:
    def update(self) -> None:
        raise NotImplementedError

    @property
    def data(self) -> dict:
        raise NotImplementedError
