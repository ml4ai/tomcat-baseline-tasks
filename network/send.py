import json
from select import select
from typing import Optional

from common import HEADER


def send(receivers: list, payload, wait_time: Optional[float] = None) -> None:
    _, receivers, exceptional = select([], receivers, receivers, wait_time)

    if exceptional:
        raise RuntimeError("Connection lost")

    if receivers:
        # Convert payload into json string and encode it
        payload_msg = json.dumps(payload).encode('utf-8')

        # Pad the json string to specific data length
        payload_msg += b' ' * (HEADER - len(payload_msg))

        for connection in receivers:
            connection.send(payload_msg)
