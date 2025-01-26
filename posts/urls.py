from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/', views.s_post_detail, name='post_detail'),
]
