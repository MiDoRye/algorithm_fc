from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('mork/', views.MorkView.as_view(), name='mork_view'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/logout/', views.LogoutView.as_view(), name='logout_view'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
    path('<int:user_id>/', views.ProfileView.as_view(), name='profile_view'),
    path('<int:user_id>/edit/', views.ProfileView.as_view(), name='edit_profile_view'),
]