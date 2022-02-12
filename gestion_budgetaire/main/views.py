from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import  render, redirect, get_object_or_404
from .forms import (NewUserForm, InterimForm, AnneeBdgForm, UpdateAnneeBdgForm,
					AddUniteForm,AddDepForm,AddPos1Form,AddPos2Form,AddPos3Form,AddPos6Form,AddPos7Form,CompteScfForm,
					AddMonnaieForm, AddTauxChngForm, AddChapitreForm, AddPaysForm, 
					AffectCadreForm, AddCompteUniteForm, MontantCompteForm,UpdateMontantCompteForm,CommentaireForm
					)
from .models import (User, Interim,Commentaire,
                    Departement, Unite, Pays, Monnaie, Taux_de_change, Chapitre,
                    SCF_Pos_1, SCF_Pos_2, SCF_Pos_3, SCF_Pos_6, SCF_Pos_7,Compte_SCF,
                    Unite_has_Compte, Compte_has_Montant, Cadre_has_Unite, Annee_Budgetaire
                    )
from django.contrib.auth import login
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
import math
from datetime import date
from django.contrib.auth import get_user_model
User = get_user_model()

# home
@login_required(login_url='login')
def home(request):
    return render(request, "base.html" , {'users_count':User.objects.all().count(), 'unite_count':Unite.objects.all().count(), 'comptes':SCF_Pos_6.objects.all().count() })

# ------------ users management -----------------------------------------------

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

# afichage 
@login_required(login_url='login')
def cadres_list(request):
	cadre = User.objects.filter(user_type=6)
	cadres_count = User.objects.filter(user_type=6).count()
	return render(request, "registration/cadres_list.html" , {'cadre' : cadre, 'cadres_count':cadres_count})

def chef_dep_list(request):
	chefs = User.objects.filter(user_type=5)
	chefs_count = User.objects.filter(user_type=5).count()
	return render(request, "registration/chef_dep_list.html" , {'chefs' : chefs, 'chefs_count':chefs_count})

def sous_dir_list(request):
	sous_dir = User.objects.filter(user_type=4)
	sous_dir_count = User.objects.filter(user_type=4).count()
	return render(request, "registration/sous_dir_list.html" , {'sous_dir' : sous_dir, 'sous_dir_count':sous_dir_count})

def dir_list(request):
	dir = User.objects.filter(user_type=3)
	dir_count = User.objects.filter(user_type=3).count()
	return render(request, "registration/dir_list.html" , {'dir':dir, 'dir_count':dir_count})

def content_admin_list(request):
	content_admin = User.objects.filter(user_type=2)
	content_admin_count = User.objects.filter(user_type=2).count()
	return render(request, "registration/content_admin_list.html" , {'content_admin' : content_admin, 'content_admin_count':content_admin_count})

# supprimer
@login_required(login_url='login')
def delete_user(request, id):
    form = User.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/cadres_list")

#update
class UserUpdateView(UpdateView):
	model = User
	fields = '__all__'
	template_name = "registration/update_user.html"
	success_url = "/"



# gestion des interimes ---------------------------------------------------
def interims(request):
	interims = Interim.objects.all()
	return render(request, "registration/interims.html" , {'interims':interims})

def add_interim(request):
	form = InterimForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			interim = form.save()
			messages.success(request, "Intérim added successfuly." )
			return redirect("/interims")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="registration/add_interim.html", context={"form":form})


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
	taux_chng = Taux_de_change.objects.all().order_by('-annee')
	taux_chng_count = Taux_de_change.objects.all().count()
	return render(request, "others/taux_chng_list.html" , {'taux_chng' : taux_chng, 'taux_chng_count':taux_chng_count})

class TauxUpdateView(UpdateView):
	model = Taux_de_change
	fields = '__all__'
	template_name = "others/update_taux_chng.html"
	success_url = "/ref/taux_chng_list"

def delete_taux_chng(request, id):
    form = Taux_de_change.objects.get(id=id)
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

# annee budgétaire -------------------------------------------

def add_annee_bdg(request):
	annee_bdg_form = AnneeBdgForm(request.POST or None)
	if request.method == "POST":
		if  annee_bdg_form.is_valid():
			annee_bdg = annee_bdg_form.save(commit=False)
			annee_bdg.code = annee_bdg.type_bdg + str(annee_bdg.annee)
			annee_bdg.save()
			messages.success(request, "Année Budgétaire added successfuly." )
			return redirect("/annee_bdg")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="others/add_annee_bdg.html", context={"annee_bdg_form":annee_bdg_form})

def annee_bdg(request):
	annee_bdg = Annee_Budgetaire.objects.all().order_by('-annee')
	return render(request, "others/annee_bdg_list.html" , {'annee_bdg' : annee_bdg })

def update_annee_bdg(request, id): 
	annee_bdg = get_object_or_404(Annee_Budgetaire, id = id)
	form = UpdateAnneeBdgForm(request.POST or None, instance = annee_bdg)
	if form.is_valid():
		form.save()
		messages.success(request, "Année budgétaire updated successfuly." )
		return redirect("/annee_bdg")

	return render (request=request, template_name="others/update_annee_bdg.html", context={"form":form, "annee_bdg":annee_bdg})

def delete_annee_bdg(request, id):
    form = Annee_Budgetaire.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/annee_bdg")


# Affectation des cadres aux unités ---------------------------------------------------

def show_cadres(request):
	cadre = User.objects.filter(user_type=6)
	# cadres.unites  we can use related name in cadre_has_unite table
	return render(request, "affectation/show_cadres.html" , {'cadre' : cadre})
	
