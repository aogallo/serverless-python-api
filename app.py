import json

def hello_name(event, **kargs):
    username = event["pathParameters"]["name"]
    return { "statusCode": 200, "body": json.dumps({"message": f"hello {username}"})}


def hello(**kargs):
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

class Router:
    def __init__(self) -> None:
        self.routes = {}

    def set(self,path,method, handler):
        self.routes[f"{path}-{method}"]=handler

    def get(self, path,method):
        try:
            route = self.routes[f"{path}-{method}"]
        except KeyError:
            raise RuntimeError(f"Cannot route request to the correct method path={path} method={method}")
        return route

router = Router()
router.set(path="/hello", method="GET", handler=hello)
router.set(path="/hello/{name}", method="GET", handler=hello_name)

def lambda_handler(event, context):
    path = event["rawPath"]
    http_method = event["requestContext"]["http"]["method"]
    method = router.get(path=path, method=http_method)
    return method(event=event)
