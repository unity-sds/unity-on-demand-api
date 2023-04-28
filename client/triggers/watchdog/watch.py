#!/usr/bin/env python
import os
import time
import logging
import argparse

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


class MyHandler(RegexMatchingEventHandler):
    def on_created(self, event):
        logging.info(f"In MyHandler: {event}")
        r = create_prewarm_request.sync_detailed(client=client, node_count=1, additive=True)
        logging.info(f"response: {r}")


def main(client):
    # configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # directory to watch
    watch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
    if not os.path.isdir(watch_dir):
        os.makedirs(watch_dir)

    # create watchdog and apply some regex filters on what to trigger on
    observer = Observer()
    my_handler = MyHandler(
        regexes=[r".*/NISAR_.+?\.h5$"], ignore_directories=True, case_sensitive=True
    )

    # start watching
    observer.schedule(my_handler, watch_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="watch files and trigger OD prewarm call"
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        default="http://localhost:8000",
        help="base url to On-Demand REST API",
    )
    args = parser.parse_args()
    client = Client(base_url=args.url)
    main(client)
