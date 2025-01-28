from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from accounts.models import User

# 회원가입, 로그인, 로그아웃, 비밀번호 수정, 회원탈퇴


# 회원가입
class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


# 로그아웃


# 비밀번호 수정


# 회원 탈퇴