from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import  render, redirect
from .forms import (NewUserForm, CadreForm, ChefDepForm, SousDirForm, ContentAdminForm,
					AddUniteForm,AddDepForm,AddPos1Form,AddPos2Form,AddPos3Form,AddPos6Form,AddPos7Form,CompteScfForm,
					AddMonnaieForm, AddTauxChngForm, AddChapitreForm, AddPaysForm, 
					AffectCadreForm
					)
from .models import (User, Cadre, Chef_Dep, Sous_Dir, Content_Admin,
                    Departement, Unite, Pays, Monnaie, Taux_de_change, Chapitre,
                    SCF_Pos_1, SCF_Pos_2, SCF_Pos_3, SCF_Pos_6, SCF_Pos_7,Compte_SCF,
                    Unite_has_Compte, Compte_has_Montant, Cadre_has_Unite
                    )
from django.contrib.auth import login
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, "base.html" , {'users_count':User.objects.all().count(), 'unite_count':Unite.objects.all().count(), 'comptes':SCF_Pos_6.objects.all().count() })


# ------------ users management -----------------------------------------------

# ajouter cadre
@login_required(login_url='login')
def ajouter_cadre(request):
	user_form = NewUserForm(request.POST or None)
	cadre_form = CadreForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid() and cadre_form.is_valid():
			user = user_form.save(commit=False)
			user.user_type = 5
			user.save()
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
			user = user_form.save(commit=False)
			user.user_type = 4
			user.save()
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
			user = user_form.save(commit=False)
			user.user_type = 3
			user.save()
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
			user = user_form.save(commit=False)
			user.user_type = 2
			user.save()
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



# unités & Departements ---------------------------------------------------

