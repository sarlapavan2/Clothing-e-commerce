
from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('verify/', views.otp_page, name='verify'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('login/', views.login_page, name='login'), 
    path('logout/', views.logout_page, name='logout'),  
    path('home/', views.home_page, name='home'),
]