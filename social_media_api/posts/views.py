from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from .filters import PostFilter
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .models import Like, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FollowUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(get_user_model(), id=user_id)
        request.user.following.add(user_to_follow)
        return  Response({'message': 'You are now following {}'.format(user_to_follow.username)})

class UnfollowUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(get_user_model(), id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({'message': 'You have unfollowed {}'.format(user_to_unfollow.username)})

class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author__in=self.request.user.following.all().order_by('-created_at'))


class LikePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            print(request.user, post.author, 'liked your post', post)  # To be changed with the create a notification function.
            return Response({'message': 'Post liked'})
        return Response({'message': 'Already liked'}, status=400)

class UnlikePostView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'message': 'Post unliked'})