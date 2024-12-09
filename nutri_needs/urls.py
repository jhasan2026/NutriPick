from django.urls import path
from . import views


urlpatterns = [
    path("",views.nutri_need_home,name="nutri_need_home"),
    path("about/",views.nutri_need_about,name="nutri_need_about"),
    path("api/",views.input_page,name="api"),
    path("response/",views.show_response,name="response"),
    path("health_form/",views.customer_input,name="health_input"),



]
