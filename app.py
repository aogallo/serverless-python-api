import json
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths

logger = Logger()
tracer = Tracer()
app = APIGatewayHttpResolver()


@app.get("/")
@tracer.capture_method
def ping():
    return {"message": "pong"}


@app.get("/hello/<name>")
def hello_name(name):
    return {"statusCode": 200, "body": {"message": f"hello {name}"}}


@app.get("/hello")
def hello():
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!",
    }

    response = {"statusCode": 200, "body": body}

    return response


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
