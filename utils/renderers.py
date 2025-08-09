from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict) and "status" in data:
            return super().render(data, accepted_media_type, renderer_context)

        response = renderer_context["response"]
        status_code = response.status_code

        response_data = {"status": status_code, "data": data}

        response.status_code = 200

        return super().render(response_data, accepted_media_type, renderer_context)