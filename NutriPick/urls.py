"""
URL configuration for NutriPick project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from user.views import home


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('posts.urls')),
    path("user/",include('user.urls')),
    path("workout_plan/",include('workout.urls')),
    path('chat/', include('a_rtchat.urls')),
    path("nutri_need_home/",include('nutri_needs.urls')),
    path('FoodRecomendation/', include('FoodRecomendation.urls')),
    path('dietitian/',include('Dietitian.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

