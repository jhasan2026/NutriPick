from django.urls import path
from .views import CustomLoginView,register,profile_update_view,set_default_image_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('register/',register,name='register'),
    path('profile/', profile_update_view, name='profile'),
    path('set_default_image/<int:patient_id>/', set_default_image_view, name='set_default_image'),

]