from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, "base.html")


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

#def showUsers(request):
#	user = User.objects.all()
#	return render(request, "show_users.html" , {'user' : user})