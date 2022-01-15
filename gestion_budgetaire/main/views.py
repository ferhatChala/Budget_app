from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import  render, redirect
from .forms import (NewUserForm,
					AddUniteForm,AddDepForm,AddPos1Form,AddPos2Form,AddPos3Form,AddPos6Form,AddPos7Form,CompteScfForm,
					AddMonnaieForm, AddTauxChngForm, AddChapitreForm, AddPaysForm, 
					AffectCadreForm, AddCompteUniteForm, MontantCompteForm
					)
from .models import (User,
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
	#cadre_form = CadreForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid():
			user = user_form.save(commit=False)
			user.user_type = 6
			user.save()
			#cadre = cadre_form.save(commit=False)
			#cadre.user = user
			#cadre.save()
			messages.success(request, "Cadre added successfuly." )
			return redirect("/cadres_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	#form = NewUserForm()
	return render (request=request, template_name="registration/add_cadre.html", context={"user_form":user_form})

# ajouter chef departement
@login_required(login_url='login')
def ajouter_chef_dep(request):
	user_form = NewUserForm(request.POST or None)
	#chef_dep_form = ChefDepForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid():
			user = user_form.save(commit=False)
			user.user_type = 5
			user.save()
			#chef_dep = chef_dep_form.save(commit=False)
			#chef_dep.user = user
			#chef_dep.save()
			messages.success(request, "chef departement added successfuly." )
			return redirect("/chef_dep_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	#form = NewUserForm()
	return render (request=request, template_name="registration/add_chef_dep.html", context={"user_form":user_form})

# ajouter sous directeur
@login_required(login_url='login')
def ajouter_sous_dir(request):
	user_form = NewUserForm(request.POST or None)
	#sous_dir_form = SousDirForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid():
			user = user_form.save(commit=False)
			user.user_type = 4
			user.save()
			#sous_dir = sous_dir_form.save(commit=False)
			#sous_dir.user = user
			#sous_dir.save()
			messages.success(request, "sous directeur added successfuly." )
			return redirect("/sous_dir_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	#form = NewUserForm()
	return render (request=request, template_name="registration/add_sous_dir.html", context={"user_form":user_form})

# Ajouter directeur
@login_required(login_url='login')
def ajouter_dir(request):
	user_form = NewUserForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid():
			user = user_form.save(commit=False)
			user.user_type = 3
			user.save()
			messages.success(request, "Directeur added successfuly.")
			return redirect("/dir_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render (request=request, template_name="registration/add_dir.html", context={"user_form":user_form})


# ajouter content admin
@login_required(login_url='login')
def ajouter_content_admin(request):
	user_form = NewUserForm(request.POST or None)
	#content_admin_form = ContentAdminForm(request.POST or None)
	if request.method == "POST":
		if  user_form.is_valid():
			user = user_form.save(commit=False)
			user.user_type = 2
			user.save()
			#content_admin = content_admin_form.save(commit=False)
			#content_admin.user = user
			#content_admin.save()
			messages.success(request, "Content admin added successfuly." )
			return redirect("/content_admin_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	#form = NewUserForm()
	return render (request=request, template_name="registration/add_content_admin.html", context={"user_form":user_form})

# afficher toutes les cadres
@login_required(login_url='login')
def cadres_list(request):
	cadre = User.objects.filter(user_type=6)
	cadres_count = User.objects.filter(user_type=6).count()
	return render(request, "registration/cadres_list.html" , {'cadre' : cadre, 'cadres_count':cadres_count})

# afficher chefs departement
def chef_dep_list(request):
	chefs = User.objects.filter(user_type=5)
	chefs_count = User.objects.filter(user_type=5).count()
	return render(request, "registration/chef_dep_list.html" , {'chefs' : chefs, 'chefs_count':chefs_count})

# afficher sous directeurs 
def sous_dir_list(request):
	sous_dir = User.objects.filter(user_type=4)
	sous_dir_count = User.objects.filter(user_type=4).count()
	return render(request, "registration/sous_dir_list.html" , {'sous_dir' : sous_dir, 'sous_dir_count':sous_dir_count})

# Afficher Directeur 
def dir_list(request):
	dir = User.objects.filter(user_type=3)
	dir_count = User.objects.filter(user_type=3).count()
	return render(request, "registration/dir_list.html" , {'dir':dir, 'dir_count':dir_count})


# afficher content admin
def content_admin_list(request):
	content_admin = User.objects.filter(user_type=2)
	content_admin_count = User.objects.filter(user_type=2).count()
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

#Ajouter comptes scf 6 and 7 in same form
def add_pos6(request):
	pos6_form = AddPos6Form(request.POST or None)
	pos7_form = AddPos7Form(request.POST or None)
	if request.method == "POST":
		if  pos6_form.is_valid():
			pos6 = pos6_form.save(commit=False)
			get_ref = int(str(pos6.numero)[0:3])
			ref = SCF_Pos_3.objects.filter(numero=get_ref)
			if len(ref)==1:
				pos6.ref = ref[0]
				pos6.save()
				messages.success(request, "compte SCF 6 position added successfuly." )
			else:
				messages.error(request, "Unsuccessful this compte dosen't existe !")
				return redirect("/scf/add_pos6")
			return redirect("/scf/comptes_list")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="scfs/add_pos6.html", context={"pos6_form":pos6_form, "pos7_form":pos7_form})

def add_pos7(request):
	pos7_form = AddPos7Form(request.POST or None)
	if request.method == "POST":
		if  pos7_form.is_valid():
			pos7 = pos7_form.save(commit=False)
			get_ref = int(str(pos7.numero)[0:6])
			ref = SCF_Pos_6.objects.filter(numero=get_ref)
			if len(ref)==1:
				pos7.ref = ref[0]
				pos7.save()
				messages.success(request, "compte SCF 7 position added successfuly." )
			else:
				messages.error(request, "Unsuccessful this compte dosen't existe !")
				return redirect("/scf/add_pos7")
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
	comptes = Compte_SCF.objects.filter(pos = 1)
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
			taux_chng = taux_chng_form.save(commit=False)
			c = taux_chng.monnaie.code_alpha + str(taux_chng.annee)
			tch = Taux_de_change.objects.filter(code=c)
			if len(tch)==0:
				taux_chng.code = c
				taux_chng.save()
				messages.success(request, "Taux de change added successfuly." )
			else:
				messages.error(request, "Unsuccessful . Taux de change éxiste déja.")
				return redirect("/ref/add_taux_chng")			
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

# afficher l'unités d'un cadre 
def show_unites(request, id):
	c = User.objects.get(id=id)
	unites = Cadre_has_Unite.objects.filter(cadre = c)
	return render(request,"affectation/show_unites.html", {'unites':unites, 'c':c})

# supprimer l'unité pour une cadre 
def delete_unite_of_cadre(request, id):
	form = Cadre_has_Unite.objects.get(id=id)
	form.delete()
	return HttpResponseRedirect("/aff/show_cadres")

# add_unite aux cadre donnée
def add_unite_to_cadre(request, id):
	cadre = User.objects.get(id=id)
	form = AffectCadreForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			unite_to_cadre = form.save(commit=False)
			unite_to_cadre.cadre = cadre
			unite_to_cadre.save()
			messages.success(request, "unite added successfuly." )
			return redirect("/aff/show_unites/"+ str(id)+"")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="affectation/add_unite_to_cadre.html", context={"form":form})

# affichier les cadres
def show_cadres(request):
	cadre = User.objects.filter(user_type=6)
	# cadres.unites  we can use related name in cadre_has_unite table
	return render(request, "affectation/show_cadres.html" , {'cadre' : cadre})
	

# -----------------------------------------------------------------------------------

# ------------ Affectation des comptes aux unités ---------------------------------------------------

# ajouter compte aux unité
def add_compte_to_unite(request, id):
	unite = Unite.objects.get(id=id)
	form = AddCompteUniteForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			compte_unite = form.save(commit=False)
			compte_unite.unite = unite
			compte_unite.existe = True
			compte_unite.added_by = request.user
			compte_unite.save()
			messages.success(request, "compte added successfuly to unite." )
			return redirect("/show_comptes/"+ str(id)+"")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="unite_comptes/add_compte_to_unite.html", context={"form":form})

# afficher toutes les unités
def all_unites(request):
	unites = Unite.objects.all()
	return render(request, "unite_comptes/all_unites.html" , {'unites' : unites})

# afficher les comptes d'un unité 
def show_comptes(request, id):
	u = Unite.objects.get(id=id)
	comptes = Unite_has_Compte.objects.filter(unite = u)
	return render(request,"unite_comptes/comptes.html", {'comptes':comptes, 'u':u})
# supprimer compte pour une unité 

# Proposition budget --------------------------------------------------------------------

def unites(request):
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	return render(request,"proposition/unites.html", {'unites':unites})

def unite_detail(request, id):
	unite = Unite.objects.get(id=id)
	comptes_nbr = Unite_has_Compte.objects.filter(unite=unite).count()
	comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS" ).count()
	if comptes_done_nbr==0:
		pr = 0
	else:
		pr = (comptes_done_nbr/comptes_nbr)*100
	return render(request,"proposition/unite_detail.html", {'unite':unite, 'comptes_nbr':comptes_nbr, "pr":pr})

def offre_comptes(request, id):
	unite = Unite.objects.get(id=id)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=1)
	return render(request,"proposition/offre_comptes.html", {'unite':unite, 'comptes':comptes})

def traffic_comptes(request, id):
	unite = Unite.objects.get(id=id)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=2)
	return render(request,"proposition/traffic_comptes.html", {'unite':unite, 'comptes':comptes})

def ca_emmission_comptes(request, id):
	unite = Unite.objects.get(id=id)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=3)
	return render(request,"proposition/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes})

def ca_transport_comptes(request, id):
	unite = Unite.objects.get(id=id)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=4)
	return render(request,"proposition/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes})

def recettes_comptes(request, id):
	unite = Unite.objects.get(id=id)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=5)
	return render(request,"proposition/recettes_comptes.html", {'unite':unite, 'comptes':comptes})

def depense_fonc_comptes(request, id):
	unite = Unite.objects.get(id=id)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6)
	return render(request,"proposition/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes})

def depense_exp_comptes(request, id):
	unite = Unite.objects.get(id=id)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7)
	return render(request,"proposition/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes})




# depense_fonc_comptes
# depense_exp_comptes


# add montant to compte 
def add_montant(request, id):
	unite_compte = Unite_has_Compte.objects.get(id=id)
	montant_form = MontantCompteForm(request.POST or None)
	if request.method == "POST":
		if  montant_form.is_valid():
			montant_compte = montant_form.save(commit=False)
			montant_compte.unite_compte = unite_compte
			montant_compte.type_bdg = "PROPOS"
			montant_compte.annee = 2022
			if request.user.user_type==6:
				montant_compte.montant_cadre = montant_compte.montant
				montant_compte.vld_cadre = True
				montant_compte.validation = "CADRE"
			
			montant_compte.save()
			messages.success(request, "compte added successfuly to unite." )
			return redirect("/proposition/unite/offre/"+ str(unite_compte.unite.id)+"")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="proposition/add_montant.html", context={"montant_form":montant_form, "unite_compte":unite_compte})

