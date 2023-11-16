"""
URL configuration for OHQueue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from queue_app import views as queue_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("queue_app/", include("queue_app.urls")),
    path("", queue_views.renderLoginPage, name="login_page"), # this assigns the login page to the root link.
    path("signup_page/", queue_views.renderSignupPage, name="signup_page"), # this assign the signup page
]
