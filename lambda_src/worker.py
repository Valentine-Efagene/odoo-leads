import json
from .common.schema import Lead
from .auth.auth_service import authenticate
from .user.user_service import getByEmail, getByPhoneNumber, save

def handler(event, context):
    print('Event: ',event)
    
    for record in event["Records"]:
        body = record["body"]
        print(f"Processing message: {body}")
        data = json.loads(body)
        lead = Lead(**data)
        print(f"✅ Processed lead: {lead}")
        uuid = authenticate()
        foundByEmail = getByEmail(lead.email)

        if(foundByEmail):
            return {"statusCode": 200}

        foundByPhone = getByPhoneNumber(lead.phone)

        if(foundByPhone):
            return {"statusCode": 200}

        save(lead=lead)

    return {"statusCode": 200}