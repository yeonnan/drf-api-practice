from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UserSerializer, ProfileUpdateSerializer, ChangePasswordSerializer
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


# 회원가입
class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()            
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


# 로그아웃
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({'error' : 'refresh token이 없습니다.'}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist
            return Response({'message' : '로그아웃 성공'}, status=200)
        except Exception as e:
            return Response({'error' : '로그아웃에 실패하였습니다.'}, status=400)


# 프로필 수정
class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)

        if request.user.pk != user.pk:
            return Response({'error' : '권한이 없습니다.'}, status=400)
        
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# 비밀번호 변경
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({'error' : '비밀번호가 필요합니다.'}, status=400)
        
        if not check_password(old_password, request.user.password):
            return Response({'error' : '현재 비밀번호가 올바르지 않습니다.'}, status=400)
        
        serializer = ChangePasswordSerializer(data={'password' : new_password})
        serializer.is_valid(raise_exception=True)

        request.user.set_password(new_password)
        request.user.save()
        return Response({'message' : '비밀번호가 변경되었습니다.'}, status=200)
    

# 회원 탈퇴
class DeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user = request.user
        password = request.data.get('password')
        if not password or not check_password(password, user.password):
            return Response({'error' : '올바른 비밀번호를 입력해주세요.'}, status=400)
        
        user.delete()
        return Response(status=200)