from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("companies/", views.companies, name="companies"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("ai/", views.ai_chat, name="ai_chat"),

    path(
        "my-applications/",
        views.my_applications,
        name="my_applications"
    ),
]