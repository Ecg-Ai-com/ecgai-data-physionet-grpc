import asyncio
import logging
import logging.config

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
    logger: logging.Logger

    def __init__(self, host: str = "localhost", port: int = 45210):
        self.logger = logging.getLogger("server")
        self._server = Server([self, Health()])
        self.host = host
        self.port = port
        self.logger.debug(f"{__class__.__name__} initializing, host: {self.host}, port:{self.port}")

    async def run(self):
        self.logger.info(f"{__class__.__name__}.run(host: {self.host}, port:{self.port})")

        await self._server.start(host=self.host, port=self.port)

        # asyncio.ensure_future(self._server.wait_closed())
        await self._server.wait_closed()

    def stop(self):
        self.logger.info(f"{__class__.__name__}.stop()")
        self._server.close()

    async def get_by_id(self, get_by_id_request: GetByIdRequest) -> GetByIdResponse:
        self.logger.info(
            f"{__class__.__name__}.get_by_id(transaction_id: {get_by_id_request.transaction_id}, record_id"
            f" {get_by_id_request.record_id}, sample_rate: {get_by_id_request.sample_rate})"
        )
        sut = PtbXl()
        try:
            record = await sut.get_record(
                record_id=get_by_id_request.record_id, sample_rate=get_by_id_request.sample_rate
            )
            return to_get_by_id_response(record=record, transaction_id=get_by_id_request.transaction_id)
        except (FileNotDownloadedError, InValidRecordError, InValidSampleRateError) as e:
            self.logger.exception(f"{__class__.__name__} exception, {str(e)}")
            raise GRPCError(status=Status.INVALID_ARGUMENT, message=str(e))


async def main():  # pragma: no cover
    s = EcgDrawingServer()
    # asyncio.ensure_future(s.run())
    await s.run()


if __name__ == "__main__":  # pragma: no cover
    try:
        logging.config.fileConfig("logging.conf")
        asyncio.run(main())
    except KeyboardInterrupt:
        # do nothing here
        print("Hello user you have pressed ctrl-c button.")
