from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import api_view
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

    @api_view(['POST', 'DELETE'])
    def follow_author(request, pk):
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


class FollowListView(ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return MyUser.objects.filter(following__user=self.request.user)