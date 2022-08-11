"""djangoapp3 URL Configuration

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
from django.urls import path
from django_pyfb import views

urlpatterns = [

    path(r'', views.index),
    path(r'facebook_login', views.facebook_login),
    path(r'facebook_login_success', views.facebook_login_success),
    path(r'facebook_javascript_login_sucess', views.facebook_javascript_login_sucess),
]
