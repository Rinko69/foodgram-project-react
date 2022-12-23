from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.pagination import CustomPageNumberPagination
from .models import Follow, MyUser
from .serializers import (CustomUserSerializer,
                          FollowSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = MyUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def follow_author(request, pk):
    """
    Подписка на автора.
    """
    user = get_object_or_404(MyUser, username=request.user.username)
    author = get_object_or_404(MyUser, pk=pk)

    if request.method == 'POST':
        if user.id == author.id:
            content = {'errors': 'Нельзя подписаться на себя!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            Follow.objects.create(user=user, author=author)
        except IntegrityError:
            content = {'errors': 'Вы уже подписаны на данного автора!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        follows = MyUser.objects.all().filter(username=author)
        serializer = FollowSerializer(
            follows,
            context={'request': request},
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        try:
            subscription = Follow.objects.get(user=user, author=author)
        except ObjectDoesNotExist:
            content = {'errors': 'Вы не подписаны на данного автора!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        subscription.delete()
        return HttpResponse('Вы успешно отписаны от этого автора!',
                            status=status.HTTP_204_NO_CONTENT)


class SubscriptionListView(viewsets.ReadOnlyModelViewSet):

    queryset = MyUser.objects.all()
    serializer_class = FollowSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAuthenticated,)
    search_fields = ('^author__user',)

    def get_queryset(self):
        user = self.request.user
        new_queryset = MyUser.objects.filter(author__user=user)
        return new_queryset
