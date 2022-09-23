"""LEP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from users import views as user_views
from main.views import home_view, about_view
from django.conf import settings
from django.conf.urls.static import static
from groups.views import group_create_view, group_join_view, group_list_view, group_manage_view, group_settings_view, group_delete_view, group_leave_view, group_kick_view, group_perm_view
from exams.views import exam_settings_view, CalendarView, exam_setup_view, exam_delete_view, exam_mcq_questions_view, exam_tf_questions_view, exam_edit_view, exam_join_view, face_view, exam_view, exam_end_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home-page'),
    path('about/', about_view, name='about'),
    path('register/', user_views.register_view, name='register'),
    path('profile/', user_views.profile_view, name='profile'),
    path('', CalendarView.as_view(), name='calendar'),
    path('group/create/', group_create_view, name='group-create'),
    path('group/join/', group_join_view, name='group-join'),
    path('group/list/', group_list_view, name='group-list'),
    path('group/<name>/', group_manage_view, name='group-manage'),
    path('group/<name>/settings/', group_settings_view, name='group-settings'),
    path('group/<name>/delete/', group_delete_view, name='group-delete'),
    path('group/<name>/leave/', group_leave_view, name='group-leave'),
    path('group/<name>/kick/<user>/', group_kick_view, name='group-kick'),
    path('group/<name>/permission/<user>/', group_perm_view, name='group-perm'),
    path('group/<name>/exam/setup/', exam_setup_view, name='exam-setup'),
    path('group/<name>/exam/<exam>/mcq/model/<int:exam_model>/', exam_mcq_questions_view, name='exam-mcq'),
    path('group/<name>/exam/<exam>/tf/model/<int:exam_model>/', exam_tf_questions_view, name='exam-tf'),
    path('group/<name>/exam/<exam>/settings/', exam_settings_view, name='exam-settings'),
    path('group/<name>/exam/<exam>/delete/', exam_delete_view, name='exam-delete'),
    path('group/<name>/exam/<exam>/edit/', exam_edit_view, name='exam-edit'),
    path('group/<name>/exam/<exam>/join/', exam_join_view, name='exam-join'),
    path('group/<name>/exam/<exam>/join/facerecog/', face_view, name='face-detect'),
    path('group/<name>/exam/<exam>/', exam_view, name='exam'),
    path('group/<name>/exam/<exam>/grade', exam_end_view, name='exam-end'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)