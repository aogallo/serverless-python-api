from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths

logger = Logger(service="APP")
tracer = Tracer(service="APP")
app = APIGatewayHttpResolver()
metrics = Metrics(namespace="MyApi", service="APP")


@app.get("/")
@tracer.capture_method
def ping():
    return {"message": "pong"}


@app.get("/hello/<name>")
def hello_name(name):
    metrics.add_metric(name="SuccessfullGreetings", unit=MetricUnit.Count, value=1)
    return {"statusCode": 200, "body": {"message": f"hello {name}"}}


@app.get("/hello")
def hello():
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!",
    }
    metrics.add_metric(name="SuccessfullGreetings", unit=MetricUnit.Count, value=1)
    response = {"statusCode": 200, "body": body}

    return response


@tracer.capture_lambda_handler
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_HTTP, log_event=True
)
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise
