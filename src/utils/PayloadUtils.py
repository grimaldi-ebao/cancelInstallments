from src.utils.RestUtils import post_request


# "ArapStatus": "1"

def arap_endo_query_payload(business_no):
    query_payload = {
        "Conditions": {
            "EndoNo": business_no,
            "ArapStatus": "1"
        },
        "InConditions": {},
        "FromRangeConditions": {},
        "ToRangeConditions": {},
        "PageNo": 1,
        "PageSize": 500,
        "SortField": "ArapId",
        "SortType": "desc"
    }

    return query_payload

def arap_policy_query_payload(business_no):
    query_payload = {
        "Conditions": {
            "PolicyNo": business_no,
            "ArapStatus": "1"
        },
        "InConditions": {},
        "FromRangeConditions": {},
        "ToRangeConditions": {},
        "PageNo": 1,
        "PageSize": 500,
        "SortField": "ArapId",
        "SortType": "desc"
    }

    return query_payload

def arap_update_item(arap_id, arap_no):
    item = {
    "@type": "BcpArap-Arap",
    "ArapId": arap_id,
    "ArapNo": arap_no,
    "ArapStatus": "7"
    }
    return item

def update_arap_status():
    payload = {

    }
    return payload


