from rest_framework.views import exception_handler
from rest_framework.response import Response

def status_in_json_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        orginal_status = response.status_code

        if not isinstance(response.data, dict):
            response.data = {'data': response.data}
        
        response.data['status'] = orginal_status
        response.status_code = 200

    return response