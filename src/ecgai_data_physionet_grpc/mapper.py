from ecgai_data_physionet.models.ecg import EcgRecord

from ecgai_data_physionet_grpc.get_by_id_service import GetByIdResponse, Ecg, EcgLead, EcgLeadName


def to_get_by_id_response(record: EcgRecord, transaction_id: str) -> GetByIdResponse:
    ecg = Ecg()
    ecg.record_id = record.record_id
    ecg.record_name = record.record_name
    ecg.sample_rate = record.sample_rate
    for lead in record.leads:
        input_lead = EcgLead()
        name = lead.lead_name
        if name[0] == 'A':
            name = name[:1].lower() + name[1:]
        # name = name[0].lower()
        input_lead.lead_name = EcgLeadName.from_string(name)
        ecg.leads.append(input_lead)
        for sig in lead.signal:
            input_lead.signals.append(sig)

    return GetByIdResponse(transaction_id=transaction_id, ecg=ecg)

#
# def to_lead_name(ecg_name: str) -> EcgLeadName:
#     out = EcgLeadName.from_string()
#     match ecg_name:
#         case 'I':
#             return "Bad request"
#         case 'II':
#             return "Not found"
#         case 'III':
#             return "I'm a teapot"
