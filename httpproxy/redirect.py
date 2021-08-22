"""Redirect HTTP requests to another server."""
from mitmproxy import http
import re

PATH_MAPPINGS = [
    r"(?P<path>[^.]+).s3.(?P<region>[^.]+).amazonaws.com"
]

def transform_path(in_path, host):
    print(f"Transform path ({in_path}) from host ({host})")
    for mapping in PATH_MAPPINGS:
        match = re.match(mapping, host)
        if match is not None:
            if in_path == "/":
                return f"/{match.group('path')}"
            else:
                return f"/{match.group('path')}{in_path}"
    return in_path

def request(flow: http.HTTPFlow) -> None:
    # pretty_host takes the "Host" header of the request into account,
    # which is useful in transparent mode where we usually only have the IP
    # otherwise.
    print("Processing requests")
    if flow.request.pretty_host.endswith(".amazonaws.com"):
        print("Forwarding localstack")
        flow.request.path = transform_path(flow.request.path, flow.request.pretty_host)
        flow.request.host = "localstack"
        flow.request.port = 4566
