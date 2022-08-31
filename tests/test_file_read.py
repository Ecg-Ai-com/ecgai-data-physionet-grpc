import json
import pathlib
import uuid

import pytest
from ecgai_data_physionet.models.ecg import EcgRecord

from tests.builder_factory import setup_test_record_data, single_valid_json_record_path_name
from tests.methods import count_files


@pytest.mark.parametrize("record_path_name", single_valid_json_record_path_name)
# @pytest.mark.asyncio
def test_read_from_json(record_path_name):
    record = setup_test_record_data(path_name=record_path_name)
    assert type(record) is EcgRecord


#
@pytest.mark.parametrize("record_path_name", single_valid_json_record_path_name)
def test_write_to_json(record_path_name, tmp_path):
    record = setup_test_record_data(path_name=record_path_name)
    json_value = record.json(by_alias=True)

    file_name = record.record_name + ".json"
    file_path = pathlib.Path(tmp_path, file_name)
    # cleanup_test_json_data(file_name=file_name)
    with open(file_path, "w") as outfile:
        json.dump(json_value, outfile)

    assert count_files(path=tmp_path, name="*.json") == 1
#
#
# @pytest.mark.parametrize("record_path_name", valid_json_record_path_name)
# def test_write_draw_ecg_plot_request_to_ecgai_file(record_path_name, tmp_path):
#     record = setup_test_record_data(path_name=record_path_name)
#     ecg = Ecg()
#     ecg.record_name = record.record_name
#     ecg.sample_rate = record.sample_rate
#     for lead in record.leads:
#         input_lead = EcgLead()
#         # ecg.leads.add()
#         input_lead.lead_name = lead.lead_name.value
#         ecg.leads.append(input_lead)
#         for sig in lead.signal:
#             input_lead.signals.append(sig)
#
#     transaction_id = str(uuid.uuid4())
#     request = DrawEcgPlotRequest()
#     request.transaction_id = transaction_id
#     request.color_style = ColorStyle.COLOR
#     request.artifact = Artifact.NONE
#     request.show_grid = True
#     request.ecg = ecg
#
#     file_name = record.record_name + "_request.ecgai"
#     file_path = pathlib.Path(tmp_path, file_name)
#
#     with open(file_path, "w") as outfile:
#         outfile.write(request.to_json())
#
#     assert count_files(path=tmp_path, name="*.ecgai") == 1
#
#
# @pytest.mark.parametrize("record_path_name", valid_json_record_path_name)
# def test_create_ecg_from_old_json_format(record_path_name, tmp_path):
#     record = setup_test_record_data(path_name=record_path_name)
#     ecg = Ecg()
#     ecg.record_name = record.record_name
#     ecg.sample_rate = record.sample_rate
#     for lead in record.leads:
#         input_lead = EcgLead()
#         # ecg.leads.add()
#         input_lead.lead_name = lead.lead_name.value
#         ecg.leads.append(input_lead)
#         for sig in lead.signal:
#             # voltage = EcgVoltage()
#             # # input_lead.signals.add()
#             # voltage.voltage = sig
#             input_lead.signals.append(sig)
#             # voltage.order = order
#         print(input_lead.lead_name)
#         print(f"Number of signals {len(input_lead.signals)}")
#         assert len(input_lead.signals) == 5000
#     assert ecg.sample_rate == record.sample_rate
#     assert ecg.record_name == record.record_name
#
#     file_name = record.record_name + ".ecgai"
#     file_path = pathlib.Path(tmp_path, file_name)
#
#     with open(file_path, "w") as outfile:
#         outfile.write(ecg.to_json())
#
#     assert count_files(path=tmp_path, name="*.ecgai") == 1
#
#     # with open('test_data/00001_hr.ecgai', "x") as f:
#     #     l = ecg.to_json()
#     #     f.write(ecg.to_json())
#
#
# @pytest.mark.parametrize("record_path_name", valid_ecgai_record_path_name)
# def test_read_ecg_from_file(record_path_name):
#     ecg = Ecg()
#     file_path = pathlib.Path(ROOT_DIR, record_path_name)
#     with open(file_path, "r") as f:
#         ecg.from_json(f.read())
#
#     assert ecg.record_name == "00001_hr" or ecg.record_name == "10001_hr"
#     assert ecg.sample_rate == 500
#     assert len(ecg.leads) == 12
#     for lead in ecg.leads:
#         assert len(lead.signals) == 5000