def add_unite(request):
	unite_form = AddUniteForm(request.POST or None)
	if request.method == "POST":
		if  unite_form.is_valid():
			unite = unite_form.save()
			messages.success(request, "Unite added successfuly." )
			return redirect("/unite_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="structure/add_unite.html", context={"unite_form":unite_form})

def unite_list(request):
	unite = Unite.objects.all()
	unite_count = Unite.objects.all().count()
	#unite_algerie = 
	#unite_etranger = 
	return render(request, "structure/unite_list.html" , {'unite' : unite, 'unite_count':unite_count})

class UniteUpdateView(UpdateView):
	model = Unite
	fields = '__all__'
	template_name = "structure/update_unite.html"
	success_url = "/unite_list"

def delete_unite(request, id):
    form = Unite.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/unite_list")

# Departement

def add_dep(request):
	dep_form = AddDepForm(request.POST or None)
	if request.method == "POST":
		if  dep_form.is_valid():
			dep = dep_form.save()
			messages.success(request, "Departement added successfuly." )
			return redirect("/dep_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="structure/add_dep.html", context={"dep_form":dep_form})

def dep_list(request):
	dep = Departement.objects.all()
	dep_count = Departement.objects.all().count()
	return render(request, "structure/dep_list.html" , {'dep' : dep, 'dep_count':dep_count})

class DepartementUpdateView(UpdateView):
	model = Departement
	fields = '__all__'
	template_name = "structure/update_dep.html"
	success_url = "/dep_list"

def delete_dep(request, id):
    form = Departement.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/dep_list")


# Comptes SCF ---------------------------------------------------

# ajouter Comptes
def add_pos1(request):
	pos1_form = AddPos1Form(request.POST or None)
	if request.method == "POST":
		if  pos1_form.is_valid():
			pos1 = pos1_form.save()
			messages.success(request, "compte SCF 1 position added successfuly." )
			return redirect("/scf/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos1.html", context={"pos1_form":pos1_form})

def add_comptes(request):
	return render(request=request, template_name="scfs/add_comptes.html")

def add_pos2(request):
	pos2_form = AddPos2Form(request.POST or None)
	if request.method == "POST":
		if  pos2_form.is_valid():
			pos2 = pos2_form.save()
			messages.success(request, "compte SCF 2 position added successfuly." )
			return redirect("/scf/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos2.html", context={"pos2_form":pos2_form})

def add_pos3(request):
	pos3_form = AddPos3Form(request.POST or None)
	if request.method == "POST":
		if  pos3_form.is_valid():
			pos3 = pos3_form.save()
			messages.success(request, "compte SCF 3 position added successfuly." )
			return redirect("/scf/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos3.html", context={"pos3_form":pos3_form})

def add_pos6(request):
	pos6_form = AddPos6Form(request.POST or None)
	if request.method == "POST":
		if  pos6_form.is_valid():
			pos6 = pos6_form.save()
			messages.success(request, "compte SCF 6 position added successfuly." )
			return redirect("/scf/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos6.html", context={"pos6_form":pos6_form})

def add_pos7(request):
	pos7_form = AddPos7Form(request.POST or None)
	if request.method == "POST":
		if  pos7_form.is_valid():
			pos7 = pos7_form.save()
			messages.success(request, "compte SCF 7 position added successfuly." )
			return redirect("/scf/comptes_list")
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


# supprimer comptes
def delete_pos1(request, id):
    form = SCF_Pos_1.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/scf/comptes_list")

def delete_pos2(request, id):
    form = SCF_Pos_2.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/scf/comptes_list")

def delete_pos3(request, id):
    form = SCF_Pos_3.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/scf/comptes_list")

def delete_pos6(request, id):
    form = SCF_Pos_6.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/scf/comptes_list")

def delete_pos7(request, id):
    form = SCF_Pos_7.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/scf/comptes_list")

# comptes scf version 2

def add_compte(request):
	compte_form = CompteScfForm(request.POST or None)
	if request.method == "POST":
		if compte_form.is_valid():
			compte = compte_form.save(commit=False)
			compte.pos = len(str(compte.numero))
			compte.save()
			messages.success(request, "compte SCF added successfuly." )
			return redirect("/scf_comptes")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render(request=request, template_name="scfs/add_compte.html", context={"compte_form":compte_form})

def scf_comptes(request):
	comptes = Compte_SCF.objects.all()
	return render(request=request, template_name="scfs/scf_comptes.html", context={'comptes':comptes})

# Monnaie ---------------------------------------------------

def add_monnaie(request):
	monnaie_form = AddMonnaieForm(request.POST or None)
	if request.method == "POST":
		if  monnaie_form.is_valid():
			monnaie = monnaie_form.save()
			messages.success(request, "Monnaie added successfuly." )
			return redirect("/ref/monnaie_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="others/add_monnaie.html", context={"monnaie_form":monnaie_form})

def monnaie_list(request):
	monnaie = Monnaie.objects.all()
	monnaie_count = Monnaie.objects.all().count()
	return render(request, "others/monnaie_list.html" , {'monnaie' : monnaie, 'monnaie_count':monnaie_count})

class MonnaieUpdateView(UpdateView):
	model = Monnaie
	fields = '__all__'
	template_name = "others/update_monnaie.html"
	success_url = "/ref/monnaie_list"

def delete_monnaie(request, id):
    form = Monnaie.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/ref/monnaie_list")


# Taux de change ---------------------------------------------

def add_taux_chng(request):
	taux_chng_form = AddTauxChngForm(request.POST or None)
	if request.method == "POST":
		if  taux_chng_form.is_valid():
			taux_chng = taux_chng_form.save()
			messages.success(request, "Taux de change added successfuly." )
			return redirect("/ref/taux_chng_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="others/add_taux_chng.html", context={"taux_chng_form":taux_chng_form})

def taux_chng_list(request):
	taux_chng = Taux_de_change.objects.all()
	taux_chng_count = Taux_de_change.objects.all().count()
	return render(request, "others/taux_chng_list.html" , {'taux_chng' : taux_chng, 'taux_chng_count':taux_chng_count})

class TauxUpdateView(UpdateView):
	model = Taux_de_change
	fields = '__all__'
	template_name = "others/update_taux_chng.html"
	success_url = "/ref/taux_chng_list"

def delete_taux_chng(request, id):
    form = Taux_de_change.objects.get(annee=id)
    form.delete()
    return HttpResponseRedirect("/ref/taux_chng_list")



# Chapitre ---------------------------------------------------

def add_chapitre(request):
	chapitre_form = AddChapitreForm(request.POST or None)
	if request.method == "POST":
		if  chapitre_form.is_valid():
			chapitre = chapitre_form.save()
			messages.success(request, "Chapitre added successfuly." )
			return redirect("/ref/chapitre_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="others/add_chapitre.html", context={"chapitre_form":chapitre_form})

def chapitre_list(request):
	chapitre = Chapitre.objects.all()
	chapitre_count = Chapitre.objects.all().count()
	return render(request, "others/chapitre_list.html" , {'chapitre' : chapitre, 'chapitre_count':chapitre_count})

class ChapitreUpdateView(UpdateView):
	model = Chapitre
	fields = ("lib",)
	template_name = "others/update_chapitre.html"
	success_url = "/ref/chapitre_list"

def delete_chapitre(request, code_num):
    form = Chapitre.objects.get(code_num=code_num)
    form.delete()
    return HttpResponseRedirect("/ref/chapitre_list")


# Pays ---------------------------------------------------

def add_pays(request):
	pays_form = AddPaysForm(request.POST or None)
	if request.method == "POST":
		if  pays_form.is_valid():
			pays = pays_form.save()
			messages.success(request, "Pays added successfuly." )
			return redirect("/ref/pays_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="others/add_pays.html", context={"pays_form":pays_form})

def pays_list(request):
	pays = Pays.objects.all()
	pays_count = Pays.objects.all().count()
	return render(request, "others/pays_list.html" , {'pays' : pays, 'pays_count':pays_count})

class PaysUpdateView(UpdateView):
	model = Pays
	fields = '__all__'
	template_name = "others/update_pays.html"
	success_url = "/ref/pays_list"

def delete_pays(request, id):
    form = Pays.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/ref/pays_list")



# ------------ Affectation des cadres aux unités ---------------------------------------------------

# show unites d'un cadre donnée
def show_unites(request, id):
	c = Cadre.objects.get(id=id)
	unites = Cadre_has_Unite.objects.filter(cadre = c)
	return render(request,"affectation/show_unites.html", {'unites':unites, 'c':c})

#delete unite 
def delete_unite_of_cadre(request, id):
	form = Cadre_has_Unite.objects.get(id=id)
	form.delete()
	return HttpResponseRedirect("/aff/show_cadres")

# add_unite aux cadre donnée
def add_unite_to_cadre(request, cadre_id):
	cadre = Cadre.objects.get(id=cadre_id)
	form = AffectCadreForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			unite_to_cadre = form.save(commit=False)
			unite_to_cadre.cadre = cadre
			unite_to_cadre.save()
			messages.success(request, "unite added successfuly." )
			return redirect("/aff/show_unites/"+ str(cadre_id)+"")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render (request=request, template_name="affectation/add_unite_to_cadre.html", context={"form":form})

#show caders list
def show_cadres(request):
	cadre = Cadre.objects.all()
	# cadres.unites  we can use related name in cadre_has_unite table
	return render(request, "affectation/show_cadres.html" , {'cadre' : cadre})
	



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
