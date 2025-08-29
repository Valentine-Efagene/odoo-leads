import os
from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_sources,
    BundlingOptions,
)
from constructs import Construct


class OdooLeadsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an SQS queue
        queue = sqs.Queue(
            self,
            "OdooLeadsQueue",
            queue_name="OdooLeadsQueue",
            visibility_timeout=Duration.seconds(300),  # must be > lambda timeout
        )

        # Lambda Layer for dependencies
        dependency_layer = _lambda.LayerVersion(
            self,
            "DependenciesLayer",
            code=_lambda.Code.from_asset(
                path="layers/python",
                bundling=BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_11.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install --platform manylinux2014_x86_64 --only-binary=:all: "
                        "-r requirements.txt -t /asset-output/python",
                    ],
                ),
            ),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_11],
        )

        # Lambda function that processes messages
        fn = _lambda.Function(
            self,
            "OdooLeadLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="worker.handler",  # file=worker.py, function=handler
            code=_lambda.Code.from_asset("lambda_src"),  # path to your code
            function_name="OdooLeadLambda",
            timeout=Duration.seconds(30),
            layers=[dependency_layer],
            environment={
                "ODOO_URL": os.getenv("ODOO_URL", ""),
                "ODOO_DB": os.getenv("ODOO_DB", ""),
                "ODOO_USERNAME": os.getenv("ODOO_USERNAME", ""),
                "ODOO_PASSWORD": os.getenv("ODOO_PASSWORD", ""),
            },
        )

        # Connect queue → lambda
        fn.add_event_source(lambda_event_sources.SqsEventSource(queue, batch_size=1))
