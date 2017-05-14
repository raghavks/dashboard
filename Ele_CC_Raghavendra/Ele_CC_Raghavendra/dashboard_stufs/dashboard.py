import json
import re
from datetime import datetime
from dateutil import parser


def read_json():
    """
    description:read sms json data from file
    :return: json data
    """
    with open('Ele_CC_Raghavendra/static/json/SMSBackUp.json') as jsonfolder:
        content = json.load(jsonfolder)
        return content


def distinct_number():
    """
    description: fetch distinct phone numbers
    :return: distinct phone numbers
    """
    distinct_numbers = []
    for i in read_json():
        distinct_numbers.append(i["number"])
    return set(distinct_numbers)


def filter_by_number():
    """
    description :group by telephone number
    :return: list of group by numbers
    """
    data = read_json()
    filter_list = []
    for i in distinct_number():
        filter_list.append(list(filter(lambda record: record['number'] == i, data)))
    return filter_list


def service_type(single_dict):
    """
    description: identify service type of sms based on text mgs i,e mgs from cab or bank or others
    :param single_dict: 
    :return: 
    """
    s_type = None
    if re.search(r'Uber|GrabTaxi|Ola|Didi Kuaidi|Hailo|Line Taxi|Blue Bird', single_dict['text'], re.IGNORECASE):
        s_type = "Cab"
    elif re.search(r'bank|bnk|Deposit|chq No|debit|credit', single_dict['text'], re.IGNORECASE):
        s_type = "Bank"
    else:
        s_type = "Other"
    return s_type


def sms_type(single_dict):
    """
    description: identify type of msg i,e either promotional or normal msg
    :param single_dict: 
    :return: 
    """
    s_type = None
    if re.search(r'Our team wishes you|http|discount|voucher|valid|promo|offers|off|sms|coupon', single_dict['text'], re.IGNORECASE):
            # s = datetime.strptime('9:00', '%H:%M')
            # e = datetime.strptime('21:00', '%H:%M')
            # obj=parser.parse(single_dict['datetime'])
        s_type = "Promotional"
        #     if obj.time() >= s.time() and obj.time() <= e.time():
        #         s_type = "Promotional"
        #     else:
        #         s_type = "Tx SMS"
        # else:
        #     s_type = "Tx SMS"
    else:
        s_type = "Tx SMS"
    return s_type


def service_sms_type():
    """
    description: to identify service and sms type
    :return: 
    """
    res = filter_by_number()
    allresult = []
    m_id = 0
    for listvalue in res:
        total = 0

        pcount = 0
        tcount = 0
        s_type = "Other"
        number = None
        status_global = []
        single_sms_track = []
        s_id = 0
        for j in listvalue:
            number = j['number']
            total = total+1
            s_type = service_type(j)
            obj = parser.parse(j['datetime'])
            val = re.sub(r':', r'.', str((obj.time()))[:4])
            val = float(val)
            if sms_type(j) == "Promotional":
                pcount = pcount+1
                single_sms_track.append({"Id": s_id, "Number": j['number'], "Val": val, "SMS_Type": "Promotional", "SMS": j['text'], "Date": j["datetime"]})
            else:
                single_sms_track.append(
                    {"Id": s_id, "Number": j['number'], "SMS_Type": "Txt SMS", "Val": val, "SMS": j['text'], "Date": j["datetime"]})
                tcount = tcount+1
            s_id = s_id+1
        status_global.append(single_sms_track)
        res_dict = {"Id": m_id, "Number": number, "Type": s_type, "Total_SMS": total, "Promotional": pcount, "TxSMS": tcount}
        m_id = m_id+1
        allresult.append([res_dict, status_global])

    return allresult
