# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from remoteid import remoteid_pb2 as remoteid_dot_remoteid__pb2


class RemoteIDStub(object):
    """RemoteID service exposes methods for the remote identification of aerial
    operations.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MonitorArea = channel.unary_stream(
                '/remoteid.RemoteID/MonitorArea',
                request_serializer=remoteid_dot_remoteid__pb2.MonitorAreaParameters.SerializeToString,
                response_deserializer=remoteid_dot_remoteid__pb2.MonitorAreaResponse.FromString,
                )


class RemoteIDServicer(object):
    """RemoteID service exposes methods for the remote identification of aerial
    operations.
    """

    def MonitorArea(self, request, context):
        """EXPERIMENTAL: API subject to change
        MonitorArea monitors a given area for active operations.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RemoteIDServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MonitorArea': grpc.unary_stream_rpc_method_handler(
                    servicer.MonitorArea,
                    request_deserializer=remoteid_dot_remoteid__pb2.MonitorAreaParameters.FromString,
                    response_serializer=remoteid_dot_remoteid__pb2.MonitorAreaResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'remoteid.RemoteID', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RemoteID(object):
    """RemoteID service exposes methods for the remote identification of aerial
    operations.
    """

    @staticmethod
    def MonitorArea(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/remoteid.RemoteID/MonitorArea',
            remoteid_dot_remoteid__pb2.MonitorAreaParameters.SerializeToString,
            remoteid_dot_remoteid__pb2.MonitorAreaResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
