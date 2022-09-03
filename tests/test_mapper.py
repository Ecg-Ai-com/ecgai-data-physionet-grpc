import pathlib
import uuid
from random import randbytes

import pytest

from ecgai_data_physionet_grpc.get_by_id_service import GetByIdResponse
from ecgai_data_physionet_grpc.mapper import to_get_by_id_response
from tests.builder_factory import single_valid_json_record_path_name, setup_test_record_data


@pytest.mark.parametrize("record_path_name", single_valid_json_record_path_name)
def test_to_ecg_plot_request(record_path_name):
    transaction_id = str(uuid.uuid4())
    record = setup_test_record_data(path_name=record_path_name)
    sut = to_get_by_id_response(record= record,transaction_id=transaction_id)
    assert type(sut) is GetByIdResponse
    assert sut.transaction_id == transaction_id
    assert sut.ecg.record_id == record.record_id
#     ecg_request = DrawEcgPlotRequest()
#     ecg = Ecg()
#     file_path = pathlib.Path(ROOT_DIR, record_path_name)
#     with open(file_path, "r") as f:
#         ecg.from_json(f.read())
#     transaction_id = str(uuid.uuid4())
#     ecg_request.transaction_id = transaction_id
#     ecg_request.ecg = ecg
#     ecg_request.artifact = Artifact.SALT
#     ecg_request.color_style = ColorStyle.COLOR
#     ecg_request.show_grid = True
#
#     response = to_ecg_plot_request(request=ecg_request)
#
#     assert response.transaction_id == transaction_id
#     assert response.artifact == Artifact.SALT
#     assert response.color_style == ColorStyle.COLOR
#     assert response.show_grid is True
#     assert len(response.ecg_leads.leads) == 12
#
#
# def test_to_draw_ecg_plot_response():
#     transaction_id = str(uuid.uuid4())
#     file_name = "test_file"
#     record_name = "000001"
#     image = randbytes(10000)
#     plot_response = EcgPlotResponse.create(
#         transaction_id=transaction_id, record_name=record_name, file_name=file_name, file_extension=".png", image=image
#     )
#     response = to_draw_ecg_plot_response(plot_response)
#     assert response.transaction_id == transaction_id
#     assert response.record_name == record_name
#     assert response.file_name == file_name
#     assert response.image == image
#     print(image)