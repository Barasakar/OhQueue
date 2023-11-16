from django.shortcuts import render
from django.http import HttpResponse


# Login page 
def renderLoginPage(request):
    return render(request, "queue_app/login_page.html")

# Signup Page
def renderSignupPage(request):
    return render(request, "queue_app/signup_page.html")