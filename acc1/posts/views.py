from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.http import Http404


class PostListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 게시판 조회
    def get(self, request):
        posts = Post.objects.all()
        if not posts.exists():
            return Response({'message' : '게시글이 없습니다.'}, status=400)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    # 게시글 생성 
    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request' : request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 게시글 상세 조회
    def get(self, request, pk):
        pass