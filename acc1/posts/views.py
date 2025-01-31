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

    # 특정 pk에 해당하는 Post 객체 가져오고 없으면 404 반환
    def get_object(self, pk):
        try:
            return get_object_or_404(Post, id=pk)
        except Http404:
            raise Http404('게시글을 찾을 수 없습니다.')

    # 게시글 상세 조회
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    # 게시글 수정
    def put(self, request, pk):
        post = self.get_object(pk)

        # 현재 로그인한 사용자와 게시글 작성자가 다를 경우 오류 반환
        if post.user != request.user:
            return Response({'message' : '유효하지 않은 사용자입니다.'}, status=400)
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.user != request.user:
            return Response({'message' : '유효하지 않은 사용자입니다.'}, status=400)
        post.delete()
        return Response({'message' : '삭제완료'}, status=200)