def show_unites(request, id):
	c = User.objects.get(id=id)
	unites = Cadre_has_Unite.objects.filter(cadre = c)
	return render(request,"affectation/show_unites.html", {'unites':unites, 'c':c})

def add_unite_to_cadre(request, id):
	cadre = User.objects.get(id=id)
	form = AffectCadreForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			unite_to_cadre = form.save(commit=False)
			unite_to_cadre.cadre = cadre
			unite_to_cadre.code = unite_to_cadre.unite.code_alpha + str(unite_to_cadre.cadre.id)
			unite_to_cadre.save()
			messages.success(request, "unite added successfuly." )
			return redirect("/aff/show_unites/"+ str(id)+"")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="affectation/add_unite_to_cadre.html", context={"form":form})

def delete_unite_of_cadre(request, id):
	form = Cadre_has_Unite.objects.get(id=id)
	cu_id = form.cadre.id
	form.delete()
	messages.success(request, "United removed successfuly." )
	return HttpResponseRedirect("/aff/show_unites/"+ str(cu_id)+"")


# Affectation des comptes aux unités ---------------------------------------------------
def all_unites(request):
	unites = Unite.objects.all()
	return render(request, "unite_comptes/all_unites.html" , {'unites' : unites})

def add_compte_to_unite(request, id):
	unite = Unite.objects.get(id=id)
	form = AddCompteUniteForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			compte_unite = form.save(commit=False)
			compte_unite.unite = unite
			compte_unite.added_by = request.user
			compte_unite.code = compte_unite.unite.code_alpha + str(compte_unite.compte.numero) + compte_unite.regle_par.code_alpha + compte_unite.reseau_compte
			compte_unite.save()
			messages.success(request, "compte added successfuly to unite." )
			return redirect("/show_comptes/"+ str(id)+"")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="unite_comptes/add_compte_to_unite.html", context={"form":form})

def show_comptes(request, id):
	u = Unite.objects.get(id=id)
	comptes = Unite_has_Compte.objects.filter(unite = u)
	return render(request,"unite_comptes/comptes.html", {'comptes':comptes, 'u':u})

def delete_compte_of_unite(request, id):
	form = Unite_has_Compte.objects.get(id=id)
	u_id = form.unite.id
	form.delete()
	messages.success(request, "Compte removed successfuly." )
	return HttpResponseRedirect("/show_comptes/"+ str(u_id)+"")

# Proposition budget --------------------------------------------------------------------

# affichage des unites et leur comptes par chapitre

def unites(request):
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]
	dep_unites = Unite.objects.filter(departement=request.user.departement)
	return render(request,"proposition/unites.html", {'unites':unites, 'dep_unites':dep_unites, 'budget':budget})

def unite_detail(request, id):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]
	unite = Unite.objects.get(id=id)
	comptes_nbr = Unite_has_Compte.objects.filter(unite=unite).count()
	comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS").count()
	comptes_vld_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True).count()	
	# porcentage de saiser pour l unite
	if comptes_nbr == 0:
		pr_cdr = 0
	else :
		pr_cdr = int(math.modf((comptes_done_nbr / comptes_nbr)*100)[1])

	if comptes_nbr == 0:
		pr_vcd = 0
	else :
		pr_vcd = int(math.modf((comptes_vld_nbr / comptes_nbr)*100)[1])

	#nombre de comptes pour chaque chapitre
	offre_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=1).count()
	traffic_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=2).count()
	ca_emmission_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=3).count()
	ca_transport_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=4).count()
	recettes_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=5).count()
	depense_fonc_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=6).count()
	depense_exp_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=7).count()
	# nombre de comptes saisie
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=1).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=4).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par chef dep
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()
	#Check if chapitre is saisié 
	offre_s = offre_nbr==offre_done_nbr
	traffic_s = traffic_nbr==traffic_done_nbr
	ca_emmission_s = ca_emmission_nbr==ca_emmission_done_nbr
	ca_transport_s = ca_transport_nbr==ca_transport_done_nbr
	recettes_s = recettes_nbr==recettes_done_nbr
	depense_fonc_s = depense_fonc_nbr==depense_fonc_done_nbr
	depense_exp_s = depense_exp_nbr==depense_exp_done_nbr
	#Check if chapitre is  non saisié
	offre_non_s = offre_done_nbr == 0
	traffic_non_s = traffic_done_nbr == 0
	ca_emmission_non_s = ca_emmission_done_nbr == 0
	ca_transport_non_s = ca_transport_done_nbr == 0
	recettes_non_s = recettes_done_nbr == 0
	depense_fonc_non_s = depense_fonc_done_nbr == 0
	depense_exp_non_s = depense_exp_done_nbr == 0

	#Check if chapitre is validé par chef dep
	offre_v = offre_nbr==offre_valid_nbr
	traffic_v = traffic_nbr==traffic_valid_nbr
	ca_emmission_v = ca_emmission_nbr==ca_emmission_valid_nbr
	ca_transport_v = ca_transport_nbr==ca_transport_valid_nbr
	recettes_v = recettes_nbr==recettes_valid_nbr
	depense_fonc_v = depense_fonc_nbr==depense_fonc_valid_nbr
	depense_exp_v = depense_exp_nbr==depense_exp_valid_nbr

	#Check if chapitre is not validé par chef dep ( = compte validé)
	offre_non_v = offre_valid_nbr == 0
	traffic_non_v = traffic_valid_nbr == 0
	ca_emmission_non_v = ca_emmission_valid_nbr == 0
	ca_transport_non_v = ca_transport_valid_nbr == 0
	recettes_non_v = recettes_valid_nbr == 0
	depense_fonc_non_v = depense_fonc_valid_nbr == 0
	depense_exp_non_v = depense_exp_valid_nbr == 0

	return render(request,"proposition/unite_detail.html", {'unite':unite, 'comptes_nbr':comptes_nbr, 'comptes_done_nbr':comptes_done_nbr, 'pr_cdr':pr_cdr, 'pr_vcd':pr_vcd, 'budget':budget,
															'offre_s':offre_s, 'traffic_s':traffic_s, 'ca_emmission_s':ca_emmission_s, 'ca_transport_s':ca_transport_s,
															'recettes_s':recettes_s, 'depense_fonc_s':depense_fonc_s, 'depense_exp_s':depense_exp_s,
															'offre_v':offre_v, 'traffic_v':traffic_v, 'ca_emmission_v':ca_emmission_v, 'ca_transport_v':ca_transport_v,
															'recettes_v':recettes_v, 'depense_fonc_v':depense_fonc_v, 'depense_exp_v':depense_exp_v,
															'offre_non_s':offre_non_s, 'traffic_non_s':traffic_non_s, 'ca_emmission_non_s':ca_emmission_non_s, 'ca_transport_non_s':ca_transport_non_s,
															'recettes_non_s':recettes_non_s, 'depense_fonc_non_s':depense_fonc_non_s, 'depense_exp_non_s':depense_exp_non_s,
															'offre_non_v':offre_non_v, 'traffic_non_v':traffic_non_v, 'ca_emmission_non_v':ca_emmission_non_v, 'ca_transport_non_v':ca_transport_non_v,
															'recettes_non_v':recettes_non_v, 'depense_fonc_non_v':depense_fonc_non_v, 'depense_exp_non_v':depense_exp_non_v
															})

