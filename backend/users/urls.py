from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionListView, follow_author

router = DefaultRouter()
router.register(
    r'users/subscriptions',
    SubscriptionListView,
    basename='subscriptions',
)

urlpatterns = [
     path('users/<int:pk>/subscribe/',
         follow_author,
         name='follow-author'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
