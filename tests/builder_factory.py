import json
import pathlib

from definitions import ROOT_DIR
from ecgai_data_physionet.models.ecg import EcgRecord

valid_json_record_path_name = {
    "tests/test_data/00001_hr.json",
    "tests/test_data/10001_hr.json",
}

single_valid_json_record_path_name = {
    "tests/test_data/00001_hr.json",
}
#
# valid_ecgai_record_path_name = {
#     "tests/test_data/00001_hr.ecgai",
#     "tests/test_data/10001_hr.ecgai",
# }
# valid_draw_ecg_plot_request_record_path_name = {
#     "tests/test_data/00001_hr_request.ecgai",
#     "tests/test_data/10001_hr_request.ecgai",
# }


def setup_test_record_data(path_name: str) -> EcgRecord:
    record_path = pathlib.Path(ROOT_DIR, path_name)
    with open(record_path) as json_file:
        data = json.load(json_file)
    record = EcgRecord.from_json(data)
    assert type(record) is EcgRecord
    return record

#
# def load_draw_ecg_plot_request_from_disk(path_name) -> DrawEcgPlotRequest:
#     request = DrawEcgPlotRequest()
#     file_path = pathlib.Path(ROOT_DIR, path_name)
#     with open(file_path, "r") as f:
#         request.from_json(f.read())
#     return request
