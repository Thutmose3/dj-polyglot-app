import json

from django.contrib.messages import get_messages
from django.utils.encoding import force_str
from django.utils.functional import Promise


class LazyEncoder(json.JSONEncoder):
    """Encodes django's lazy i18n strings."""

    def default(self, obj):
        """Encodes django's lazy i18n strings."""
        if isinstance(obj, Promise):
            return force_str(obj)
        return super().default(obj)


class HtmxMessageMiddleware:
    """Middleware to add handle messages and HTMX."""

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        """Add messages to HX-Trigger header so it is picked up by HTMX in the frontend."""
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if response.status_code == 302:
            return response

        hx_trigger = response.headers.get("HX-Trigger")

        if hx_trigger is None:
            # If the HX-Trigger is not set, start with an empty object
            hx_trigger = {}
        elif hx_trigger.startswith("{"):
            # If the HX-Trigger uses the object syntax, parse the object
            hx_trigger = hx_trigger.replace("'", '"')

            hx_trigger = json.loads(hx_trigger)
        else:
            # If the HX-Trigger uses the string syntax, convert to the object syntax
            hx_trigger = {hx_trigger: True}
        messages = []
        for message in get_messages(request):
            if message.tags == "success":
                tags = "text-green-800 bg-green-50"
            elif message.tags == "info":
                tags = "text-blue-800 bg-blue-50"
            elif message.tags == "warning":
                tags = "text-yellow-800 bg-yellow-50"
            elif message.tags == "danger":
                tags = "text-red-800 bg-red-50"
            else:
                tags = "text-gray-800 bg-gray-50"

            messages.append({"message": message.message, "tags": tags})

        hx_trigger["messages"] = messages

        response.headers["HX-Trigger"] = json.dumps(hx_trigger, cls=LazyEncoder)

        return response
