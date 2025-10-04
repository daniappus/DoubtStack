from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('index/', views.index, name='index'),
    path('verify_number/', views.verify_number, name='verify_number'),
    path('permission/', views.permission, name='permission'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('set_password/', views.set_password, name='set_password'),
    path('student_password/<int:reg_no>/', views.student_password, name='student_password'),
    path('teacher_password/<int:reg_no>/', views.teacher_password, name='teacher_password'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]
