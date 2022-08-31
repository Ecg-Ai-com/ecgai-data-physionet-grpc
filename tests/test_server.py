import asyncio

import pytest
from grpclib.client import Channel
from grpclib.health.v1.health_grpc import HealthStub
from grpclib.health.v1.health_pb2 import HealthCheckRequest

from ecgai_data_physionet_grpc.server import EcgDrawingServer


@pytest.mark.asyncio
async def test_run_server():
    server = EcgDrawingServer()
    asyncio.ensure_future(server.run())

    async with Channel(server.host, server.port) as channel:
        stub = HealthStub(channel)
        response = await stub.Check(HealthCheckRequest())
        assert response.SERVING == 1  # '1 == SERVING'
        print(response)
    # print(server.health)
    server.stop()


@pytest.mark.asyncio
async def test_health_check_when_server_has_stopped_throws_connection_refused_error():
    server = EcgDrawingServer()
    asyncio.ensure_future(server.run())
    # delay to ensure server has started correctly
    await asyncio.sleep(delay=0.2)

    server.stop()
    with pytest.raises(ConnectionRefusedError):
        async with Channel(server.host, server.port) as channel:
            stub = HealthStub(channel)
            _ = await stub.Check(HealthCheckRequest())


@pytest.mark.asyncio
async def test_health_check_before_server_has_started_throws_connection_refused_error():
    server = EcgDrawingServer()
    with pytest.raises(ConnectionRefusedError):
        async with Channel(server.host, server.port) as channel:
            stub = HealthStub(channel)
            _ = await stub.Check(HealthCheckRequest())
