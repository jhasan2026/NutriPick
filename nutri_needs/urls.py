from django.urls import path
from . import views


urlpatterns = [
    path("",views.nutri_need_home,name="nutri_need_home"),
    path("about/",views.nutri_need_about,name="nutri_need_about"),
    path("health_form/analyze/", views.analyze_data, name='analyze_data'),
    path("health_form/",views.customer_input,name="health_input"),



]
