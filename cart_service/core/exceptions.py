from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from django.http import JsonResponse

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        message = next(iter(response.data.values()))
        if isinstance(message, list) and len(message) > 0:
            message = message[0]
        response.data = {
            'status': response.status_code,
            'message': message
        }
    else:
        return JsonResponse(
            {
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An unexpected error occurred.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response

def get_error_message(errors):
    error_message = None
    for field, messages in errors.items():
        if isinstance(messages, list):
            error_message = messages[0]
            break
    return error_message


class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'
    default_code = 'error'

    def __init__(self, detail, code=None):
        self.detail = {'message': detail}
