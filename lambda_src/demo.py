from worker import handler

if __name__ == "__main__":
    # simulate SQS event
    event = {
        "Records": [
            {
                "messageId": "11111111-1111-1111-1111-111111111111",
                "receiptHandle": "AQEB123...example-handle",
                "body": '{\n  "firstName": "John",\n  "lastName": "Doe",\n  "email": "john.doe@example.com",\n  "phone": "+1-5551234567",\n  "utm": "facebook_ads",\n  "property_type": "Apartment",\n  "payment_option": "Mortgage",\n  "place_of_work": "Acme Corp",\n  "salary_range": "50k-70k",\n  "project_location": "Lagos"\n}',
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1724830200000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1724830201000",
                },
                "messageAttributes": {},
                "md5OfBody": "c8a3d3e2ab...example-md5",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
                "awsRegion": "us-east-1",
            }
        ]
    }

    handler(event, None)
