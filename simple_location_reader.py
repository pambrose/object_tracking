#!/usr/bin/env python3

import argparse
import logging
import sys
from threading import Thread

from client import LocationClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grpc", required=True, help="gRPC location server hostname")
    args = vars(parser.parse_args())

    logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                        format="%(asctime)s %(name)-10s %(funcName)-10s():%(lineno)i: %(levelname)-6s %(message)s")

    client = LocationClient(args["grpc"])

    Thread(target=client.read_locations).start()

    try:
        while True:
            print("Got location: {0}".format(client.get_xy()))
    except KeyboardInterrupt as e:
        client.stop()
        print("Exiting...")