def offre_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=1)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	offre_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=1).count()
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=1).count()
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	
	offre_s = offre_nbr==offre_done_nbr
	offre_non_s = offre_done_nbr == 0
	offre_v = offre_nbr==offre_valid_nbr

	return render(request,"proposition/offre_comptes.html", {'unite':unite, 'comptes':comptes, "offre_s":offre_s, "offre_non_s":offre_non_s, "offre_v":offre_v, 'budget':budget, 'cm_dict':cm_dict})

def traffic_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=2)
	traffic_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=2).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=2).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()

	traffic_s = traffic_nbr==traffic_done_nbr
	traffic_non_s = traffic_done_nbr == 0
	traffic_v = traffic_nbr==traffic_valid_nbr

	return render(request,"proposition/traffic_comptes.html", {'unite':unite, 'comptes':comptes,  "traffic_s":traffic_s, "traffic_non_s":traffic_non_s, "traffic_v":traffic_v, 'budget':budget })

def ca_emmission_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=3)
	ca_emmission_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=3).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=3).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	
	ca_emmission_s = ca_emmission_nbr==ca_emmission_done_nbr
	ca_emmission_non_s = ca_emmission_done_nbr == 0
	ca_emmission_v = ca_emmission_nbr==ca_emmission_valid_nbr

	return render(request,"proposition/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes, "ca_emmission_s":ca_emmission_s, "ca_emmission_non_s":ca_emmission_non_s, "ca_emmission_v":ca_emmission_v, 'budget':budget})

def ca_transport_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=4).order_by('-reseau_compte')
	ca_transport_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=4).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=4).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()

	ca_transport_s = ca_transport_nbr==ca_transport_done_nbr
	ca_transport_non_s = ca_transport_done_nbr == 0
	ca_transport_v = ca_transport_nbr==ca_transport_valid_nbr

	return render(request,"proposition/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes, "ca_transport_s":ca_transport_s, "ca_transport_non_s":ca_transport_non_s, "ca_transport_v":ca_transport_v, 'budget':budget})

def recettes_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=5)
	recettes_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=5).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=5).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()

	recettes_s = recettes_nbr==recettes_done_nbr
	recettes_non_s = recettes_done_nbr == 0
	recettes_v = recettes_nbr==recettes_valid_nbr

	return render(request,"proposition/recettes_comptes.html", {'unite':unite, 'comptes':comptes, "recettes_s":recettes_s, "recettes_non_s":recettes_non_s, "recettes_v":recettes_v, 'budget':budget})

