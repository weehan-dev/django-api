from exponent_server_sdk import PushClient, PushMessage, PushServerError, PushResponseError, DeviceNotRegisteredError

# Create your views here.
from requests.exceptions import ConnectionError, HTTPError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User


def send_push_message(target_token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(
                to=target_token,
                body=message,
                data=extra
            )
        )

    except PushServerError as e:
        print('푸시 서버에 전송되지 않음.', e)

    except (ConnectionError, HTTPError) as e:
        print('푸시 서버에 전송되지 않음.', e)

    try:
        # 푸시 서버에서 응답을 받긴 함
        response.validate_response()
        return True
    except DeviceNotRegisteredError:
        user = User.objects.filter(notification_token=target_token)[0]
        user.notification_token = None;
        user.save()
        return False

    except PushResponseError as e:
        print(e)
        return False


@api_view(['POST'])
def set_notification_token(request, id):
    try:
        user = User.objects.get(id=id)
        if request.user != user:
            raise Exception('타인의 정보를 수정할 수 없습니다.')
        print(request.data.get('token'))
        notification_token = request.data.get('token')
        print(notification_token)
        if notification_token:
            user.notification_token = notification_token
            user.save()

            return Response(status=status.HTTP_202_ACCEPTED, data={'message': '알림 설정 완료'})
        raise Exception('토큰 정보가 없습니다.')
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': '해당 유저가 존재하지 않습니다.'})
    except Exception as e:
        print(str(e))
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})
