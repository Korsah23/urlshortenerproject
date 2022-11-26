from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("signup",views.signup, name="signup"),
    path("login",views.Login, name="login"),
    path("dashboard",views.dashboard, name="dashboard"),
    path("logout",views.Logout, name="logout"),
    path("<str:pk>", views.visitLink, name = "visitLink"),
]