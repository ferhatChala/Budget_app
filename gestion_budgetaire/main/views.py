from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import  render, redirect
from .forms import NewUserForm, CadreForm, ChefDepForm, SousDirForm, ContentAdminForm
from .models import Cadre, Chef_Dep, Sous_Dir, Content_Admin
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, "base.html")

# ------------ users management -----------------------------------------------

# ajouter cadre
@login_required(login_url='login')
def ajouter_cadre(request):
	user_form = NewUserForm(request.POST or None)
	cadre_form = CadreForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid() and cadre_form.is_valid():
			user = user_form.save()
			cadre = cadre_form.save(commit=False)
			cadre.user = user
			cadre.save()
			messages.success(request, "Cadre added successfuly." )
			return redirect("/cadres_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	#form = NewUserForm()
	return render (request=request, template_name="registration/add_cadre.html", context={"user_form":user_form , "cadre_form":cadre_form})

# ajouter chef departement
@login_required(login_url='login')
def ajouter_chef_dep(request):
	user_form = NewUserForm(request.POST or None)
	chef_dep_form = ChefDepForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid() and chef_dep_form.is_valid():
			user = user_form.save()
			chef_dep = chef_dep_form.save(commit=False)
			chef_dep.user = user
			chef_dep.save()
			messages.success(request, "chef departement added successfuly." )
			return redirect("/chef_dep_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	#form = NewUserForm()
	return render (request=request, template_name="registration/add_chef_dep.html", context={"user_form":user_form , "chef_dep_form":chef_dep_form})

# ajouter sous directeur
@login_required(login_url='login')
def ajouter_sous_dir(request):
	user_form = NewUserForm(request.POST or None)
	sous_dir_form = SousDirForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid() and sous_dir_form.is_valid():
			user = user_form.save()
			sous_dir = sous_dir_form.save(commit=False)
			sous_dir.user = user
			sous_dir.save()
			messages.success(request, "sous directeur added successfuly." )
			return redirect("/sous_dir_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	#form = NewUserForm()
	return render (request=request, template_name="registration/add_sous_dir.html", context={"user_form":user_form , "sous_dir_form":sous_dir_form})

# ajouter content admin
@login_required(login_url='login')
def ajouter_content_admin(request):
	user_form = NewUserForm(request.POST or None)
	content_admin_form = ContentAdminForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid() and content_admin_form.is_valid():
			user = user_form.save()
			content_admin = content_admin_form.save(commit=False)
			content_admin.user = user
			content_admin.save()
			messages.success(request, "Content admin added successfuly." )
			return redirect("/content_admin_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	#form = NewUserForm()
	return render (request=request, template_name="registration/add_content_admin.html", context={"user_form":user_form , "content_admin_form":content_admin_form})

# afficher toutes les cadres
@login_required(login_url='login')
def cadres_list(request):
	cadre = Cadre.objects.all()
	cadres_count = Cadre.objects.all().count()
	return render(request, "registration/cadres_list.html" , {'cadre' : cadre, 'cadres_count':cadres_count})

# afficher chefs departement
def chef_dep_list(request):
	chefs = Chef_Dep.objects.all()
	chefs_count = Chef_Dep.objects.all().count()
	return render(request, "registration/chef_dep_list.html" , {'chefs' : chefs, 'chefs_count':chefs_count})

# afficher sous directeurs 
def sous_dir_list(request):
	sous_dir = Sous_Dir.objects.all()
	sous_dir_count = Sous_Dir.objects.all().count()
	return render(request, "registration/sous_dir_list.html" , {'sous_dir' : sous_dir, 'sous_dir_count':sous_dir_count})

# afficher content admin
def content_admin_list(request):
	content_admin = Content_Admin.objects.all()
	content_admin_count = Content_Admin.objects.all().count()
	return render(request, "registration/content_admin_list.html" , {'content_admin' : content_admin, 'content_admin_count':content_admin_count})



# supprimer user (concerne tout les users)
@login_required(login_url='login')
def delete_user(request, id):
    form = User.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/")

# ----------------------------------------------------------------------------------

# ------------ gestion des unités ---------------------------------------------------

# ajouter unite
# afficher tout les unités
# afficher les unités en algérie
# affichier les unités a l'etranger
# modifier unité
# supprimer unité 

# -----------------------------------------------------------------------------------

# ------------ gestion des Comptes SCF ---------------------------------------------------

# ajouter Compte pos 1
# ajouter Compte pos 2
# ajouter Compte pos 3
# ajouter Compte pos 6
# ajouter Compte pos 7

# afficher Comptes pos 1 
# afficher Comptes pos 2 
# afficher Comptes pos 3 
# afficher Comptes pos 6 
# afficher Comptes pos 7

# modifier Comptes pos 1 
# modifier Comptes pos 2 
# modifier Comptes pos 3 
# modifier Comptes pos 6 
# modifier Comptes pos 7

# supprimer compte

# -----------------------------------------------------------------------------------

# ------------ gestion des Departement ---------------------------------------------------

# ajouter Departement
# afficher tout les Departement
# modifier departement
# supprimer Departement 

# -----------------------------------------------------------------------------------

# ------------ gestion des monnaie ---------------------------------------------------

# ajouter monnaie
# afficher tout les monnaie
# modifier monnaie
# supprimer monnaie 

# -----------------------------------------------------------------------------------

# ------------ gestion des Taux de change ---------------------------------------------------

# ajouter Taux de change
# afficher tout les Taux de change
# modifier Taux de change
# supprimer Taux de change 

# -----------------------------------------------------------------------------------

# ------------ gestion des chapitre ---------------------------------------------------

# ajouter chapitre
# afficher tout les chapitres
# modifier chapitre
# supprimer chapitre

# -----------------------------------------------------------------------------------

# ------------ gestion des pays ---------------------------------------------------

# ajouter pays 
# afficher tout les pays 
# modifier pays 
# supprimer pays 

# -----------------------------------------------------------------------------------

# ------------ Affectation des cadres aux unités ---------------------------------------------------

# ajouter unité aux cadre
# affichier les cadres
# afficher l'unités d'un cadre   
# supprimer l'unité pour une cadre 

# -----------------------------------------------------------------------------------

# ------------ Affectation des comptes aux unités ---------------------------------------------------

# ajouter compte aux unité
# afficher l'unités
# afficher les comptes d'un unité   
# supprimer compte pour une unité 

# -----------------------------------------------------------------------------------
