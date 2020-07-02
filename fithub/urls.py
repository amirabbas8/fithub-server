from django.urls import path

from . import views

urlpatterns = [
    path('sign_up', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('insert_history', views.insert_history, name='insert_history'),
    path('get_history', views.get_history, name='get_history'),
    path('add_course', views.add_course, name='add_course'),
    path('enroll_course', views.enroll_course, name='enroll_course'),
    path('left_course', views.left_course, name='left_course'),
    path('add_post', views.add_post, name='add_post'),
    path('delete_post', views.delete_post, name='delete_post'),
    path('edit_post', views.edit_post, name='edit_post'),
    path('get_courses', views.get_courses, name='get_courses'),
    path('get_my_courses', views.get_my_courses, name='get_my_courses'),
]
