from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.login_to_dashboard, name="login"),
]