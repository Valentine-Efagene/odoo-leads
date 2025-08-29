import json
from .common.schema import Lead
from .auth.auth_service import authenticate
from .user.user_service import getByEmail, getByPhoneNumber, save


def handler(event, context):
    print("Event: ", event)

    for record in event["Records"]:
        body = record["body"]
        print(f"Processing message: {body}")
        data = json.loads(body)
        lead = Lead(**data)
        lead.name = f"{lead.firstName} {lead.lastName}"
        print(f"✅ Processed lead: {lead}")
        uid = authenticate()

        if uid == None:
            return {"statusCode": 401}

        foundByEmail = getByEmail(lead.email, uid=uid)

        if foundByEmail:
            return {"statusCode": 200}

        foundByPhone = getByPhoneNumber(lead.phone, uid=uid)

        if foundByPhone:
            return {"statusCode": 200}

        save(lead=lead, uid=uid)

    return {"statusCode": 200}
