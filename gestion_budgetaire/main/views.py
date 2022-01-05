from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import  render, redirect
from .forms import (NewUserForm, CadreForm, ChefDepForm, SousDirForm, ContentAdminForm,
					AddUniteForm,AddDepForm,AddPos1Form,AddPos2Form,AddPos3Form,AddPos6Form,AddPos7Form
					)
from .models import (User, Cadre, Chef_Dep, Sous_Dir, Content_Admin,
                    Departement, Unite, Pays, Monnaie, Taux_de_change, Chapitre,
                    SCF_Pos_1, SCF_Pos_2, SCF_Pos_3, SCF_Pos_6, SCF_Pos_7,
                    Unite_has_Compte, Compte_has_Montant, Cadre_has_Unite
                    )
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
def add_unite(request):
	unite_form = AddUniteForm(request.POST or None)
	if request.method == "POST":
		if  unite_form.is_valid():
			unite = unite_form.save()
			messages.success(request, "Unite added successfuly." )
			return redirect("/unite_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="structure/add_unite.html", context={"unite_form":unite_form})

# afficher tout les unités / en algérie / a l'etranger 
def unite_list(request):
	unite = Unite.objects.all()
	unite_count = Unite.objects.all().count()
	#unite_algerie = 
	#unite_etranger = 
	return render(request, "structure/unite_list.html" , {'unite' : unite, 'unite_count':unite_count})

# modifier unité
# supprimer unité 

# -----------------------------------------------------------------------------------

# ------------ gestion des Departement ---------------------------------------------------

# ajouter Departement
def add_dep(request):
	dep_form = AddDepForm(request.POST or None)
	if request.method == "POST":
		if  dep_form.is_valid():
			dep = dep_form.save()
			messages.success(request, "Departement added successfuly." )
			return redirect("/dep_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="structure/add_dep.html", context={"dep_form":dep_form})
# afficher tout les Departement
def dep_list(request):
	dep = Departement.objects.all()
	dep_count = Departement.objects.all().count()
	return render(request, "structure/dep_list.html" , {'dep' : unite, 'dep_count':unite_count})

# modifier departement
# supprimer Departement 

# -----------------------------------------------------------------------------------

# ------------ gestion des Comptes SCF ---------------------------------------------------

# ajouter Compte pos 1
def add_pos1(request):
	pos1_form = AddPos1Form(request.POST or None)
	if request.method == "POST":
		if  pos1_form.is_valid():
			pos1 = pos1_form.save()
			messages.success(request, "compte SCF 1 position added successfuly." )
			return redirect("/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos1.html", context={"pos1_form":pos1_form})
# ajouter Compte pos 2
def add_pos2(request):
	pos2_form = AddPos2Form(request.POST or None)
	if request.method == "POST":
		if  pos2_form.is_valid():
			pos2 = pos2_form.save()
			messages.success(request, "compte SCF 2 position added successfuly." )
			return redirect("/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos2.html", context={"pos2_form":pos2_form})
# ajouter Compte pos 3
def add_pos3(request):
	pos3_form = AddPos3Form(request.POST or None)
	if request.method == "POST":
		if  pos3_form.is_valid():
			pos3 = pos3_form.save()
			messages.success(request, "compte SCF 3 position added successfuly." )
			return redirect("/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos3.html", context={"pos3_form":pos3_form})
# ajouter Compte pos 6
def add_pos6(request):
	pos6_form = AddPos6Form(request.POST or None)
	if request.method == "POST":
		if  pos6_form.is_valid():
			pos6 = pos6_form.save()
			messages.success(request, "compte SCF 6 position added successfuly." )
			return redirect("/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos6.html", context={"pos6_form":pos6_form})
# ajouter Compte pos 7
def add_pos7(request):
	pos7_form = AddPos7Form(request.POST or None)
	if request.method == "POST":
		if  pos7_form.is_valid():
			pos7 = pos7_form.save()
			messages.success(request, "compte SCF 7 position added successfuly." )
			return redirect("/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos7.html", context={"pos7_form":pos7_form})

# afficher Comptes 
def comptes_list(request):
	pos1 = SCF_Pos_1.objects.all()
	pos2 = SCF_Pos_2.objects.all()
	pos3 = SCF_Pos_3.objects.all()
	pos6 = SCF_Pos_6.objects.all()
	pos7 = SCF_Pos_7.objects.all()
	#pos1 = SCF_Pos_1.objects.all().count()
	return render(request, "scfs/comptes_list.html" , {'pos1' : pos1, 'pos2' : pos2,
													 'pos3' : pos3, 'pos6' : pos6, 'pos7' : pos7})

# modifier Comptes pos 1 
# modifier Comptes pos 2 
# modifier Comptes pos 3 
# modifier Comptes pos 6 
# modifier Comptes pos 7

# supprimer compte

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
