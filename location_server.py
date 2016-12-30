import logging
import time
from threading import Lock

import grpc
from concurrent import futures

from gen.grpc_server_pb2 import ObjectLocation
from gen.grpc_server_pb2 import ObjectLocationServerServicer
from gen.grpc_server_pb2 import ServerInfo
from gen.grpc_server_pb2 import add_ObjectLocationServerServicer_to_server
from generic_server import GenericServer


class LocationServer(ObjectLocationServerServicer, GenericServer):
    def __init__(self, port):
        super(LocationServer, self).__init__(port)
        self._cnt_lock = Lock()

    def registerClient(self, request, context):
        logging.info("Connected to client {0} [{1}]".format(context.peer(), request.info))
        with self._cnt_lock:
            self._invoke_cnt += 1
        return ServerInfo(info="Server invoke count {0}".format(self._invoke_cnt))

    def getObjectLocations(self, request, context):
        client_info = request.info
        return self._currval_generator(context.peer())

    def write_location(self, x, y, width, height, middle_inc):
        if not self._stopped:
            self._set_currval(ObjectLocation(id=self._id,
                                             x=x,
                                             y=y,
                                             width=width,
                                             height=height,
                                             middle_inc=middle_inc))
            self._id += 1

    def start_location_server(self):
        logging.info("Starting gRPC server listening on {0}".format(self._hostname))
        self._grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_ObjectLocationServerServicer_to_server(self, self._grpc_server)
        self._grpc_server.add_insecure_port(self._hostname)
        self._grpc_server.start()
        try:
            while not self._stopped:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
