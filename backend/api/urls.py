from django.contrib.auth.views import LogoutView
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (FollowViewSet, RecipeViewSet,
                    TagViewSet, UserViewSet)

v1 = routers.DefaultRouter()
v1.register('users', UserViewSet, basename='users')
v1.register('tags', TagViewSet, basename='tags')
v1.register(r'tags/(?P<tag_id>\d+)/recipes',
            RecipeViewSet, basename='recipes')
v1.register(r'users/(?P<user_id>\d+)/follow/(?P<author_id>\d+)/follow_list',
            FollowViewSet, basename='follow_list')

urlpatterns = [
    path('v1/', include(v1.urls)),
    path('v1/users/', UserViewSet.as_view({'post': 'create', 'get': 'list'}), name="register"),
    path('v1/auth/token/login/', views.obtain_auth_token, name='login'),
    path('v1/auth/token/logout/', LogoutView.as_view(), name='logout'),
]
