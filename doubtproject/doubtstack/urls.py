from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('doubts/', views.view_all_doubts, name='view_all_doubts'),
    path('doubts/upvote/<int:doubt_id>/', views.upvote_doubt, name='upvote_doubt'),
    path('student/doubts/<int:doubt_id>/chat/', views.student_reply_chat, name='student_reply_chat'),

    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/doubts/', views.teacher_view_doubts, name='teacher_view_doubts'),
    path('teacher/doubts/<int:doubt_id>/chat/', views.teacher_reply_chat, name='teacher_reply_chat'),
]



from . import ajax_views
urlpatterns += [
    path('student/doubts/<int:doubt_id>/fetch-replies/', ajax_views.fetch_replies, name='fetch_replies'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)