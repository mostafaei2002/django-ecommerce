import logging
from io import BytesIO

from django.contrib import messages
from django_htmx.http import trigger_client_event

logger = logging.getLogger("django")


def HtmxMessagesMiddleware(get_response):
    # Middleware to handle htmx messages

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # If No Redirect then trigger the messages event
        if (
            not response.headers.get("HX-Redirect")
            and not response.headers.get("Location")
            and not response.headers.get("HX-Refresh")
        ):
            response = trigger_client_event(
                response,
                "messages",
                [
                    {"message": message.message, "tags": message.tags}
                    for message in messages.get_messages(request)
                ],
            )

        return response

    return middleware