def depense_fonc_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6)
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=6)
	comptes_regle_par_autre = []
	for c in comptes:
		if c.regle_par != unite:
			comptes_regle_par_autre.append(c)	
	# pos 2 comptes 
	all_c2 = SCF_Pos_2.objects.all()
	c2_par_unite = []
	for c2 in all_c2:
		for cu in comptes_regle_par_unite:
			if c2.numero == cu.compte.ref.ref.ref.numero:
				c2_par_unite.append(c2)

	c2_par_autre = []
	for c2 in all_c2:
		for cu in comptes_regle_par_autre:
			if c2.numero == cu.compte.ref.ref.ref.numero:
				c2_par_autre.append(c2)
	
	c2_par_unite = list(dict.fromkeys(c2_par_unite))
	c2_par_autre = list(dict.fromkeys(c2_par_autre))
	
	# clacule les pos 2 saisier 
	



	#pos 3 comptes
	all_c3 = SCF_Pos_3.objects.all()
	c3_par_unite = []
	for c3 in all_c3:
		for cu in comptes_regle_par_unite:
			if c3.numero == cu.compte.ref.ref.numero:
				c3_par_unite.append(c3)

	c3_par_autre = []
	for c3 in all_c3:
		for cu in comptes_regle_par_autre:
			if c3.numero == cu.compte.ref.ref.numero:
				c3_par_autre.append(c3)
	
	c3_par_unite = list(dict.fromkeys(c3_par_unite))
	c3_par_autre = list(dict.fromkeys(c3_par_autre))

	#comptes_regle_par_autre = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite compte__chapitre__code_num=6)	
	
	depense_fonc_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6).count()
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=6).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()


	depense_fonc_s = depense_fonc_nbr==depense_fonc_done_nbr
	depense_fonc_non_s = depense_fonc_done_nbr == 0
	depense_fonc_v = depense_fonc_nbr==depense_fonc_valid_nbr

	return render(request,"proposition/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes, 'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																  "depense_fonc_s":depense_fonc_s, "depense_fonc_non_s":depense_fonc_non_s, "depense_fonc_v":depense_fonc_v, 'budget':budget,
																  "c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre})

def depense_exp_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7)
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=7)
	comptes_regle_par_autre = []
	for c in comptes:
		if c.regle_par != unite:
			comptes_regle_par_autre.append(c)	

	all_c2 = SCF_Pos_2.objects.all()
	c2_par_unite = []
	for c2 in all_c2:
		for cu in comptes_regle_par_unite:
			if c2.numero == cu.compte.ref.ref.ref.numero:
				c2_par_unite.append(c2)

	c2_par_autre = []
	for c2 in all_c2:
		for cu in comptes_regle_par_autre:
			if c2.numero == cu.compte.ref.ref.ref.numero:
				c2_par_autre.append(c2)
	
	c2_par_unite = list(dict.fromkeys(c2_par_unite))
	c2_par_autre = list(dict.fromkeys(c2_par_autre))

	# pos 3 comptes
	all_c3 = SCF_Pos_3.objects.all()
	c3_par_unite = []
	for c3 in all_c3:
		for cu in comptes_regle_par_unite:
			if c3.numero == cu.compte.ref.ref.numero:
				c3_par_unite.append(c3)

	c3_par_autre = []
	for c3 in all_c3:
		for cu in comptes_regle_par_autre:
			if c3.numero == cu.compte.ref.ref.numero:
				c3_par_autre.append(c3)
	
	c3_par_unite = list(dict.fromkeys(c3_par_unite))
	c3_par_autre = list(dict.fromkeys(c3_par_autre))	


	depense_exp_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7).count()
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", unite_compte__compte__chapitre__code_num=7).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="PROPOS", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()

	depense_exp_s = depense_exp_nbr==depense_exp_done_nbr
	depense_exp_non_s = depense_exp_done_nbr == 0
	depense_exp_v = depense_exp_nbr==depense_exp_valid_nbr

	return render(request,"proposition/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes,  'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																	"depense_exp_s":depense_exp_s, "depense_exp_non_s":depense_exp_non_s, "depense_exp_v":depense_exp_v, 'budget':budget,
																	"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre})

# add montant to compte 
def add_montant(request, id):
	unite_compte = Unite_has_Compte.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comment_form = CommentaireForm(request.POST or None)
	montant_form = MontantCompteForm(request.POST or None)
	if request.method == "POST":
		if  montant_form.is_valid():
			montant_compte = montant_form.save(commit=False)
			montant_compte.unite_compte = unite_compte
			montant_compte.type_bdg = "PROPOS"
			montant_compte.annee_budgetaire = budget
			montant_compte.code = str(montant_compte.unite_compte.id) + montant_compte.annee_budgetaire.code + montant_compte.unite_compte.monnaie.code_alpha + montant_compte.unite_compte.regle_par.code_alpha
			if comment_form.is_valid():
				comment = comment_form.save(commit=False)
				comment.comment_type = "M"
				comment.user = request.user
				comment.save()
				montant_compte.commentaire_montant = comment
			
			if request.user.user_type==6:
				montant_compte.montant_cadre = montant_compte.montant
				montant_compte.vld_cadre = True
				montant_compte.validation = "CADRE"

			if request.user.user_type==5:
				montant_compte.montant_chef_dep = montant_compte.montant
				montant_compte.vld_chef_dep = True
				montant_compte.validation = "CHEFD"
			
			if request.user.user_type==4:
				montant_compte.montant_sous_dir = montant_compte.montant
				montant_compte.vld_sous_dir = True
				montant_compte.validation = "SOUSD"				
			
			montant_compte.save()
			messages.success(request, "compte added successfuly to unite." )
			# Redirecter vers chaque chapitre
			if unite_compte.compte.chapitre.code_num== 1:
				return redirect("/proposition/unite/offre/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 2:
				return redirect("/proposition/unite/traffic/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 3:
				return redirect("/proposition/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 4:
				return redirect("/proposition/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 5:
				return redirect("/proposition/unite/recettes/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 6:
				return redirect("/proposition/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 7:
				return redirect("/proposition/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
			else:
				return redirect("/proposition/unites")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="proposition/add_montant.html", context={"montant_form":montant_form, "comment_form":comment_form, "unite_compte":unite_compte, "budget":budget})

def update_montant(request, id): 
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]	
	form = UpdateMontantCompteForm(request.POST or None, instance = montant)
	if form.is_valid():
		form.save()
		messages.success(request, "Montant updated successfuly." )
		new_montant = get_object_or_404(Compte_has_Montant, id = id)
		if request.user.user_type==6:
			new_montant.montant_cadre = new_montant.montant
			new_montant.vld_cadre = True
			new_montant.save()
		if request.user.user_type==5:
			new_montant.montant_chef_dep = new_montant.montant
			new_montant.vld_chef_dep = True
			new_montant.validation = "CHEFD"
			new_montant.save()
		if request.user.user_type==4:
			new_montant.montant_sous_dir = new_montant.montant
			new_montant.vld_sous_dir = True
			new_montant.validation = "SOUSD"
			new_montant.save()
		
		# Redirecter vers chaque chapitre
		if unite_compte.compte.chapitre.code_num== 1:
			return redirect("/proposition/unite/offre/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 2:
			return redirect("/proposition/unite/traffic/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 3:
			return redirect("/proposition/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 4:
			return redirect("/proposition/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 5:
			return redirect("/proposition/unite/recettes/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 6:
			return redirect("/proposition/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 7:
			return redirect("/proposition/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
		else:
			return redirect("/proposition/unites")
	return render (request=request, template_name="proposition/update_montant.html", context={"form":form, "unite_compte":unite_compte, "montant":montant, "budget":budget})

def valid_montant(request, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte
	if request.user.user_type==6:
		new_montant.vld_cadre = True
		new_montant.save()
	if request.user.user_type==5:
		new_montant.vld_chef_dep = True
		new_montant.validation = "CHEFD"
		new_montant.save()
	if request.user.user_type==4:
		new_montant.vld_sous_dir = True
		new_montant.validation = "SOUSD"
		new_montant.save()

	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/proposition/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/proposition/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/proposition/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/proposition/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/proposition/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/proposition/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/proposition/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/proposition/unites")

def cancel_valid_montant(request, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte
	if request.user.user_type==6:
		new_montant.vld_cadre = False
		new_montant.save()
	if request.user.user_type==5:
		new_montant.vld_chef_dep = False
		new_montant.validation = "CHEFD"
		new_montant.save()
	if request.user.user_type==4:
		new_montant.vld_sous_dir = False
		new_montant.validation = "SOUSD"
		new_montant.save()
	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/proposition/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/proposition/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/proposition/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/proposition/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/proposition/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/proposition/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/proposition/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/proposition/unites")

def add_new_compte(request, id):
	unite = Unite.objects.get(id=id)
	form = AddCompteUniteForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			compte_unite = form.save(commit=False)
			compte_unite.unite = unite
			compte_unite.added_by = request.user
			compte_unite.code = compte_unite.unite.code_alpha + str(compte_unite.compte.numero) + compte_unite.regle_par.code_alpha + compte_unite.reseau_compte
			compte_unite.save()
			messages.success(request, "compte added successfuly." )
			return HttpResponseRedirect("/proposition/unite/"+ str(unite.id)+"")
			
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="proposition/add_new_compte.html", context={"form":form})

def delete_added_compte(request,id):
	form = Unite_has_Compte.objects.get(id=id)
	unite = form.unite
	compte = form.compte
	form.delete()
	# Redirecter vers chaque chapitre
	if compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/proposition/unite/offre/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/proposition/unite/traffic/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/proposition/unite/ca_emmission/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/proposition/unite/ca_transport/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/proposition/unite/recettes/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/proposition/unite/depense_fonc/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/proposition/unite/depense_exp/"+ str(unite.id)+"")
	else:
		return HttpResponseRedirect("/proposition/unites")	

# comments
def update_comment(request, id): 
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]
	comment = get_object_or_404(Commentaire, id = id)
	form = CommentaireForm(request.POST or None, instance = comment)
	if form.is_valid():
		form.save()
		messages.success(request, "Commentaire updated successfuly." )
		return redirect("/proposition/unites")

	return render (request=request, template_name="proposition/update_comment.html", context={"form":form, "comment":comment, "budget":budget})

def delete_comment(request, id):
    form = Commentaire.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/proposition/unites")

# consultation proposition budget 
def annees_bdg_prop(request):
	budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	dep_unites = Unite.objects.filter(departement=request.user.departement)
	all_unites = Unite.objects.all()
	return render(request,"proposition/consultation/annees.html", {'budgets':budgets, 'unites':unites, 'dep_unites':dep_unites, 'all_unites':all_unites})

# -------------------------------------- Fin Proposition budget --------------------------------------------------------

# Réunion --------------------------------------------------------------------------------------------------------------

# affichage des unites et leur comptes par chapitre

def unites_reunion(request):
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]
	dep_unites = Unite.objects.filter(departement=request.user.departement)
	return render(request,"reunion/unites.html", {'unites':unites, 'dep_unites':dep_unites, 'budget':budget})

def unite_detail_reunion(request, id):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]
	unite = Unite.objects.get(id=id)
	comptes_nbr = Unite_has_Compte.objects.filter(unite=unite).count()
	comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN").count()
	comptes_vld_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True).count()	
	# porcentage de saiser pour l unite
	if comptes_nbr == 0:
		pr_cdr = 0
	else :
		pr_cdr = int(math.modf((comptes_done_nbr / comptes_nbr)*100)[1])

	if comptes_nbr == 0:
		pr_vcd = 0
	else :
		pr_vcd = int(math.modf((comptes_vld_nbr / comptes_nbr)*100)[1])

	#nombre de comptes pour chaque chapitre
	offre_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=1).count()
	traffic_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=2).count()
	ca_emmission_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=3).count()
	ca_transport_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=4).count()
	recettes_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=5).count()
	depense_fonc_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=6).count()
	depense_exp_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=7).count()
	# nombre de comptes saisie
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=1).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=4).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par chef dep
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()
	#Check if chapitre is saisié 
	offre_s = offre_nbr==offre_done_nbr
	traffic_s = traffic_nbr==traffic_done_nbr
	ca_emmission_s = ca_emmission_nbr==ca_emmission_done_nbr
	ca_transport_s = ca_transport_nbr==ca_transport_done_nbr
	recettes_s = recettes_nbr==recettes_done_nbr
	depense_fonc_s = depense_fonc_nbr==depense_fonc_done_nbr
	depense_exp_s = depense_exp_nbr==depense_exp_done_nbr
	#Check if chapitre is  non saisié
	offre_non_s = offre_done_nbr == 0
	traffic_non_s = traffic_done_nbr == 0
	ca_emmission_non_s = ca_emmission_done_nbr == 0
	ca_transport_non_s = ca_transport_done_nbr == 0
	recettes_non_s = recettes_done_nbr == 0
	depense_fonc_non_s = depense_fonc_done_nbr == 0
	depense_exp_non_s = depense_exp_done_nbr == 0

	#Check if chapitre is validé par chef dep
	offre_v = offre_nbr==offre_valid_nbr
	traffic_v = traffic_nbr==traffic_valid_nbr
	ca_emmission_v = ca_emmission_nbr==ca_emmission_valid_nbr
	ca_transport_v = ca_transport_nbr==ca_transport_valid_nbr
	recettes_v = recettes_nbr==recettes_valid_nbr
	depense_fonc_v = depense_fonc_nbr==depense_fonc_valid_nbr
	depense_exp_v = depense_exp_nbr==depense_exp_valid_nbr

	#Check if chapitre is not validé par chef dep ( = compte validé)
	offre_non_v = offre_valid_nbr == 0
	traffic_non_v = traffic_valid_nbr == 0
	ca_emmission_non_v = ca_emmission_valid_nbr == 0
	ca_transport_non_v = ca_transport_valid_nbr == 0
	recettes_non_v = recettes_valid_nbr == 0
	depense_fonc_non_v = depense_fonc_valid_nbr == 0
	depense_exp_non_v = depense_exp_valid_nbr == 0

	return render(request,"reunion/unite_detail.html", {'unite':unite, 'comptes_nbr':comptes_nbr, 'comptes_done_nbr':comptes_done_nbr, 'pr_cdr':pr_cdr, 'pr_vcd':pr_vcd, 'budget':budget,
															'offre_s':offre_s, 'traffic_s':traffic_s, 'ca_emmission_s':ca_emmission_s, 'ca_transport_s':ca_transport_s,
															'recettes_s':recettes_s, 'depense_fonc_s':depense_fonc_s, 'depense_exp_s':depense_exp_s,
															'offre_v':offre_v, 'traffic_v':traffic_v, 'ca_emmission_v':ca_emmission_v, 'ca_transport_v':ca_transport_v,
															'recettes_v':recettes_v, 'depense_fonc_v':depense_fonc_v, 'depense_exp_v':depense_exp_v,
															'offre_non_s':offre_non_s, 'traffic_non_s':traffic_non_s, 'ca_emmission_non_s':ca_emmission_non_s, 'ca_transport_non_s':ca_transport_non_s,
															'recettes_non_s':recettes_non_s, 'depense_fonc_non_s':depense_fonc_non_s, 'depense_exp_non_s':depense_exp_non_s,
															'offre_non_v':offre_non_v, 'traffic_non_v':traffic_non_v, 'ca_emmission_non_v':ca_emmission_non_v, 'ca_transport_non_v':ca_transport_non_v,
															'recettes_non_v':recettes_non_v, 'depense_fonc_non_v':depense_fonc_non_v, 'depense_exp_non_v':depense_exp_non_v
															})

def offre_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=1)
	#montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite, unite_compte__compte__chapitre__code_num=1)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]
	
	#print(cm_dict)

	# montants = Compte_has_Monatnt.objects.filter(unite_compte.unite=unite, type_bdg="REUN", unite_compte_compte__chapitre__code_num=1)
	offre_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=1).count()
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=1).count()
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	
	offre_s = offre_nbr==offre_done_nbr
	offre_non_s = offre_done_nbr == 0
	offre_v = offre_nbr==offre_valid_nbr

	return render(request,"reunion/offre_comptes.html", {'unite':unite, 'comptes':comptes, "offre_s":offre_s, "offre_non_s":offre_non_s, "offre_v":offre_v, 'budget':budget, 'cm_dict':cm_dict})

