# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: protos/get_by_id.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
)

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


class EcgLeadName(betterproto.Enum):
    UNSPECIFIED = 0
    I = 1
    II = 2
    III = 3
    aVR = 4
    aVL = 5
    aVF = 6
    V1 = 7
    V2 = 8
    V3 = 9
    V4 = 10
    V5 = 11
    V6 = 12


@dataclass(eq=False, repr=False)
class GetByIdRequest(betterproto.Message):
    transaction_id: str = betterproto.string_field(1)
    record_id: int = betterproto.int32_field(2)
    sample_rate: int = betterproto.int32_field(3)


@dataclass(eq=False, repr=False)
class GetByIdResponse(betterproto.Message):
    transaction_id: str = betterproto.string_field(1)
    ecg: "Ecg" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class DiagnosticCode(betterproto.Message):
    scp_code: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    confidence: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class Ecg(betterproto.Message):
    record_name: str = betterproto.string_field(1)
    sample_rate: int = betterproto.int32_field(2)
    leads: List["EcgLead"] = betterproto.message_field(3)
    record_id: str = betterproto.string_field(4)
    age: int = betterproto.int32_field(5)
    sex: str = betterproto.string_field(6)
    database_name: str = betterproto.string_field(7)
    diagnostic_code: List["DiagnosticCode"] = betterproto.message_field(8)


@dataclass(eq=False, repr=False)
class EcgLead(betterproto.Message):
    lead_name: "EcgLeadName" = betterproto.enum_field(1)
    signals: List[float] = betterproto.float_field(2)


class GetByIdServiceStub(betterproto.ServiceStub):
    async def get_by_id(
        self,
        get_by_id_request: "GetByIdRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetByIdResponse":
        return await self._unary_unary(
            "/get_by_id_service.GetByIdService/GetById",
            get_by_id_request,
            GetByIdResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class GetByIdServiceBase(ServiceBase):
    async def get_by_id(self, get_by_id_request: "GetByIdRequest") -> "GetByIdResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_get_by_id(
        self, stream: "grpclib.server.Stream[GetByIdRequest, GetByIdResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_by_id(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/get_by_id_service.GetByIdService/GetById": grpclib.const.Handler(
                self.__rpc_get_by_id,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetByIdRequest,
                GetByIdResponse,
            ),
        }