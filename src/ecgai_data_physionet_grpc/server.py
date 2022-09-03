import asyncio

from ecgai_data_physionet.exceptions import FileNotDownloadedError, InValidRecordError, InValidSampleRateError
from ecgai_data_physionet.ptbxl import PtbXl
from grpclib import GRPCError, Status
from grpclib.health.service import Health
from grpclib.server import Server

from ecgai_data_physionet_grpc.get_by_id_service import GetByIdServiceBase, GetByIdRequest, GetByIdResponse
from ecgai_data_physionet_grpc.mapper import to_get_by_id_response


class EcgDrawingServer(GetByIdServiceBase):
    _server: Server
    host: str
    port: int

    def __init__(self, host: str = "localhost", port: int = 45210):
        self._server = Server([self, Health()])
        self.host = host
        self.port = port

    async def run(
            self,
    ):
        await self._server.start(host=self.host, port=self.port)
        print("")
        print(f"Serving on {self.host}:{self.port}")
        # asyncio.ensure_future(self._server.wait_closed())
        await self._server.wait_closed()

    def stop(self):
        print("server closing down")
        self._server.close()

    async def get_by_id(self, get_by_id_request: GetByIdRequest) -> GetByIdResponse:
        sut = PtbXl()
        try:
            record = await sut.get_record(record_id=get_by_id_request.record_id,
                                          sample_rate=get_by_id_request.sample_rate)
            return to_get_by_id_response(record=record, transaction_id=get_by_id_request.transaction_id)
        except (FileNotDownloadedError, InValidRecordError, InValidSampleRateError) as e:
            raise GRPCError(status=Status.INVALID_ARGUMENT, message=str(e))


async def main():
    s = EcgDrawingServer()
    # asyncio.ensure_future(s.run())
    await s.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # do nothing here
        print("Hello user you have pressed ctrl-c button.")
