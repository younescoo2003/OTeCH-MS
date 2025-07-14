from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from rest_framework import status

class StatusInJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']
        
        # Handle 204 No Content responses
        if response.status_code == status.HTTP_204_NO_CONTENT:
            data = {'status': status.HTTP_204_NO_CONTENT}
            response.status_code = status.HTTP_200_OK
            return super().render(data, accepted_media_type, renderer_context)
            
        if data is None:
            data = {'status': response.status_code}
        elif isinstance(data, (ReturnList, list)):
            data = {
                'status': response.status_code,
                'results': list(data)
            }
        elif isinstance(data, (ReturnDict, dict)):
            if 'status' not in data:
                data['status'] = response.status_code
        else:
            data = {
                'status': response.status_code,
                'detail': str(data)
            }

        response.status_code = status.HTTP_200_OK
        return super().render(data, accepted_media_type, renderer_context)