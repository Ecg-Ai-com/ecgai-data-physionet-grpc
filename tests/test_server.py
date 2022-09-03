import asyncio
import uuid

import pytest
from ecgai_data_physionet_grpc.get_by_id_service import GetByIdRequest, GetByIdResponse
from ecgai_data_physionet_grpc.server import EcgDrawingServer
from grpclib import GRPCError
from grpclib.client import Channel
from grpclib.health.v1.health_grpc import HealthStub
from grpclib.health.v1.health_pb2 import HealthCheckRequest


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


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.asyncio
async def test_get_by_id_with_valid_request():
    server = EcgDrawingServer()
    # asyncio.ensure_future(server.run())
    transaction_id = str(uuid.uuid4())
    record_id = 1

    request = GetByIdRequest(transaction_id=transaction_id, record_id=record_id, sample_rate=500);
    response = await server.get_by_id(request)
    assert type(response) is GetByIdResponse
    assert response.transaction_id == transaction_id
    assert response.ecg.record_id == record_id


@pytest.mark.asyncio
async def test_get_by_id_with_invalid_id_request():
    server = EcgDrawingServer()
    # asyncio.ensure_future(server.run())
    transaction_id = str(uuid.uuid4())
    record_id = 600000000
    request = GetByIdRequest(transaction_id=transaction_id, record_id=record_id, sample_rate=500);
    with pytest.raises(GRPCError):
        _ = await server.get_by_id(request)


@pytest.mark.asyncio
async def test_get_by_id_with_invalid_sample_rate_request():
    server = EcgDrawingServer()
    # asyncio.ensure_future(server.run())
    transaction_id = str(uuid.uuid4())
    record_id = 1
    request = GetByIdRequest(transaction_id=transaction_id, record_id=record_id, sample_rate=499);
    with pytest.raises(GRPCError):
        _ = await server.get_by_id(request)

