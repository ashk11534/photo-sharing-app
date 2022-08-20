from django.urls import path
from . import views

urlpatterns = [
    path('photo-share/<str:url_route>/', views.home, name='home'),
    path('user-account/', views.user_account, name='user_account'),
    path('register-user/', views.register_user, name='register_user'),
    path('login-user/', views.login_user, name='login_user'),
    path('user-profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('logout-user/', views.logout_user, name='logout_user'),
    path('delete_post/', views.delete_post, name='delete_post'),
    path('like-post/<str:post_id>/<str:user_id>/', views.like_post, name='like_post'),
    path('comment-post/<str:post_id>/<str:user_id>/', views.comment_post, name='comment_post'),
    path('following/<str:user_id>/<str:following_user_id>/', views.following, name='following'),
    path('message/', views.message, name='message'),
    path('chat_box/<str:receiver_id>/', views.chat_box, name='chat_box'),
    path('delete_message/<str:message_id>/', views.delete_message, name='delete_message'),
    path('mark_message_read/<str:receiver_id>/', views.mark_message_read, name='mark_message_read'),
]
