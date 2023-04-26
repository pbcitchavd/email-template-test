from django.urls import path
from . import views

app_name = "app_phishing"

urlpatterns = [
    path('', views.index, name="home"),
    path('employees/', views.employees, name="employees"),
    path('employees/<str:employee_id>', views.show_template_from_db, name="show_template"),
    path('register_pwd/<str:email>/<int:user_id>/', views.get_password, name="get_pwd"),
    path('send_mail/', views.send_email_to_all, name="send_mail"),
    path('send_mail_to_user/<int:employee_id>', views.send_email_to_user, name="send_mail_to_user"),
    path('activate/<uidb64>/<token>/', views.activate_user, name="activate")
]