def traffic_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=2)
	traffic_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=2).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=2).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()

	traffic_s = traffic_nbr==traffic_done_nbr
	traffic_non_s = traffic_done_nbr == 0
	traffic_v = traffic_nbr==traffic_valid_nbr

	return render(request,"reunion/traffic_comptes.html", {'unite':unite, 'comptes':comptes,  "traffic_s":traffic_s, "traffic_non_s":traffic_non_s, "traffic_v":traffic_v, 'budget':budget })

def ca_emmission_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=3)
	ca_emmission_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=3).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=3).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	
	ca_emmission_s = ca_emmission_nbr==ca_emmission_done_nbr
	ca_emmission_non_s = ca_emmission_done_nbr == 0
	ca_emmission_v = ca_emmission_nbr==ca_emmission_valid_nbr

	return render(request,"reunion/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes, "ca_emmission_s":ca_emmission_s, "ca_emmission_non_s":ca_emmission_non_s, "ca_emmission_v":ca_emmission_v, 'budget':budget})

def ca_transport_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=4).order_by('-reseau_compte')
	ca_transport_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=4).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=4).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()

	ca_transport_s = ca_transport_nbr==ca_transport_done_nbr
	ca_transport_non_s = ca_transport_done_nbr == 0
	ca_transport_v = ca_transport_nbr==ca_transport_valid_nbr

	return render(request,"reunion/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes, "ca_transport_s":ca_transport_s, "ca_transport_non_s":ca_transport_non_s, "ca_transport_v":ca_transport_v, 'budget':budget})

def recettes_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=5)
	recettes_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=5).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=5).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()

	recettes_s = recettes_nbr==recettes_done_nbr
	recettes_non_s = recettes_done_nbr == 0
	recettes_v = recettes_nbr==recettes_valid_nbr

	return render(request,"reunion/recettes_comptes.html", {'unite':unite, 'comptes':comptes, "recettes_s":recettes_s, "recettes_non_s":recettes_non_s, "recettes_v":recettes_v, 'budget':budget})

