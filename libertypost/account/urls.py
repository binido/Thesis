from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/status/<str:status>/", views.profile, name="profile_status"),
    path("profile/user/<int:user_id>/", views.user_profile, name="user_profile"),
]
