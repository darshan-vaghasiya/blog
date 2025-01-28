from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import PostFilter
from .models import Post, Like
from .serializers import PostSerializer, CommentSerializer, PostStatsSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(is_active=True, is_delete=False)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ('title', 'content')
    filterset_class = PostFilter
    ordering_fields = ['like_counts', 'comment_counts', 'view_counts', 'created_at']

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.exclude(author=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Increase blog post view counts.
        if instance.author != request.user:
            instance.view_counts += 1
            instance.save(update_fields=['view_counts'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='like', url_name='like')
    def like(self, request, pk=None):
        try:
            post = self.get_object()
            like, created = Like.objects.get_or_create(post=post, user=request.user)
            if not created:
                like.delete()
                return Response({"message": "Post successfully unliked."}, status=status.HTTP_200_OK)
            return Response({"message": "Post successfully liked"}, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], serializer_class=CommentSerializer, url_path='comment', url_name='comment')
    def comment(self, request, pk=None):
        try:
            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], serializer_class=PostStatsSerializer, url_path='stats', url_name='stats')
    def stats(self, request, pk=None):
        try:
            post = self.get_object()
            serializer = self.get_serializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='my-posts', url_name='my_posts')
    def my_posts(self, request):
        """
        List posts created by the authenticated user.
        """
        user_posts = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(user_posts)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(user_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
