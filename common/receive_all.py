import json
from select import select
from time import time
from typing import Optional

from common import HEADER


def receive_all(senders: dict, wait_time: Optional[float] = None) -> list:
    data = {}

    waiting_for_senders = list(senders.keys()).copy()

    start_time = time()

    while waiting_for_senders:
        senders_replied, _, exceptional = select(waiting_for_senders, [], waiting_for_senders, 0.01)

        if exceptional:
            raise RuntimeError("Connection lost")

        for connection in senders_replied:
            message = connection.recv(HEADER)

            try:
                message = json.loads(message.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                print("[INFO] JSON failed to decode message")
                continue

            data[senders[connection]] = message

            waiting_for_senders.remove(connection)

        if wait_time is not None and time() - start_time > wait_time:
            break

    return data
