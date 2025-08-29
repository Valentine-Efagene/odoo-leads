import json
from common.schema import Lead
from auth.auth_service import authenticate
from user.user_service import getByEmail, getByPhoneNumber, save, update
from user.user_schema import User


def updateDetails(person: User, lead: Lead, uid: str):
    mappings = {
        "name": lead.name,
        "phone": lead.phone,
        "email": lead.email,
    }

    dto = {
        field: value
        for field, value in mappings.items()
        if not getattr(person, field) and value
    }

    if dto:
        print(f"Updating user {person.id} with: {dto}")
        update(id=person.id, dto=dto, uid=uid)
    else:
        print(f"No updates needed for user {person.id}")


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
            person = foundByEmail[0]
            updateDetails(person=person, lead=lead, uid=uid)
            return {"statusCode": 200}

        foundByPhone = getByPhoneNumber(lead.phone, uid=uid)

        if foundByPhone:
            person = foundByPhone[0]
            updateDetails(person=person, lead=lead, uid=uid)
            return {"statusCode": 200}

        save(lead=lead, uid=uid)

    return {"statusCode": 200}
