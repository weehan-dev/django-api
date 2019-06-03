# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from django.core.mail.message import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User, Profile
from userInfo.models import Token
from userInfo.serializers import ProfileSerializer
import random
from yeonhadae.config import KAKAO_APP_KEY

def map_view(request):
    APP_KEY = KAKAO_APP_KEY

    if request.method == 'GET':
        print('이건 GET이다');
        return render(request, "DaumPost.html", {"APP_KEY": APP_KEY})

    else:
        print('이건 POST다')
        return render(request, "DaumPost.html", {"APP_KEY": APP_KEY})

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def validate_token(request, id):
    try:
        user = User.objects.get(id=id)
        if (request.user == user) and (request.user.username == request.data['username']):
            Response(status=status.HTTP_200_OK, data={"success": True, "message": "유효한 토큰입니다."})
        else:
            raise PermissionError

    except PermissionError:
        Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "message": "비정상적 접근입니다."})




class SendMailToken(APIView):

    @staticmethod
    def make_token(length):
        available = 'qwertyuiopasdfghjklzxcvbnm123456789QWERTYUIOPASDFGHJKLZXCVBNM'
        return "".join([random.choice(available) for _ in range(length)])

    def post(self, request, id, format=None):

        user = request.user
        print(user.email, user.username)
        token = self.make_token(7)
        try:
            token_obj = Token.objects.get(email=user.email, username=user.username)
            token_obj.token = token
            token_obj.save()
        except Token.DoesNotExist:
            Token.objects.create(email=user.email, username=user.username, token=token)

        # 메일 발송
        # TODO 메일 템플릿 바꿔줘야함
        html_content = render_to_string('mail_template.html', {'token': token})
        email = EmailMultiAlternatives('[연하대] 인증 메일', to=[user.email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response(status=status.HTTP_201_CREATED, data={"success": True, "data": "메일이 발송되었습니다."})


class VerifyMailToken(APIView):

    def post(self, request, id):
        if request.user.is_certificated:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"data": "이미 인증된 계정입니다."})
        token_string = request.data.__getitem__('token')
        user = get_object_or_404(User, id=id)
        token = get_object_or_404(Token, email=user.email, username=user.username, token=token_string)

        user.is_certificated = True
        user.save()

        token.delete()
        return Response(status=status.HTTP_200_OK, data={"data": "인증 완료되었습니다."})


class HandleProfile(APIView):
    def get(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        profile = get_object_or_404(Profile, user=user)

        serializer = ProfileSerializer(profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        if user != request.user:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="타인의 프로필을 수정할 수 없습니다.")

        profile = get_object_or_404(Profile, user=user)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)

    def post(self, request, id, format=None):
        """
        :body: name, gender, univ, latitude, longitude, avatar, height, weight, religion, is_smoker:
        :return: json(success, message, data):
        """
        user = get_object_or_404(User, id=id)
        if user != request.user:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="타인의 프로필을 생성할 수 없습니다.")

        try:
            Profile.objects.get(user=user)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="이미 프로필이 존재합니다.")
        except Profile.DoesNotExist:
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                profile = serializer.save()
                if profile:
                    profile.user = request.user
                    profile.save()
                    print(request.user.profile)

                    data = ProfileSerializer(profile)
                    return Response(status=status.HTTP_201_CREATED, data=data.data)
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED, data=serializer.errors)

            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)
