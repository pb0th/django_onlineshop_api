from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AuthLogoutView, RequestResetPasswordView, ChangePasswordView, UpdateProfileInfo

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path("logout/", AuthLogoutView.as_view(), name="logout"),
    path('refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('request_reset_password/', RequestResetPasswordView.as_view(), name="request_reset_password"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path("update_profile/", UpdateProfileInfo.as_view(), name="update_profile")
]



