from django.shortcuts import render
from django.http import HttpResponse 

def nutri_need_home (request): 
    return render(request,"nutri_needs/nutri_need_home.html")


def nutri_need_about (request): 
    return HttpResponse("hello world from about")