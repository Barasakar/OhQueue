from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


# Login page 
def renderLoginPage(request):
    return render(request, "queue_app/login_page.html")

# Signup Page
def renderSignupPage(request):
    return render(request, "queue_app/signup_page.html")

#------------------ Functionality -----------------------#
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("Username: ", username)
        print("Password: ", password)
        try:
            user = User.objects.create_user(username=username, password=password)
            print("You have created an account. Redirecting you to login page.")
            return redirect("/login_page/")
        except Exception as e:
            return render(request, "queue_app/signup_page.html", {'error': str(e)})
    return render(request, "queue_app/signup_page.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("You are logged in!")
            #TODO: Implement redirect()
        else:
            return render(request, "queue_app/login_page.html", {'error': 'Invalid username or password'})
    return render(request, "queue_app/login_page.html")