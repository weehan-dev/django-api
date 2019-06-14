from exponent_server_sdk import PushClient, PushMessage, PushServerError, PushResponseError

# Create your views here.
from rest_framework.decorators import api_view


@api_view(['POST'])
def send_push_message(request):
    pass
