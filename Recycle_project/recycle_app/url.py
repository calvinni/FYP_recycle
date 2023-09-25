from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #For register
    path('register/', views.register, name='register'),
    path('register/addregister/', views.add_register, name='add_register'),
    #For login
    path('login/', views.Login, name='login'),
    path('login/checklogin/', views.check_login, name='check_login'),
    #For logout
    path('logout/', views.Logout, name='logout'),
     #For search
    path('search/', views.search, name='search'),
    #For Appointment
    path('appointment/', views.appointment, name='appointment'),
    path('appointment/<str:Date>', views.appointment_Timeslots, name='appointment_Timeslots'),
    path('appointment/addbooking/', views.add_appointment, name='add_appointment'),
    #For profile view, edit, update and delete
    path('profile/<str:phone_number>/', views.profile, name='profile'),
    path('edit/<str:id>/', views.update_profile, name='edit_profile'),
    path('delete/<str:id>/', views.del_profile, name='del_profile'),
    #For voucher
    path('voucher/', views.voucher, name='voucher'),
    path('voucher/addvoucher/', views.add_voucher, name='add_voucher'),
    #For forget password procedure
    path('forget/', views.FP_em_ph, name='forget'),
    path('forget/onetime/', views.FP_OTP, name='onetime'),
    path('forget/onetime/update/', views.FP_update, name='update'),
    path('forget/onetime/update/updating/', views.FP_updating, name='updating'),
    #For FAQ
    path('FAQ/', views.FAQ, name='FAQ'),
]