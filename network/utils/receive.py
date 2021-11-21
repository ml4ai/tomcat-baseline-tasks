import json
from select import select
from typing import Optional

from common import HEADER


def receive(senders: list, wait_time: Optional[float] = None) -> list:
    senders, _, exceptional = select(senders, [], senders, wait_time)

    if exceptional:
        raise RuntimeError("Connection lost")

    data = []

    for connection in senders:
        message = connection.recv(HEADER)
        message = json.loads(message.decode('utf-8'))
        data.append(message)

    return data
