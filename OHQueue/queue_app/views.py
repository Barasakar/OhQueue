from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def renderLoginPage(request):
    return render(request, "queue_app/login_page.html")