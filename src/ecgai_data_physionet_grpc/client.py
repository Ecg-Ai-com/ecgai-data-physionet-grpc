import asyncio
import uuid

from grpclib.client import Channel

from ecgai_data_physionet_grpc.get_by_id_service import (
    GetByIdRequest,
    GetByIdServiceStub,
)


async def main():
    channel = Channel(host="localhost", port=45210)
    client = GetByIdServiceStub(channel)

    transaction_id = str(uuid.uuid4())
    record_id = 1

    request = GetByIdRequest(transaction_id=transaction_id, record_id=record_id, sample_rate=500)
    response = await client.get_by_id(request)
    print(response)
    channel.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # do nothing here
        print("Hello user you have pressed ctrl-c button.")
