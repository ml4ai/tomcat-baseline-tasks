from select import select
from time import time
from typing import Optional

from .utils import read_message


def receive_all(senders: dict, wait_time: Optional[float] = None) -> list:
    data = {}

    waiting_for_senders = list(senders.keys()).copy()

    start_time = time()

    while waiting_for_senders:
        senders_replied, _, exceptional = select(waiting_for_senders, [], waiting_for_senders, 0.01)

        if exceptional:
            raise RuntimeError("Connection lost")

        for connection in senders_replied:
            message = read_message(connection)
            if message is None:
                continue

            data[senders[connection]] = message

            waiting_for_senders.remove(connection)

        if wait_time is not None and time() - start_time > wait_time:
            break

    return data
