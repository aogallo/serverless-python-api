import json
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

app = APIGatewayRestResolver()

@app.get("/hello/<name>")
def hello_name(name):
    return { "statusCode": 200, "body": json.dumps({"message": f"hello {name}"})}

@app.get("/hello")
def hello():
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def lambda_handler(event, context):
    return app.resolve(event,context)
