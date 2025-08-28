import json
from .common.schema import Lead

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