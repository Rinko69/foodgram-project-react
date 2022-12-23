from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPageNumberPagination
from .models import Follow, MyUser
from .serializers import (CustomUserSerializer,
                          FollowSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = MyUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FollowViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('id', None)
        author = get_object_or_404(MyUser, pk=pk)
        user = request.user

        if author == user:
            return Response(
                {'errors': 'Вы не можете подписываться на себя!'},
                status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(author=author, user=user).exists():
            return Response(
                {'errors': 'Вы уже подписаны на этого пользователя!'},
                status=status.HTTP_400_BAD_REQUEST)

        obj = Follow(author=author, user=user)
        obj.save()

        serializer = FollowSerializer(
            author, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(MyUser, id=id)
        try:
            subscription = get_object_or_404(Follow, user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(
                'Ошибка отписки!',
                status=status.HTTP_400_BAD_REQUEST,
            )


class FollowListView(ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return MyUser.objects.filter(following__user=self.request.user)