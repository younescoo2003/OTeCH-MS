from rest_framework.views import exception_handler


def status_in_json_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code
        response.data = {"data": response.data}
        response.data["status"] = status_code
        response.status_code = 200

    return response