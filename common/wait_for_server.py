from network import receive, send


def wait_for_server(to_server, from_server):
    data = {}
    data["type"] = "status"
    data["status"] = "ready"

    send([to_server], data)

    [data] = receive([from_server])
    if not (data["type"] == "request" and data["request"] == "start"):
        raise RuntimeError("Cannot parse request from server")