def depense_fonc_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6)
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=6)
	comptes_regle_par_autre = []
	for c in comptes:
		if c.regle_par != unite:
			comptes_regle_par_autre.append(c)	
	# pos 2 comptes 
	all_c2 = SCF_Pos_2.objects.all()
	c2_par_unite = []
	for c2 in all_c2:
		for cu in comptes_regle_par_unite:
			if c2.numero == cu.compte.ref.ref.ref.numero:
				c2_par_unite.append(c2)

	c2_par_autre = []
	for c2 in all_c2:
		for cu in comptes_regle_par_autre:
			if c2.numero == cu.compte.ref.ref.ref.numero:
				c2_par_autre.append(c2)
	
	c2_par_unite = list(dict.fromkeys(c2_par_unite))
	c2_par_autre = list(dict.fromkeys(c2_par_autre))
	
	# clacule les pos 2 saisier 
	



	#pos 3 comptes
	all_c3 = SCF_Pos_3.objects.all()
	c3_par_unite = []
	for c3 in all_c3:
		for cu in comptes_regle_par_unite:
			if c3.numero == cu.compte.ref.ref.numero:
				c3_par_unite.append(c3)

	c3_par_autre = []
	for c3 in all_c3:
		for cu in comptes_regle_par_autre:
			if c3.numero == cu.compte.ref.ref.numero:
				c3_par_autre.append(c3)
	
	c3_par_unite = list(dict.fromkeys(c3_par_unite))
	c3_par_autre = list(dict.fromkeys(c3_par_autre))

	#comptes_regle_par_autre = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite compte__chapitre__code_num=6)	
	
	depense_fonc_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6).count()
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=6).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()


	depense_fonc_s = depense_fonc_nbr==depense_fonc_done_nbr
	depense_fonc_non_s = depense_fonc_done_nbr == 0
	depense_fonc_v = depense_fonc_nbr==depense_fonc_valid_nbr

	return render(request,"reunion/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes, 'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																  "depense_fonc_s":depense_fonc_s, "depense_fonc_non_s":depense_fonc_non_s, "depense_fonc_v":depense_fonc_v, 'budget':budget,
																  "c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre})

def depense_exp_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7)
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=7)
	comptes_regle_par_autre = []
	for c in comptes:
		if c.regle_par != unite:
			comptes_regle_par_autre.append(c)	

	all_c2 = SCF_Pos_2.objects.all()
	c2_par_unite = []
	for c2 in all_c2:
		for cu in comptes_regle_par_unite:
			if c2.numero == cu.compte.ref.ref.ref.numero:
				c2_par_unite.append(c2)

	c2_par_autre = []
	for c2 in all_c2:
		for cu in comptes_regle_par_autre:
			if c2.numero == cu.compte.ref.ref.ref.numero:
				c2_par_autre.append(c2)
	
	c2_par_unite = list(dict.fromkeys(c2_par_unite))
	c2_par_autre = list(dict.fromkeys(c2_par_autre))

	# pos 3 comptes
	all_c3 = SCF_Pos_3.objects.all()
	c3_par_unite = []
	for c3 in all_c3:
		for cu in comptes_regle_par_unite:
			if c3.numero == cu.compte.ref.ref.numero:
				c3_par_unite.append(c3)

	c3_par_autre = []
	for c3 in all_c3:
		for cu in comptes_regle_par_autre:
			if c3.numero == cu.compte.ref.ref.numero:
				c3_par_autre.append(c3)
	
	c3_par_unite = list(dict.fromkeys(c3_par_unite))
	c3_par_autre = list(dict.fromkeys(c3_par_autre))	


	depense_exp_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7).count()
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", unite_compte__compte__chapitre__code_num=7).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_bdg="REUN", vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()

	depense_exp_s = depense_exp_nbr==depense_exp_done_nbr
	depense_exp_non_s = depense_exp_done_nbr == 0
	depense_exp_v = depense_exp_nbr==depense_exp_valid_nbr

	return render(request,"reunion/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes,  'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																	"depense_exp_s":depense_exp_s, "depense_exp_non_s":depense_exp_non_s, "depense_exp_v":depense_exp_v, 'budget':budget,
																	"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre})

# add montant to compte 
def add_montant_reunion(request, id):
	unite_compte = Unite_has_Compte.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comment_form = CommentaireForm(request.POST or None)
	montant_form = MontantCompteForm(request.POST or None)
	if request.method == "POST":
		if  montant_form.is_valid():
			montant_compte = montant_form.save(commit=False)
			montant_compte.unite_compte = unite_compte
			montant_compte.type_bdg = "REUN"
			montant_compte.annee_budgetaire = budget
			montant_compte.code = str(montant_compte.unite_compte.id) + montant_compte.annee_budgetaire.code + montant_compte.unite_compte.monnaie.code_alpha + montant_compte.unite_compte.regle_par.code_alpha
			if comment_form.is_valid():
				comment = comment_form.save(commit=False)
				comment.comment_type = "M"
				comment.user = request.user
				comment.save()
				montant_compte.commentaire_montant = comment
			
			if request.user.user_type==6:
				montant_compte.montant_cadre = montant_compte.montant
				montant_compte.vld_cadre = True
				montant_compte.validation = "CADRE"

			if request.user.user_type==5:
				montant_compte.montant_chef_dep = montant_compte.montant
				montant_compte.vld_chef_dep = True
				montant_compte.validation = "CHEFD"
			
			if request.user.user_type==4:
				montant_compte.montant_sous_dir = montant_compte.montant
				montant_compte.vld_sous_dir = True
				montant_compte.validation = "SOUSD"				
			
			montant_compte.save()
			messages.success(request, "compte added successfuly to unite." )
			# Redirecter vers chaque chapitre
			if unite_compte.compte.chapitre.code_num== 1:
				return redirect("/reunion/unite/offre/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 2:
				return redirect("/reunion/unite/traffic/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 3:
				return redirect("/reunion/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 4:
				return redirect("/reunion/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 5:
				return redirect("/reunion/unite/recettes/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 6:
				return redirect("/reunion/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 7:
				return redirect("/reunion/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
			else:
				return redirect("/reunion/unites")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="reunion/add_montant.html", context={"montant_form":montant_form, "comment_form":comment_form, "unite_compte":unite_compte, "budget":budget})

def update_montant_reunion(request, id): 
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]	
	form = UpdateMontantCompteForm(request.POST or None, instance = montant)
	if form.is_valid():
		form.save()
		messages.success(request, "Montant updated successfuly." )
		new_montant = get_object_or_404(Compte_has_Montant, id = id)
		if request.user.user_type==6:
			new_montant.montant_cadre = new_montant.montant
			new_montant.vld_cadre = True
			new_montant.save()
		if request.user.user_type==5:
			new_montant.montant_chef_dep = new_montant.montant
			new_montant.vld_chef_dep = True
			new_montant.validation = "CHEFD"
			new_montant.save()
		if request.user.user_type==4:
			new_montant.montant_sous_dir = new_montant.montant
			new_montant.vld_sous_dir = True
			new_montant.validation = "SOUSD"
			new_montant.save()
		
		# Redirecter vers chaque chapitre
		if unite_compte.compte.chapitre.code_num== 1:
			return redirect("/reunion/unite/offre/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 2:
			return redirect("/reunion/unite/traffic/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 3:
			return redirect("/reunion/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 4:
			return redirect("/reunion/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 5:
			return redirect("/reunion/unite/recettes/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 6:
			return redirect("/reunion/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 7:
			return redirect("/reunion/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
		else:
			return redirect("/reunion/unites")
	return render (request=request, template_name="reunion/update_montant.html", context={"form":form, "unite_compte":unite_compte, "montant":montant, "budget":budget})

def valid_montant_reunion(request, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte
	if request.user.user_type==6:
		new_montant.vld_cadre = True
		new_montant.save()
	if request.user.user_type==5:
		new_montant.vld_chef_dep = True
		new_montant.validation = "CHEFD"
		new_montant.save()
	if request.user.user_type==4:
		new_montant.vld_sous_dir = True
		new_montant.validation = "SOUSD"
		new_montant.save()

	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/reunion/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/reunion/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/reunion/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/reunion/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/reunion/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/reunion/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/reunion/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/reunion/unites")

def cancel_valid_montant_reunion(request, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte
	if request.user.user_type==6:
		new_montant.vld_cadre = False
		new_montant.save()
	if request.user.user_type==5:
		new_montant.vld_chef_dep = False
		new_montant.validation = "CHEFD"
		new_montant.save()
	if request.user.user_type==4:
		new_montant.vld_sous_dir = False
		new_montant.validation = "SOUSD"
		new_montant.save()
	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/reunion/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/reunion/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/reunion/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/reunion/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/reunion/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/reunion/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/reunion/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/reunion/unites")

def add_new_compte_reunion(request, id):
	unite = Unite.objects.get(id=id)
	form = AddCompteUniteForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			compte_unite = form.save(commit=False)
			compte_unite.unite = unite
			compte_unite.added_by = request.user
			compte_unite.code = compte_unite.unite.code_alpha + str(compte_unite.compte.numero) + compte_unite.regle_par.code_alpha + compte_unite.reseau_compte
			compte_unite.save()
			messages.success(request, "compte added successfuly." )
			return HttpResponseRedirect("/reunion/unite/"+ str(unite.id)+"")
			
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="reunion/add_new_compte.html", context={"form":form})

def delete_added_compte_reunion(request,id):
	form = Unite_has_Compte.objects.get(id=id)
	unite = form.unite
	compte = form.compte
	form.delete()
	# Redirecter vers chaque chapitre
	if compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/reunion/unite/offre/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/reunion/unite/traffic/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/reunion/unite/ca_emmission/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/reunion/unite/ca_transport/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/reunion/unite/recettes/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/reunion/unite/depense_fonc/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/reunion/unite/depense_exp/"+ str(unite.id)+"")
	else:
		return HttpResponseRedirect("/reunion/unites")	

# comments
def update_comment_reunion(request, id): 
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]
	comment = get_object_or_404(Commentaire, id = id)
	form = CommentaireForm(request.POST or None, instance = comment)
	if form.is_valid():
		form.save()
		messages.success(request, "Commentaire updated successfuly." )
		return redirect("/reunion/unites")

	return render (request=request, template_name="reunion/update_comment.html", context={"form":form, "comment":comment, "budget":budget})

def delete_comment_reunion(request, id):
    form = Commentaire.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/reunion/unites")

# consultation reunion budget 
def annees_bdg_reunion(request):
	budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	dep_unites = Unite.objects.filter(departement=request.user.departement)
	all_unites = Unite.objects.all()
	return render(request,"reunion/consultation/annees.html", {'budgets':budgets, 'unites':unites, 'dep_unites':dep_unites, 'all_unites':all_unites})


# méme view que proposition 
# add montant et modifier monatnt on le modifier 
# pour les url meme que proposition 



