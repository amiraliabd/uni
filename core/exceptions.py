from rest_framework import status, response


class HttpNotAllowed(Exception):
    def __init__(self, msg):
        self.http_response = response.Response(status=status.HTTP_425_TOO_EARLY, data=msg)
