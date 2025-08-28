import os
import json
from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, StringConstraints

class Lead(BaseModel):
    email: EmailStr
    phone: Annotated[str, StringConstraints(pattern=r"^\+?\d{1,4}-\d+$")]  # e.g. +234-8012345678

    # optional fields
    utm: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    property_type: Optional[str] = None
    payment_option: Optional[str] = None
    place_of_work: Optional[str] = None
    salary_range: Optional[str] = None
    project_location: Optional[str] = None

def handler(event, context):
    print('Event: ',event)
    # event contains a batch of SQS messages
    for record in event["Records"]:
        body = record["body"]
        print(f"Processing message: {body}")
        data = json.loads(body)
        lead = Lead(**data)
        print(f"✅ Processed lead: {lead}")
        # Your business logic goes here

    return {"statusCode": 200}