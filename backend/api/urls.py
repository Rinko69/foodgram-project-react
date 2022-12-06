from django.contrib.auth.views import LogoutView
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (FollowViewSet, RecipeViewSet,
                    TagViewSet, UserViewSet, code, signup,)

v1 = routers.DefaultRouter()
v1.register('users', UserViewSet, basename='users')
v1.register('tags', TagViewSet, basename='tags')
v1.register('recipes', RecipeViewSet, basename='recipes')
v1.register(r'follow/(?P<user_id>\d+)/folow_list',
            FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/login/', views.obtain_auth_token, name='login'),
    path('v1/auth/token/logout/', LogoutView.as_view(), name='logout'),
    path('v1/auth/code/', code, name='code'),
]