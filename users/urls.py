from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
    path('sign-in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('<int:user_id>/', views.UserDetailView.as_view(), name='user_view'),
    path('sign-in/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
]
