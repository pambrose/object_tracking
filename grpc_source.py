import logging
import sys
import thread

from  generic_source import GenericSource
from location_server import LocationServer


class GrpcSource(GenericSource):
    def __init__(self, port):
        GenericSource.__init__(self)
        self._location_server = LocationServer('[::]:' + str(port), self)

    def start(self):
        try:
            thread.start_new_thread(LocationServer.start_server, (self._location_server,))
            logging.info("Started gRPC location server")
        except BaseException as e:
            logging.error("Unable to start gRPC location server [{0}]".format(e))
            sys.exit(1)
