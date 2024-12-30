from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserRegistrationView, UserProfileView, UserUpdateView, UserDeleteView, UserListView, UserDetailView, \
    AdCreateView, AdsListView, AdDetailView, AdUpdateView, AdDelete, UserAdsList

urlpatterns = [

    path('user/register/', UserRegistrationView.as_view(), name='user-register'),
    path('token/login/', TokenObtainPairView.as_view(), name='token-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('user/protected/', UserProfileView.as_view(), name='user-self'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('users/', UserListView.as_view(), name='users-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('ad/create/', AdCreateView.as_view(), name='ad-create'),
    path('ads/', AdsListView.as_view(), name='ads-list'),
    path('ad/<int:id>/update/', AdUpdateView.as_view(), name='ad-update'),
    path('ad/<int:pk>/delete', AdDelete.as_view(), name='ad-delete'),
    path('ad/<int:id>/', AdDetailView.as_view(), name='ad-detail'),
    path('user/<int:user_id>/ads/', UserAdsList.as_view(), name='user-adslist'),

]
