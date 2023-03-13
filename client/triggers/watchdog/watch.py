#!/usr/bin/env python
import os
import time
import logging

from watchdog.observers import Observer
from watchdog.events import (
    LoggingEventHandler,
    RegexMatchingEventHandler,
    FileCreatedEvent,
    EVENT_TYPE_CREATED,
)

from unity_on_demand_client import Client
from unity_on_demand_client.api.test import echo
from unity_on_demand_client.api.on_demand_v0_1_0 import (
    create_prewarm_request,
    get_prewarm_request,
    cancel_prewarm_request,
)


# create client
client = Client(base_url="http://localhost:8000")


class MyHandler(RegexMatchingEventHandler):
    def on_created(self, event):
        logging.info(f"In MyHandler: {event}")
        r = create_prewarm_request.sync_detailed(client=client, node_count=COUNTER)
        logging.info(f"response: {r}")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    watch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
    if not os.path.isdir(watch_dir):
        os.makedirs(watch_dir)
    observer = Observer()
    my_handler = MyHandler(
        regexes=[r".*/NISAR_.+?\.h5$"], ignore_directories=True, case_sensitive=True
    )
    observer.schedule(my_handler, watch_dir, recursive=True)
    # logging_handler = LoggingEventHandler()
    # observer.schedule(logging_handler, watch_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
