from django.urls import path
from .views import (UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView, UserPasswordResetView,
                    UserPasswordRestDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView,
                    UserFollowView, UserUnfollowView, EditProfileView)


app_name = 'account'
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='profile'),
    path('reset/', UserPasswordResetView.as_view(), name='rest_password'),
    path('reset/done/', UserPasswordRestDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>/', UserFollowView.as_view(), name='follower'),
    path('unfollow/<int:user_id>/', UserUnfollowView.as_view(), name='unfollower'),
    path('edit_user/', EditProfileView.as_view(), name='edite_user'),
]