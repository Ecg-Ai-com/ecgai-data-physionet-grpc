from ecgai_data_physionet.models.ecg import EcgRecord

from ecgai_data_physionet_grpc.get_by_id_service import GetByIdResponse, Ecg, EcgLead


def to_get_by_id_response(record: EcgRecord, transaction_id: str) -> GetByIdResponse:
    ecg = Ecg()
    ecg.record_id= record.record_id
    ecg.record_name = record.record_name
    ecg.sample_rate = record.sample_rate
    for lead in record.leads:
        input_lead = EcgLead()
        # ecg.leads.add()
        input_lead.lead_name = lead.lead_name
        ecg.leads.append(input_lead)
        for sig in lead.signal:
            input_lead.signals.append(sig)

    return GetByIdResponse(transaction_id=transaction_id,ecg=ecg)

