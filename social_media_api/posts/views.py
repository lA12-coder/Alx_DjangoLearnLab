from django.contrib.auth import get_user_model
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from .filters import PostFilter
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import permissions
from rest_framework.response import Response
from .models import Like, Post
from ..notifications.models import Notification
from ..notifications.serializers import NotificationSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FollowUserView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = generics.get_object_or_404(get_user_model(), id=user_id)
        request.user.following.add(user_to_follow)
        return  Response({'message': 'You are now following {}'.format(user_to_follow.username)})

class UnfollowUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        user_to_unfollow = generics.get_object_or_404(get_user_model(), id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({'message': 'You have unfollowed {}'.format(user_to_unfollow.username)})

class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, following_users=None):
        return Post.objects.filter(author__in=following_users).order_by('-created_at').following.all()


class LikePostView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = generics.get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            print(request.user, post.author, 'liked your post', post)  # To be changed with the create a notification function.
            return Response({'message': 'Post liked'})
        return Response({'message': 'Already liked'}, status=400)

class UnlikePostView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'message': 'Post unliked'})


class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        notification = Notification.objects.create()
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')