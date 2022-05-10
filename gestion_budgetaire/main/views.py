from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.shortcuts import  render, redirect, get_object_or_404
from .forms import (NewUserForm, InterimForm, AnneeBdgForm, UpdateAnneeBdgForm,
					AddUniteForm,AddDepForm,AddPos1Form,AddPos2Form,AddPos3Form,AddPos6Form,AddPos7Form,CompteScfForm,
					AddMonnaieForm, AddTauxChngForm, AddChapitreForm, AddPaysForm, 
					AffectCadreForm, AddCompteUniteForm, MontantCompteForm,UpdateMontantCompteForm,CommentaireForm,MontantOnlyForm,
					UpdateMontantNotifForm,TypeDecoupeMontantForm, ActualisMontantNotifForm
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

@login_required(login_url='login')
def home(request):
	# count objects
	users_nbr = User.objects.all().count()
	unites_nbr = Unite.objects.all().count()
	comptes_nbr = SCF_Pos_7.objects.all().count()
	budgets_nbr = Annee_Budgetaire.objects.all().count()
	# get objects
	unites = Unite.objects.all().order_by('id')
	unites_chef = Unite.objects.filter(departement=request.user.departement)
	all_unites_cadre = Cadre_has_Unite.objects.filter(cadre=request.user)
	unites_cadre = []
	for u in all_unites_cadre:
		unites_cadre.append(u.unite)

	budgets = Annee_Budgetaire.objects.all().order_by('-annee')
	budgets_encours = Annee_Budgetaire.objects.filter(cloture=False).order_by('-annee')

	unite_rubs = {}
	for u in unites:
		uc = Unite_has_Compte.objects.filter(unite=u).count()
		unite_rubs[u.id] = uc

	#print("------------------") 
	#print(unite_rubs)

	# get last budget notif data ----------------------------------------------------------
	# Converter touts les sommes en DZD
	def sum_montants(montants):
		result = 0
		if len(montants) != 0:
			for m in montants:
				# DZD id = 12
				if m.unite_compte.monnaie.id == 12 or m.unite_compte.monnaie.id == 0:  
					result = result + m.montant	
				else:	
					tch_val = 1											
					tch = Taux_de_change.objects.filter(monnaie=m.unite_compte.monnaie, annee=m.annee_budgetaire.annee)
					if len(tch) != 0:
						tch_val = tch[0].value
					conv_montant = m.montant * tch_val
					result = result + conv_montant
		return result

	budget_notif = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	if len(budget_notif) != 0:
		last_budget = budget_notif[0]
		# offre:   PAX: 8000100 -- BCB: 8000110 --  FRET: 8000120 -- POSTE: 8000130 
		# trafic:  PAX: 8000200 -- BCB: 8000210 --  FRET: 8000220 -- POSTE: 8000230 

		montants_off_pax = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__numero=8000100, type_maj="N") 
		montants_off_bcb = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__numero=8000110, type_maj="N")
		montants_off_fret = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__numero=8000120, type_maj="N")
		montants_off_poste = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__numero=8000130, type_maj="N") 

		montants_trf_pax = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__numero=8000200, type_maj="N") 
		montants_trf_bcb = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__numero=8000210, type_maj="N")
		montants_trf_fret = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__numero=8000220, type_maj="N")
		montants_trf_poste = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__numero=8000230, type_maj="N") 

		montants_ca_emmession = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__chapitre__code_num=3, type_maj="N")
		montants_recettes_transport = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__chapitre__code_num=4, type_maj="N")
		montants_autre_recettes = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__chapitre__code_num=5, type_maj="N")		
		montants_dep_fonc = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__chapitre__code_num=6, type_maj="N")
		montants_dep_exp = Compte_has_Montant.objects.filter(annee_budgetaire=last_budget, unite_compte__compte__chapitre__code_num=7, type_maj="N")
		
		# les tautaux pour chaue chapitre
		total_off_pax = int(sum_montants(montants_off_pax))
		total_off_bcb = int(sum_montants(montants_off_bcb))
		total_off_fret = int(sum_montants(montants_off_fret))
		total_off_poste = int(sum_montants(montants_off_poste))

		total_trf_pax = int(sum_montants(montants_trf_pax))
		total_trf_bcb = int(sum_montants(montants_trf_bcb))
		total_trf_fret = int(sum_montants(montants_trf_fret))
		total_trf_poste = int(sum_montants(montants_trf_poste))


		total_emmission = int(sum_montants(montants_ca_emmession))
		total_recettes_transport = int(sum_montants(montants_recettes_transport))
		total_autre_recettes = int(sum_montants(montants_autre_recettes))
		total_dep_fonc = int(sum_montants(montants_dep_fonc))
		total_dep_exp = int(sum_montants(montants_dep_exp))

		#print("Query : ------------------------------------------")
		#print("Emission: ",total_emmission) 
		#print("Reccetes trans: ",total_recettes_transport)
		#print("Autre Recettes: ",total_autre_recettes)
		#print("Depens fonc: ",total_dep_fonc)
		#print("Depens Exp: ",total_dep_exp)
		#print(montants_ca_emmession.query)
	else: 
		last_budget = "NULL"

	# etat d'avancemenet 
	def get_unite_status(unite, budget):
		unite_state = {}
		result = {}
		result["pr"] = 0
		result["state"] = "-"

		comptes = Unite_has_Compte.objects.filter(unite=unite)
		montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite)
		montants_vld_sdir = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite, vld_sous_dir=True, type_maj="N")
		montants_vld_chef = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite, vld_chef_dep=True, type_maj="N")
		montants_valid = []
		for m in montants:
			if m.vld_sous_dir == True or vld_chef_dep == True:
				montants_valid.append(m)


		pr = 0
		if len(comptes) == 0:
			pr = 0
		else:
			if len(montants) == 0:
				pr = 0
			else:
				pr = int(math.modf((comptes.count() / montants.count())*100)[1])

		# state cadre
		if len(montants) == 0:
			state_cadre = "Non saisie"
		elif len(comptes) == len(montants) and len(comptes) != len(montants_valid) :
			state_cadre = "Terminé"
		elif len(comptes) == len(montants) and len(comptes) == len(montants_valid):
			state_cadre = "Validé"
		else:
			state_cadre = "En cours"
		
		# state chef
		if len(montants) == 0:
			state_chef = "Non saisie"
		elif len(comptes) == len(montants) and len(comptes) != len(montants_valid) :
			state_chef = "Instance"
		elif len(comptes) == len(montants) and len(comptes) == len(montants_valid) and len(comptes) != len(montants_vld_sdir) :
			state_chef = "Terminé" 
		elif len(comptes) == len(montants) and len(comptes) == len(montants_vld_sdir):
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		
		# state sdir 
		if len(montants) == 0:
			state_sdir = "Non saisie"
		elif len(comptes) == len(montants) and len(comptes) != len(montants_vld_sdir) :
			state_sdir = "Instance"
		elif len(comptes) == len(montants) and len(comptes) == len(montants_vld_sdir):
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"

		unite_state["cadre"] = state_cadre
		unite_state["chef"] = state_chef
		unite_state["sdir"] = state_sdir

		result["pr"] = pr
		result["state"] = unite_state


		return result

	b_status = {}
	for budget in budgets_encours:
		u_status = {}
		for u in unites:
			u_status[u.id] = get_unite_status(u, budget)
		
		b_status[budget.id] = u_status
		
	#print("status --------------------")
	#print(b_status)

	return render(request, "home.html", {'users_nbr':users_nbr, 'unites_nbr':unites_nbr, 'comptes_nbr':comptes_nbr, 'budgets_nbr':budgets_nbr,
										  'unites':unites, 'budgets':budgets, 'unite_rubs':unite_rubs, 'budgets_encours':budgets_encours,
										  'unites_chef':unites_chef, 'unites_cadre':unites_cadre,
										  'total_emmission':total_emmission, 'total_recettes_transport':total_recettes_transport, 'total_autre_recettes':total_autre_recettes,
										   'total_dep_fonc':total_dep_fonc, 'total_dep_exp': total_dep_exp, 'last_budget':last_budget,
										   'total_off_pax':total_off_pax, 'total_off_bcb':total_off_bcb,'total_off_fret':total_off_fret,'total_off_poste':total_off_poste,
										   'total_trf_pax':total_trf_pax, 'total_trf_bcb':total_trf_bcb,'total_trf_fret':total_trf_fret,'total_trf_poste':total_trf_poste, })

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

@login_required(login_url='login')
def chef_dep_list(request):
	chefs = User.objects.filter(user_type=5)
	chefs_count = User.objects.filter(user_type=5).count()
	return render(request, "registration/chef_dep_list.html" , {'chefs' : chefs, 'chefs_count':chefs_count})

@login_required(login_url='login')
def sous_dir_list(request):
	sous_dir = User.objects.filter(user_type=4)
	sous_dir_count = User.objects.filter(user_type=4).count()
	return render(request, "registration/sous_dir_list.html" , {'sous_dir' : sous_dir, 'sous_dir_count':sous_dir_count})

@login_required(login_url='login')
def dir_list(request):
	dir = User.objects.filter(user_type=3)
	dir_count = User.objects.filter(user_type=3).count()
	return render(request, "registration/dir_list.html" , {'dir':dir, 'dir_count':dir_count})

@login_required(login_url='login')
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
	unite = Unite.objects.all().order_by('id')
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
	monnaie = Monnaie.objects.all().order_by('id')
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
	unites = Unite.objects.all().order_by('id')
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
	all_unites = Unite.objects.all()

	# montant total consolidé of unite --------
	total_unite_dic = {}
	bdg_total = 0
	state_cadre_dic = {}
	state_chef_dic = {}
	pr_dic = {}
	for u in all_unites:
		# calculer le montant
		total = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire=budget).aggregate(Sum('montant'))
		total_unite_dic[u.id] = total['montant__sum']
		if total['montant__sum'] != None:
			bdg_total = bdg_total + total['montant__sum']

		# get state of unite (Terminé , En cours, ...)
		comptes_nbr = Unite_has_Compte.objects.filter(unite=u).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget, vld_chef_dep=True).count()
		
		# needed status comptes_valid
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr

		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic[u.id]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False :
			state_chef = "Instance"
		elif comptes_v and comptes_s :
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic[u.id]= state_chef

		# porcentage de saiser pour l unite
		if comptes_nbr == 0:
			pr = 0
		else :
			pr = int(math.modf((comptes_done_nbr / comptes_nbr)*100)[1])						
		pr_dic[u.id] = pr
	#------------------------------------------

	return render(request,"proposition/unites.html", {'unites':unites, 'dep_unites':dep_unites, 'budget':budget, 'total_unite_dic':total_unite_dic, 'bdg_total':bdg_total,
														'state_cadre_dic':state_cadre_dic, 'state_chef_dic':state_chef_dic, 'pr_dic':pr_dic })

def unite_detail(request, id):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id)
	comptes_nbr = Unite_has_Compte.objects.filter(unite=unite).count()
	comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget).count()
	comptes_vld_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True).count()	
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
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=1).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=4).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par chef dep
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()
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

	chapitre = Chapitre.objects.get(code_num=1)

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
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=1).count()
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	
	c_s = offre_nbr==offre_done_nbr
	c_non_s = offre_done_nbr == 0
	c_v = offre_nbr==offre_valid_nbr

	return render(request,"proposition/offre_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict,
															"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre })

def traffic_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=2)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=2)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	traffic_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=2).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=2).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()

	c_s = traffic_nbr==traffic_done_nbr
	c_non_s = traffic_done_nbr == 0
	c_v = traffic_nbr==traffic_valid_nbr

	return render(request,"proposition/traffic_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict,
																"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre  })

def ca_emmission_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=3)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=3)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	ca_emmission_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=3).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=3).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	
	c_s = ca_emmission_nbr==ca_emmission_done_nbr
	c_non_s = ca_emmission_done_nbr == 0
	c_v = ca_emmission_nbr==ca_emmission_valid_nbr

	return render(request,"proposition/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict,
																	"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre  })

def ca_transport_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=4)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=4).order_by('-reseau_compte')
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	ca_transport_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=4).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=4).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()

	c_s = ca_transport_nbr==ca_transport_done_nbr
	c_non_s = ca_transport_done_nbr == 0
	c_v = ca_transport_nbr==ca_transport_valid_nbr

	return render(request,"proposition/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict, 
																	"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre })

def recettes_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=5)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=5)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	recettes_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=5).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=5).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()

	c_s = recettes_nbr==recettes_done_nbr
	c_non_s = recettes_done_nbr == 0
	c_v = recettes_nbr==recettes_valid_nbr

	return render(request,"proposition/recettes_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict, 
																"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre })

def depense_fonc_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=6)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
		
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
	
	# clacule les pos 2 saisier state 
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		
		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False:
			state_chef = "Instance"
		elif comptes_v and comptes_s:
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

	# comptes par unité -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, compte__ref__ref__ref=c2).count()
		comptes_nbr = comptes_all_nbr - comptes_unite_nbr

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		comptes_done_nbr = done_all_nbr - done_par_unite_nbr

		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		
		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False:
			state_chef = "Instance"
		elif comptes_v and comptes_s:
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef
	# ------------------------------------



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
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=6).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()


	c_s = depense_fonc_nbr==depense_fonc_done_nbr
	c_non_s = depense_fonc_done_nbr == 0
	c_v = depense_fonc_nbr==depense_fonc_valid_nbr

	return render(request,"proposition/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes, 'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																  "c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre, 'budget':budget,
																  "c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																  'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																  'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre })

def depense_exp_comptes(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=7)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
		
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

	# clacule les pos 2 saisier state 
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		
		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False:
			state_chef = "Instance"
		elif comptes_v and comptes_s:
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

	# comptes par unité -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, compte__ref__ref__ref=c2).count()
		comptes_nbr = comptes_all_nbr - comptes_unite_nbr

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		comptes_done_nbr = done_all_nbr - done_par_unite_nbr

		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		
		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False:
			state_chef = "Instance"
		elif comptes_v and comptes_s:
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef
	# ------------------------------------

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
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=7).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()

	c_s = depense_exp_nbr==depense_exp_done_nbr
	c_non_s = depense_exp_done_nbr == 0
	c_v = depense_exp_nbr==depense_exp_valid_nbr

	return render(request,"proposition/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes,  'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																	"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre, 'budget':budget,
																	"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																	'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																	'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre})

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
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

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
	return render (request=request, template_name="proposition/add_new_compte.html", context={"form":form, 'unite':unite, 'budget':budget})

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

#valider tous 
def valid_tous(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_chef_dep = True
			m.validation = "CHEFD"
			m.save()
		elif request.user.user_type == 4:
			m.vld_sous_dir = True
			m.validation = "SOUSD"
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/proposition/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/proposition/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/proposition/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/proposition/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/proposition/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/proposition/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/proposition/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/proposition/unites")

def cancel_valid_tous(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_chef_dep = False
			m.save()
		elif request.user.user_type == 4:
			m.vld_sous_dir = False
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/proposition/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/proposition/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/proposition/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/proposition/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/proposition/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/proposition/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/proposition/unite/depense_exp/"+ str(id_unite)+"")
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

# -------------------------------------- Fin Proposition budget --------------------------------------------------------



# Réunion --------------------------------------------------------------------------------------------------------------

# affichage des unites et leur comptes par chapitre

def unites_reunion(request):
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]
	dep_unites = Unite.objects.filter(departement=request.user.departement)
	all_unites = Unite.objects.all()

	# montant total consolidé of unite --------
	total_unite_dic = {}
	bdg_total = 0
	state_cadre_dic = {}
	state_chef_dic = {}
	state_sdir_dic = {}
	pr_dic = {}
	for u in all_unites:
		# calculer le montant
		total = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire=budget).aggregate(Sum('montant'))
		total_unite_dic[u.id] = total['montant__sum']
		if total['montant__sum'] != None:
			bdg_total = bdg_total + total['montant__sum']

		# get state of unite (Terminé , En cours, ...)
		comptes_nbr = Unite_has_Compte.objects.filter(unite=u).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget, vld_chef_dep=True).count()
		comptes_v_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget, vld_sous_dir=True).count()
		# valid par tous staus
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1
		if i == 0:
			comptes_valid =  False
		else: 
			comptes_valid =  comptes_done_nbr == i	
		
		# needed status comptes_valid
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid	

		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic[u.id]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic[u.id]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic[u.id]= state_sdir	

		# porcentage de saiser pour l unite
		if comptes_nbr == 0:
			pr = 0
		else :
			pr = int(math.modf((comptes_done_nbr / comptes_nbr)*100)[1])						
		pr_dic[u.id] = pr
	#------------------------------------------


	return render(request,"reunion/unites.html", {'unites':unites, 'dep_unites':dep_unites, 'all_unites':all_unites, 'budget':budget, 'total_unite_dic':total_unite_dic, 'bdg_total':bdg_total,
													'state_cadre_dic':state_cadre_dic, 'state_chef_dic':state_chef_dic, 'state_sdir_dic':state_sdir_dic, 'pr_dic':pr_dic})

def unite_detail_reunion(request, id):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]
	unite = Unite.objects.get(id=id)
	comptes_nbr = Unite_has_Compte.objects.filter(unite=unite).count()
	comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget,).count()
	comptes_vld_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True).count()	
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
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=1).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=4).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par chef dep
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par sous dir
	offre_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=7).count()
	
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

	#Check if chapitre is validé par sous directeur
	offre_v_sdir = offre_nbr==offre_valid_sdir_nbr
	traffic_v_sdir = traffic_nbr==traffic_valid_sdir_nbr
	ca_emmission_v_sdir = ca_emmission_nbr==ca_emmission_valid_sdir_nbr
	ca_transport_v_sdir = ca_transport_nbr==ca_transport_valid_sdir_nbr
	recettes_v_sdir = recettes_nbr==recettes_valid_sdir_nbr
	depense_fonc_v_sdir = depense_fonc_nbr==depense_fonc_valid_sdir_nbr
	depense_exp_v_sdir = depense_exp_nbr==depense_exp_valid_sdir_nbr

	#Check if chapitre is not validé par chef dep ( = compte validé)
	offre_non_v = offre_valid_nbr == 0
	traffic_non_v = traffic_valid_nbr == 0
	ca_emmission_non_v = ca_emmission_valid_nbr == 0
	ca_transport_non_v = ca_transport_valid_nbr == 0
	recettes_non_v = recettes_valid_nbr == 0
	depense_fonc_non_v = depense_fonc_valid_nbr == 0
	depense_exp_non_v = depense_exp_valid_nbr == 0

	#Check if chapitre is not validé par sous directeur( = compte validé)
	offre_non_v_sdir = offre_valid_sdir_nbr == 0
	traffic_non_v_sdir = traffic_valid_sdir_nbr == 0
	ca_emmission_non_v_sdir = ca_emmission_valid_sdir_nbr == 0
	ca_transport_non_v_sdir = ca_transport_valid_sdir_nbr == 0
	recettes_non_v_sdir = recettes_valid_sdir_nbr == 0
	depense_fonc_non_v_sdir = depense_fonc_valid_sdir_nbr == 0
	depense_exp_non_v_sdir = depense_exp_valid_sdir_nbr == 0

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	offre_valid = is_valid(1)
	traffic_valid = is_valid(2)
	ca_emmission_valid = is_valid(3)
	ca_transport_valid = is_valid(4)
	recettes_valid = is_valid(5)
	depense_fonc_valid = is_valid(6)
	depense_exp_valid = is_valid(7)

	return render(request,"reunion/unite_detail.html", {'unite':unite, 'comptes_nbr':comptes_nbr, 'comptes_done_nbr':comptes_done_nbr, 'pr_cdr':pr_cdr, 'pr_vcd':pr_vcd, 'budget':budget, 
															'offre_s':offre_s, 'traffic_s':traffic_s, 'ca_emmission_s':ca_emmission_s, 'ca_transport_s':ca_transport_s,
															'recettes_s':recettes_s, 'depense_fonc_s':depense_fonc_s, 'depense_exp_s':depense_exp_s,
															'offre_v':offre_v, 'traffic_v':traffic_v, 'ca_emmission_v':ca_emmission_v, 'ca_transport_v':ca_transport_v,
															'recettes_v':recettes_v, 'depense_fonc_v':depense_fonc_v, 'depense_exp_v':depense_exp_v,
															'offre_non_s':offre_non_s, 'traffic_non_s':traffic_non_s, 'ca_emmission_non_s':ca_emmission_non_s, 'ca_transport_non_s':ca_transport_non_s,
															'recettes_non_s':recettes_non_s, 'depense_fonc_non_s':depense_fonc_non_s, 'depense_exp_non_s':depense_exp_non_s,
															'offre_non_v':offre_non_v, 'traffic_non_v':traffic_non_v, 'ca_emmission_non_v':ca_emmission_non_v, 'ca_transport_non_v':ca_transport_non_v,
															'recettes_non_v':recettes_non_v, 'depense_fonc_non_v':depense_fonc_non_v, 'depense_exp_non_v':depense_exp_non_v,

															'offre_non_v_sdir':offre_non_v_sdir, 'traffic_non_v_sdir':traffic_non_v_sdir, 'ca_emmission_non_v_sdir':ca_emmission_non_v_sdir, 'ca_transport_non_v_sdir':ca_transport_non_v_sdir,
															'recettes_non_v_sdir':recettes_non_v_sdir, 'depense_fonc_non_v_sdir':depense_fonc_non_v_sdir, 'depense_exp_non_v_sdir':depense_exp_non_v_sdir,
															'offre_v_sdir':offre_v_sdir, 'traffic_v_sdir':traffic_v_sdir, 'ca_emmission_v_sdir':ca_emmission_v_sdir, 'ca_transport_v_sdir':ca_transport_v_sdir,
															'recettes_v_sdir':recettes_v_sdir, 'depense_fonc_v_sdir':depense_fonc_v_sdir, 'depense_exp_v_sdir':depense_exp_v_sdir,

															'offre_valid':offre_valid, 'traffic_valid':traffic_valid, 'ca_emmission_valid':ca_emmission_valid, 'ca_transport_valid':ca_transport_valid, 'recettes_valid':recettes_valid,
															'depense_fonc_valid':depense_fonc_valid, 'depense_exp_valid':depense_exp_valid
															})

def offre_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	# chapitre (offre)
	chapitre = Chapitre.objects.get(code_num=1)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=1)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]
	#print(cm_dict)

	offre_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=1).count()
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=1).count()
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	offre_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=1).count()
	
	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	offre_valid = is_valid(1)

	offre_s = offre_nbr==offre_done_nbr
	offre_non_s = offre_done_nbr == 0
	offre_v = offre_nbr==offre_valid_nbr
	offre_v_sdir = offre_nbr==offre_valid_sdir_nbr

	return render(request,"reunion/offre_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":offre_s, "c_non_s":offre_non_s, "c_v":offre_v, 'c_v_sdir':offre_v_sdir, 'c_valid':offre_valid , 'cm_dict':cm_dict,
														 'budget':budget, 'chapitre':chapitre})

def traffic_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=2)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=2)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	traffic_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=2).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=2).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()
	traffic_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=2).count()

	traffic_s = traffic_nbr==traffic_done_nbr
	traffic_non_s = traffic_done_nbr == 0
	traffic_v = traffic_nbr==traffic_valid_nbr
	traffic_v_sdir = traffic_nbr==traffic_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	traffic_valid = is_valid(2)	


	return render(request,"reunion/traffic_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":traffic_s, "c_non_s":traffic_non_s, "c_v":traffic_v, 'budget':budget, 'cm_dict':cm_dict,
															'c_valid':traffic_valid, 'c_v_sdir':traffic_v_sdir, 'chapitre':chapitre })

def ca_emmission_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=3)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=3)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	ca_emmission_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=3).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=3).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_emmission_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=3).count()
	
	ca_emmission_s = ca_emmission_nbr==ca_emmission_done_nbr
	ca_emmission_non_s = ca_emmission_done_nbr == 0
	ca_emmission_v = ca_emmission_nbr==ca_emmission_valid_nbr
	ca_emmission_v_sdir = ca_emmission_nbr==ca_emmission_valid_sdir_nbr


	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	ca_emmission_valid = is_valid(3)	

	return render(request,"reunion/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":ca_emmission_s, "c_non_s":ca_emmission_non_s, "c_v":ca_emmission_v, 'budget':budget, 'cm_dict':cm_dict,
																'c_valid':ca_emmission_valid, 'c_v_sdir':ca_emmission_v_sdir, 'chapitre':chapitre })

def ca_transport_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=4)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=4).order_by('-reseau_compte')
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	ca_transport_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=4).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=4).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()
	ca_transport_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=4).count()

	ca_transport_s = ca_transport_nbr==ca_transport_done_nbr
	ca_transport_non_s = ca_transport_done_nbr == 0
	ca_transport_v = ca_transport_nbr==ca_transport_valid_nbr
	ca_transport_v_sdir = ca_transport_nbr==ca_transport_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	ca_transport_valid = is_valid(4)	

	return render(request,"reunion/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":ca_transport_s, "c_non_s":ca_transport_non_s, "c_v":ca_transport_v, 'budget':budget, 'cm_dict':cm_dict,
																'c_valid':ca_transport_valid, 'c_v_sdir':ca_transport_v_sdir, 'chapitre':chapitre })

def recettes_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=5)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=5)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	recettes_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=5).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=5).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()
	recettes_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=5).count()

	recettes_s = recettes_nbr==recettes_done_nbr
	recettes_non_s = recettes_done_nbr == 0
	recettes_v = recettes_nbr==recettes_valid_nbr
	recettes_v_sdir = recettes_nbr==recettes_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	recettes_valid = is_valid(5)	

	return render(request,"reunion/recettes_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":recettes_s, "c_non_s":recettes_non_s, "c_v":recettes_v, 'budget':budget, 'cm_dict':cm_dict,
															'c_valid':recettes_valid, 'c_v_sdir':recettes_v_sdir, 'chapitre':chapitre })

def depense_fonc_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=6)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=6)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)
	#for c in comptes:
	#	if c.regle_par != unite:
	#		comptes_regle_par_autre.append(c)	
	
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
	
	# clacule les pos 2 saisier state -----------------------
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	state_sdir_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False and comptes_valid:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_unite[c2.numero]= state_sdir		

	# comptes par autre -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	state_sdir_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2)
		comptes_all = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, compte__ref__ref__ref=c2)
		comptes_autre = comptes_all.difference(comptes_unite)  

		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, compte__ref__ref__ref=c2).count()
		#comptes_nbr = comptes_all_nbr - comptes_unite_nbr
		comptes_nbr = comptes_all.difference(comptes_unite).count()


		done_par_unite = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6)
		done_all = Compte_has_Montant.objects.filter(unite_compte__unite=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6)
		comptes_done = done_all.difference(done_par_unite)
		

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		#comptes_done_nbr = done_all_nbr - done_par_unite_nbr
		comptes_done_nbr = comptes_done.count()


		#check chef dep validation 
		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		#check sous dir validation
		comptes_vsdir_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_vsdir_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_sdir_nbr = comptes_vsdir_all_nbr - comptes_vsdir_unite_nbr
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False and comptes_valid:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_autre[c2.numero]= state_sdir	

	# --------------------------------------------------------

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
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=6).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_fonc_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=6).count()


	depense_fonc_s = depense_fonc_nbr==depense_fonc_done_nbr
	depense_fonc_non_s = depense_fonc_done_nbr == 0
	depense_fonc_v = depense_fonc_nbr==depense_fonc_valid_nbr
	depense_fonc_v_sdir = depense_fonc_nbr==depense_fonc_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	depense_fonc_valid = is_valid(6)	

	return render(request,"reunion/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes, 'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																"c_s":depense_fonc_s, "c_non_s":depense_fonc_non_s, "c_v":depense_fonc_v, 'budget':budget,
																"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																"c_valid":depense_fonc_valid, 'c_v_sdir':depense_fonc_v_sdir, 'chapitre':chapitre,
																'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre,
																'state_sdir_dic_par_unite':state_sdir_dic_par_unite, 'state_sdir_dic_par_autre':state_sdir_dic_par_autre })

def depense_exp_comptes_reunion(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=7)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=7)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)

	#for c in comptes:
	#	if c.regle_par != unite:
	#		comptes_regle_par_autre.append(c)	

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

	# clacule les pos 2 saisier state--------------------- 
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	state_sdir_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_unite[c2.numero]= state_sdir		

	# comptes par autre -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	state_sdir_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2)
		comptes_all = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, compte__ref__ref__ref=c2)
		comptes_autre = comptes_all.difference(comptes_unite)  

		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, compte__ref__ref__ref=c2).count()
		#comptes_nbr = comptes_all_nbr - comptes_unite_nbr
		comptes_nbr = comptes_all.difference(comptes_unite).count()


		done_par_unite = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7)
		done_all = Compte_has_Montant.objects.filter(unite_compte__unite=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7)
		comptes_done = done_all.difference(done_par_unite)
		

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		#comptes_done_nbr = done_all_nbr - done_par_unite_nbr
		comptes_done_nbr = comptes_done.count()


		#check chef dep validation 
		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		#check sous dir validation
		comptes_vsdir_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_vsdir_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_sdir_nbr = comptes_vsdir_all_nbr - comptes_vsdir_unite_nbr
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False and comptes_valid:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_autre[c2.numero]= state_sdir	

	# --------------------------------------------------------

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
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=7).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()
	depense_exp_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=7).count()

	depense_exp_s = depense_exp_nbr==depense_exp_done_nbr
	depense_exp_non_s = depense_exp_done_nbr == 0
	depense_exp_v = depense_exp_nbr==depense_exp_valid_nbr
	depense_exp_v_sdir = depense_exp_nbr==depense_exp_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	depense_exp_valid = is_valid(7)	

	return render(request,"reunion/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes,  'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																	"c_s":depense_exp_s, "c_non_s":depense_exp_non_s, "c_v":depense_exp_v, 'budget':budget,
																	"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																	"c_valid":depense_exp_valid, 'c_v_sdir':depense_exp_v_sdir, 'chapitre':chapitre,
																	'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																	'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre,
																	'state_sdir_dic_par_unite':state_sdir_dic_par_unite, 'state_sdir_dic_par_autre':state_sdir_dic_par_autre })

# add montant to compte 
def add_montant_reunion(request, id):
	unite_compte = Unite_has_Compte.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	# Les Anneés  --------------------------------------------------------------------------
	annee_next = budget.annee    # N+1  (2023)
	annee_n = annee_next - 1     # N    (2022)  
	annee_n_1 = annee_next - 2   # N-1  (2021)
	annee_n_2 = annee_next - 3   # N-2  (2020)
	annee_n_3 = annee_next - 4   # N-3  (2019)

	# Réalisation n-1, n-2, n-3
	rls_n_1 = "-"
	rls_n_2 = "-"
	rls_n_3 = "-"
	ms_n_1 = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n_1, annee_budgetaire__type_bdg = "RELS" ).order_by('-edition')
	ms_n_2 = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n_2, annee_budgetaire__type_bdg = "RELS" ).order_by('-edition')
	ms_n_3 = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n_3, annee_budgetaire__type_bdg = "RELS" ).order_by('-edition')
	if len(ms_n_1) != 0:
		rls_n_1 = ms_n_1[0].montant
	else:
		rls_n_1 = "-"

	if len(ms_n_2) != 0:
		rls_n_2 = ms_n_2[0].montant
	else:
		rls_n_2 = "-"

	if len(ms_n_3) != 0:
		rls_n_3 = ms_n_3[0].montant
	else:
		rls_n_3 = "-"

	# annee n 
	notif_n = "-"
	notif_ms_n = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n, annee_budgetaire__type_bdg = "NOTIF" ).order_by('-edition')
	if len(notif_ms_n) != 0:
		notif_n = notif_ms_n[0].montant
	else:
		notif_n = "-"
	
	control_n = 0 # control cummulé année n
	mois_courant = "Jnavier" # mois control budgétaire
	control_ms_n = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n, annee_budgetaire__type_bdg = "CTRL" ).order_by('-edition')
	if len(control_ms_n) == 0:
		control_n = "-" 
		mois_courant = "-"
	else:
		m_control = control_ms_n[0]
		if m_control.janvier != None:
			control_n = control_n + m_control.janvier
			mois_courant = "Janvier"
		if m_control.fevrier != None:
			control_n = control_n + m_control.fevrier
			mois_courant = "Février"
		if m_control.mars != None:
			control_n = control_n + m_control.mars
			mois_courant = "Mars"
		if m_control.avril != None:
			control_n = control_n + m_control.avril
			mois_courant = "Avril"
		if m_control.mai != None:
			control_n = control_n + m_control.mai
			mois_courant = "Mai"
		if m_control.juin != None:
			control_n = control_n + m_control.juin
			mois_courant = "Juin"
		if m_control.juillet != None:
			control_n = control_n + m_control.juillet
			mois_courant = "Juillet"
		if m_control.aout != None:
			control_n = control_n + m_control.aout
			mois_courant = "Août"
		if m_control.septemre != None:
			control_n = control_n + m_control.septemre
			mois_courant = "Septembre"
		if m_control.octobre != None:
			control_n = control_n + m_control.octobre
			mois_courant = "Octobre"
		if m_control.novembre != None:
			control_n = control_n + m_control.novembre
			mois_courant = "Novembre"
		if m_control.decembre != None:
			control_n = control_n + m_control.decembre
			mois_courant = "Decembre"

	# Proposition (meme annee N+1) Cloture et Proposition 
	propos_clotur = "-"
	propos_prevs = "-"
	propos_ms_n = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_next, annee_budgetaire__type_bdg = "PROPOS" ).order_by('-edition')
	if len(propos_ms_n) != 0:
		propos_clotur = propos_ms_n[0].montant_cloture
		propos_prevs = propos_ms_n[0].montant
	else: 
		propos_clotur = "-"
		propos_prevs = "-"

	# ---------------------------------------------------------------------------------------------------

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
			messages.success(request, "compte saisié successfuly." )
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
	return render (request=request, template_name="reunion/add_montant.html", context={"montant_form":montant_form, "comment_form":comment_form, "unite_compte":unite_compte, "budget":budget,
																						"rls_n_1":rls_n_1, "rls_n_2":rls_n_2, "rls_n_3":rls_n_3, "notif_n":notif_n, "control_n":control_n, 
																						"mois_courant":mois_courant, "propos_clotur":propos_clotur, "propos_prevs":propos_prevs,
																						"annee_n_1":annee_n_1, "annee_n_2":annee_n_2, "annee_n_3":annee_n_3, "annee_n":annee_n, })

def update_montant_reunion(request, id): 
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]	

	# Les Anneés  --------------------------------------------------------------------------
	annee_next = budget.annee    # N+1  (2023)
	annee_n = annee_next - 1     # N    (2022)  
	annee_n_1 = annee_next - 2   # N-1  (2021)
	annee_n_2 = annee_next - 3   # N-2  (2020)
	annee_n_3 = annee_next - 4   # N-3  (2019)

	# Réalisation n-1, n-2, n-3
	rls_n_1 = "-"
	rls_n_2 = "-"
	rls_n_3 = "-"
	ms_n_1 = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n_1, annee_budgetaire__type_bdg = "RELS" ).order_by('-edition')
	ms_n_2 = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n_2, annee_budgetaire__type_bdg = "RELS" ).order_by('-edition')
	ms_n_3 = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n_3, annee_budgetaire__type_bdg = "RELS" ).order_by('-edition')
	if len(ms_n_1) != 0:
		rls_n_1 = ms_n_1[0].montant
	else:
		rls_n_1 = "-"

	if len(ms_n_2) != 0:
		rls_n_2 = ms_n_2[0].montant
	else:
		rls_n_2 = "-"

	if len(ms_n_3) != 0:
		rls_n_3 = ms_n_3[0].montant
	else:
		rls_n_3 = "-"

	# annee n 
	notif_n = "-"
	notif_ms_n = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n, annee_budgetaire__type_bdg = "NOTIF" ).order_by('-edition')
	if len(notif_ms_n) != 0:
		notif_n = notif_ms_n[0].montant
	else:
		notif_n = "-"
	
	control_n = 0 # control cummulé année n
	mois_courant = "Jnavier" # mois control budgétaire
	control_ms_n = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_n, annee_budgetaire__type_bdg = "CTRL" ).order_by('-edition')
	if len(control_ms_n) == 0:
		control_n = "-" 
		mois_courant = "-"
	else:
		m_control = control_ms_n[0]
		if m_control.janvier != None:
			control_n = control_n + m_control.janvier
			mois_courant = "Janvier"
		if m_control.fevrier != None:
			control_n = control_n + m_control.fevrier
			mois_courant = "Février"
		if m_control.mars != None:
			control_n = control_n + m_control.mars
			mois_courant = "Mars"
		if m_control.avril != None:
			control_n = control_n + m_control.avril
			mois_courant = "Avril"
		if m_control.mai != None:
			control_n = control_n + m_control.mai
			mois_courant = "Mai"
		if m_control.juin != None:
			control_n = control_n + m_control.juin
			mois_courant = "Juin"
		if m_control.juillet != None:
			control_n = control_n + m_control.juillet
			mois_courant = "Juillet"
		if m_control.aout != None:
			control_n = control_n + m_control.aout
			mois_courant = "Août"
		if m_control.septemre != None:
			control_n = control_n + m_control.septemre
			mois_courant = "Septembre"
		if m_control.octobre != None:
			control_n = control_n + m_control.octobre
			mois_courant = "Octobre"
		if m_control.novembre != None:
			control_n = control_n + m_control.novembre
			mois_courant = "Novembre"
		if m_control.decembre != None:
			control_n = control_n + m_control.decembre
			mois_courant = "Decembre"

	# Proposition (meme annee N+1) Cloture et Proposition 
	propos_clotur = "-"
	propos_prevs = "-"
	propos_ms_n = Compte_has_Montant.objects.filter( unite_compte=unite_compte, annee_budgetaire__annee = annee_next, annee_budgetaire__type_bdg = "PROPOS" ).order_by('-edition')
	if len(propos_ms_n) != 0:
		propos_clotur = propos_ms_n[0].montant_cloture
		propos_prevs = propos_ms_n[0].montant
	else: 
		propos_clotur = "-"
		propos_prevs = "-"

	# ---------------------------------------------------------------------------------------------------



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
	return render (request=request, template_name="reunion/update_montant.html", context={"form":form, "unite_compte":unite_compte, "montant":montant, "budget":budget, 
																							"rls_n_1":rls_n_1, "rls_n_2":rls_n_2, "rls_n_3":rls_n_3, "notif_n":notif_n, "control_n":control_n, 
																							"mois_courant":mois_courant, "propos_clotur":propos_clotur, "propos_prevs":propos_prevs,
																							"annee_n_1":annee_n_1, "annee_n_2":annee_n_2, "annee_n_3":annee_n_3, "annee_n":annee_n, })

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

#valider tous 
def valid_tous_reunion(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_chef_dep = True
			m.validation = "CHEFD"
			m.save()
		elif request.user.user_type == 4:
			m.vld_sous_dir = True
			m.validation = "SOUSD"
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/reunion/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/reunion/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/reunion/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/reunion/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/reunion/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/reunion/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/reunion/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/reunion/unites")

def cancel_valid_tous_reunion(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]
	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_chef_dep = False
			m.save()
		elif request.user.user_type == 4:
			m.vld_sous_dir = False
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/reunion/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/reunion/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/reunion/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/reunion/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/reunion/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/reunion/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/reunion/unite/depense_exp/"+ str(id_unite)+"")
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
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	budget = all_budgets[0]

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
	return render (request=request, template_name="reunion/add_new_compte.html", context={"form":form, 'unite':unite, 'budget':budget})

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

# -------------------------------------- Fin Réunion budget --------------------------------------------------------


# Notification budget --------------------------------------------------------------------------------------------------------------

# ---------------- Budget annuelle -----------

def unites_notif(request):
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	dep_unites = Unite.objects.filter(departement=request.user.departement)
	all_unites = Unite.objects.all()


	# montant total consolidé of unite --------
	#total_unite_dic = {}
	#bdg_total = 0
	state_cadre_dic = {}
	state_chef_dic = {}
	state_sdir_dic = {}
	pr_dic = {}
	# bdg mensulle 
	state_cadre_dic_mens = {}
	state_chef_dic_mens = {}
	state_sdir_dic_mens = {}
	pr_dic_mens = {}

	unite_mens_dispo = {}
	globale_mens_state = True
	for u in all_unites:
		# calculer le montant
		#total = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire=budget).aggregate(Sum('montant'))
		#total_unite_dic[u.id] = total['montant__sum']
		#if total['montant__sum'] != None:
		#	bdg_total = bdg_total + total['montant__sum']

	# get state of unite anuule (Terminé , En cours, ...)
		comptes_nbr = Unite_has_Compte.objects.filter(unite=u).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, type_maj="N", annee_budgetaire = budget).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=u, type_maj="N", annee_budgetaire = budget)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True).count()
		comptes_v_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True).count()
		# valid par tous staus
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1
		if i == 0:
			comptes_valid =  False
		else: 
			comptes_valid =  comptes_done_nbr == i	
		
		# needed status comptes_valid
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid	

		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic[u.id]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic[u.id]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v and comptes_v_sdir == False:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic[u.id]= state_sdir	

		# porcentage de saiser pour l unite
		if comptes_nbr == 0:
			pr = 0
		else :
			pr = int(math.modf((comptes_done_nbr / comptes_nbr)*100)[1])						
		pr_dic[u.id] = pr

	# get state of unite Mensulle (Terminé , En cours, ...)
		#comptes_nbr = Unite_has_Compte.objects.filter(unite=u).count()
		comptes_done_nbr_mens = Compte_has_Montant.objects.filter(unite_compte__unite=u, type_maj="N", mens_done = True,  annee_budgetaire = budget).count()
		comptes_done_mens = Compte_has_Montant.objects.filter(unite_compte__unite=u, type_maj="N", mens_done = True, annee_budgetaire = budget)		
		comptes_v_nbr_mens = Compte_has_Montant.objects.filter(unite_compte__unite=u, type_maj="N", mens_done = True, annee_budgetaire = budget, vld_mens_chef_dep=True).count()
		comptes_v_sdir_nbr_mens = Compte_has_Montant.objects.filter(unite_compte__unite=u, type_maj="N", mens_done = True, annee_budgetaire = budget, vld_mens_sous_dir=True).count()
		# valid par tous staus
		i = 0
		for cd in comptes_done_mens:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1
		if i == 0:
			comptes_valid_mens =  False
		else: 
			comptes_valid_mens =  comptes_done_nbr_mens == i	
		
		# needed status comptes_valid
		comptes_s_mens = comptes_nbr == comptes_done_nbr_mens
		comptes_non_s_mens = comptes_done_nbr_mens == 0
		comptes_v_mens = comptes_nbr == comptes_v_nbr_mens
		comptes_v_sdir_mens = comptes_nbr == comptes_v_sdir_nbr_mens
		#comptes_valid	

		# pour le cadre
		if comptes_s_mens and comptes_valid_mens == False: 
			state_cadre_mens = "Terminé"
		elif comptes_s_mens and comptes_valid_mens: 
			state_cadre_mens = "Validé"
		elif comptes_non_s_mens:
			state_cadre_mens = "Non saisie"
		else:
			state_cadre_mens = "En cours"
		state_cadre_dic_mens[u.id]= state_cadre_mens

		# pour chef dep
		if comptes_non_s_mens:
			state_chef_mens = "Non saisie"
		elif comptes_s_mens and comptes_v_mens == False and comptes_valid_mens == False :
			state_chef_mens = "Instance"
		elif comptes_v_mens and comptes_v_sdir_mens == False:
			state_chef_mens = "Terminé"
		elif comptes_valid_mens and comptes_s_mens and comptes_v_sdir_mens == False:
			state_chef_mens = "Terminé"
		elif comptes_v_sdir_mens:
			state_chef_mens = "Validé"
		else:
			state_chef_mens = "En cours"
		state_chef_dic_mens[u.id]= state_chef_mens

		# pour sous dir
		if comptes_non_s_mens:
			state_sdir_mens = "Non saisie"
		elif comptes_s_mens and comptes_v_mens and comptes_v_sdir_mens == False:
			state_sdir_mens = "Instance"
		elif comptes_v_sdir_mens and comptes_s_mens:
			state_sdir_mens = "Terminé"
		else:
			state_sdir_mens = "En cours"
		state_sdir_dic_mens[u.id]= state_sdir_mens	

		# porcentage de saiser pour l unite
		if comptes_nbr == 0:
			pr_mens = 0
		else :
			pr_mens = int(math.modf((comptes_done_nbr_mens / comptes_nbr)*100)[1])						
		pr_dic_mens[u.id] = pr_mens

	# status globale  mensulle et annuel
		# mensulle
		montants_u_v =  Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte__unite=u, vld_sous_dir=True).count()
		comptes_u = Unite_has_Compte.objects.filter(unite=u).count()
		mens_disp = comptes_u == montants_u_v
		unite_mens_dispo[u.id] = mens_disp

		globale_mens_state = globale_mens_state and mens_disp


	# annulle 
	all_comptes_nbr = Unite_has_Compte.objects.all().count()
	all_done_nbr =  Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N").count()
	all_done =  Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N")
	all_valid_sdir_nbr =  Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", vld_sous_dir=True).count()
	all_valid_chef_nbr =  Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", vld_chef_dep=True).count()
	
	# --------------------------
	i = 0
	for cd in all_done:
		if cd.vld_chef_dep or cd.vld_sous_dir : 
			i = i+1

	if i == 0:
		all_valid = False
	else: 
		all_valid = all_done_nbr == i
	#--------------------------
	bdg_ann_done = all_comptes_nbr == all_done_nbr
	bdg_ann_non_s = all_comptes_nbr == 0
	bdg_ann_valid_chef = all_comptes_nbr == all_valid_chef_nbr
	bdg_ann_valid_sdir = all_comptes_nbr == all_valid_sdir_nbr
	bdg_ann_valid = all_valid
	# status cadre 
	state_ann_cadre=""
	if bdg_ann_done and bdg_ann_valid == False :
		state_ann_cadre = "Terminé"
	elif bdg_ann_valid and bdg_ann_done :
		state_ann_cadre = "Validé"
	elif bdg_ann_non_s :
		state_ann_cadre = "Non saisie"
	else :
		state_ann_cadre = "En cours"

	# status chef 
	state_ann_chef=""
	if bdg_ann_done and bdg_ann_valid_chef and bdg_ann_valid_sdir == False :
		state_ann_chef = "Terminé"
	elif bdg_ann_valid_sdir :
		state_ann_chef = "Validé"
	elif bdg_ann_done and bdg_ann_valid == False :
		state_ann_chef = "Instance"
	elif bdg_ann_non_s :
		state_ann_chef = "Non saisie"
	else :
		state_ann_chef = "En cours"
	
	# status sdir 
	state_ann_sdir=""
	if bdg_ann_done and bdg_ann_valid_sdir :
		state_ann_sdir = "Terminé"
	elif bdg_ann_done and bdg_ann_valid:
		state_ann_sdir = "Instance"
	elif bdg_ann_non_s :
		state_ann_sdir = "Non saisie"
	else :
		state_ann_sdir = "En cours"




	#------------------------------------------


	return render(request,"notif/unites.html", {'unites':unites, 'dep_unites':dep_unites, 'all_unites':all_unites, 'budget':budget,
													'state_cadre_dic':state_cadre_dic, 'state_chef_dic':state_chef_dic, 'state_sdir_dic':state_sdir_dic, 'pr_dic':pr_dic, 'unite_mens_dispo':unite_mens_dispo,
													'state_cadre_dic_mens':state_cadre_dic_mens, 'state_chef_dic_mens':state_chef_dic_mens, 'state_sdir_dic_mens':state_sdir_dic_mens, 'pr_dic_mens':pr_dic_mens, 
													'globale_mens_state':globale_mens_state , 'state_ann_cadre':state_ann_cadre, 'state_ann_chef':state_ann_chef, 'state_ann_sdir':state_ann_sdir })

def unite_detail_notif(request, id):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]
	unite = Unite.objects.get(id=id)
	comptes_nbr = Unite_has_Compte.objects.filter(unite=unite).count()
	comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget,).count()
	comptes_vld_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True).count()	
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
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=1).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=4).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par chef dep
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par sous dir
	offre_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=7).count()
	
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

	#Check if chapitre is validé par sous directeur
	offre_v_sdir = offre_nbr==offre_valid_sdir_nbr
	traffic_v_sdir = traffic_nbr==traffic_valid_sdir_nbr
	ca_emmission_v_sdir = ca_emmission_nbr==ca_emmission_valid_sdir_nbr
	ca_transport_v_sdir = ca_transport_nbr==ca_transport_valid_sdir_nbr
	recettes_v_sdir = recettes_nbr==recettes_valid_sdir_nbr
	depense_fonc_v_sdir = depense_fonc_nbr==depense_fonc_valid_sdir_nbr
	depense_exp_v_sdir = depense_exp_nbr==depense_exp_valid_sdir_nbr

	#Check if chapitre is not validé par chef dep ( = compte validé)
	offre_non_v = offre_valid_nbr == 0
	traffic_non_v = traffic_valid_nbr == 0
	ca_emmission_non_v = ca_emmission_valid_nbr == 0
	ca_transport_non_v = ca_transport_valid_nbr == 0
	recettes_non_v = recettes_valid_nbr == 0
	depense_fonc_non_v = depense_fonc_valid_nbr == 0
	depense_exp_non_v = depense_exp_valid_nbr == 0

	#Check if chapitre is not validé par sous directeur( = compte validé)
	offre_non_v_sdir = offre_valid_sdir_nbr == 0
	traffic_non_v_sdir = traffic_valid_sdir_nbr == 0
	ca_emmission_non_v_sdir = ca_emmission_valid_sdir_nbr == 0
	ca_transport_non_v_sdir = ca_transport_valid_sdir_nbr == 0
	recettes_non_v_sdir = recettes_valid_sdir_nbr == 0
	depense_fonc_non_v_sdir = depense_fonc_valid_sdir_nbr == 0
	depense_exp_non_v_sdir = depense_exp_valid_sdir_nbr == 0

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	offre_valid = is_valid(1)
	traffic_valid = is_valid(2)
	ca_emmission_valid = is_valid(3)
	ca_transport_valid = is_valid(4)
	recettes_valid = is_valid(5)
	depense_fonc_valid = is_valid(6)
	depense_exp_valid = is_valid(7)

	return render(request,"notif/unite_detail.html", {'unite':unite, 'comptes_nbr':comptes_nbr, 'comptes_done_nbr':comptes_done_nbr, 'pr_cdr':pr_cdr, 'pr_vcd':pr_vcd, 'budget':budget, 
															'offre_s':offre_s, 'traffic_s':traffic_s, 'ca_emmission_s':ca_emmission_s, 'ca_transport_s':ca_transport_s,
															'recettes_s':recettes_s, 'depense_fonc_s':depense_fonc_s, 'depense_exp_s':depense_exp_s,
															'offre_v':offre_v, 'traffic_v':traffic_v, 'ca_emmission_v':ca_emmission_v, 'ca_transport_v':ca_transport_v,
															'recettes_v':recettes_v, 'depense_fonc_v':depense_fonc_v, 'depense_exp_v':depense_exp_v,
															'offre_non_s':offre_non_s, 'traffic_non_s':traffic_non_s, 'ca_emmission_non_s':ca_emmission_non_s, 'ca_transport_non_s':ca_transport_non_s,
															'recettes_non_s':recettes_non_s, 'depense_fonc_non_s':depense_fonc_non_s, 'depense_exp_non_s':depense_exp_non_s,
															'offre_non_v':offre_non_v, 'traffic_non_v':traffic_non_v, 'ca_emmission_non_v':ca_emmission_non_v, 'ca_transport_non_v':ca_transport_non_v,
															'recettes_non_v':recettes_non_v, 'depense_fonc_non_v':depense_fonc_non_v, 'depense_exp_non_v':depense_exp_non_v,

															'offre_non_v_sdir':offre_non_v_sdir, 'traffic_non_v_sdir':traffic_non_v_sdir, 'ca_emmission_non_v_sdir':ca_emmission_non_v_sdir, 'ca_transport_non_v_sdir':ca_transport_non_v_sdir,
															'recettes_non_v_sdir':recettes_non_v_sdir, 'depense_fonc_non_v_sdir':depense_fonc_non_v_sdir, 'depense_exp_non_v_sdir':depense_exp_non_v_sdir,
															'offre_v_sdir':offre_v_sdir, 'traffic_v_sdir':traffic_v_sdir, 'ca_emmission_v_sdir':ca_emmission_v_sdir, 'ca_transport_v_sdir':ca_transport_v_sdir,
															'recettes_v_sdir':recettes_v_sdir, 'depense_fonc_v_sdir':depense_fonc_v_sdir, 'depense_exp_v_sdir':depense_exp_v_sdir,

															'offre_valid':offre_valid, 'traffic_valid':traffic_valid, 'ca_emmission_valid':ca_emmission_valid, 'ca_transport_valid':ca_transport_valid, 'recettes_valid':recettes_valid,
															'depense_fonc_valid':depense_fonc_valid, 'depense_exp_valid':depense_exp_valid
															})

def offre_comptes_notif(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	# chapitre (offre)
	chapitre = Chapitre.objects.get(code_num=1)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=1)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]
	#print(cm_dict)

	offre_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=1).count()
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=1).count()
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	offre_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=1).count()
	
	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	offre_valid = is_valid(1)

	offre_s = offre_nbr==offre_done_nbr
	offre_non_s = offre_done_nbr == 0
	offre_v = offre_nbr==offre_valid_nbr
	offre_v_sdir = offre_nbr==offre_valid_sdir_nbr

	return render(request,"notif/offre_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":offre_s, "c_non_s":offre_non_s, "c_v":offre_v, 'c_v_sdir':offre_v_sdir, 'c_valid':offre_valid , 'cm_dict':cm_dict,
														 'budget':budget, 'chapitre':chapitre})

def traffic_comptes_notif(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=2)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=2)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	traffic_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=2).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=2).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()
	traffic_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=2).count()

	traffic_s = traffic_nbr==traffic_done_nbr
	traffic_non_s = traffic_done_nbr == 0
	traffic_v = traffic_nbr==traffic_valid_nbr
	traffic_v_sdir = traffic_nbr==traffic_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	traffic_valid = is_valid(2)	


	return render(request,"notif/traffic_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":traffic_s, "c_non_s":traffic_non_s, "c_v":traffic_v, 'budget':budget, 'cm_dict':cm_dict,
															'c_valid':traffic_valid, 'c_v_sdir':traffic_v_sdir, 'chapitre':chapitre })

def ca_emmission_comptes_notif(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=3)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=3)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	ca_emmission_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=3).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=3).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_emmission_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=3).count()
	
	ca_emmission_s = ca_emmission_nbr==ca_emmission_done_nbr
	ca_emmission_non_s = ca_emmission_done_nbr == 0
	ca_emmission_v = ca_emmission_nbr==ca_emmission_valid_nbr
	ca_emmission_v_sdir = ca_emmission_nbr==ca_emmission_valid_sdir_nbr


	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	ca_emmission_valid = is_valid(3)	

	return render(request,"notif/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":ca_emmission_s, "c_non_s":ca_emmission_non_s, "c_v":ca_emmission_v, 'budget':budget, 'cm_dict':cm_dict,
																'c_valid':ca_emmission_valid, 'c_v_sdir':ca_emmission_v_sdir, 'chapitre':chapitre })

def ca_transport_comptes_notif(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=4)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=4).order_by('-reseau_compte')
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	ca_transport_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=4).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=4).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()
	ca_transport_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=4).count()

	ca_transport_s = ca_transport_nbr==ca_transport_done_nbr
	ca_transport_non_s = ca_transport_done_nbr == 0
	ca_transport_v = ca_transport_nbr==ca_transport_valid_nbr
	ca_transport_v_sdir = ca_transport_nbr==ca_transport_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	ca_transport_valid = is_valid(4)	

	return render(request,"notif/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":ca_transport_s, "c_non_s":ca_transport_non_s, "c_v":ca_transport_v, 'budget':budget, 'cm_dict':cm_dict,
																'c_valid':ca_transport_valid, 'c_v_sdir':ca_transport_v_sdir, 'chapitre':chapitre })

def recettes_comptes_notif(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=5)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=5)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	recettes_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=5).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=5).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()
	recettes_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=5).count()

	recettes_s = recettes_nbr==recettes_done_nbr
	recettes_non_s = recettes_done_nbr == 0
	recettes_v = recettes_nbr==recettes_valid_nbr
	recettes_v_sdir = recettes_nbr==recettes_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	recettes_valid = is_valid(5)	

	return render(request,"notif/recettes_comptes.html", {'unite':unite, 'comptes':comptes, "c_s":recettes_s, "c_non_s":recettes_non_s, "c_v":recettes_v, 'budget':budget, 'cm_dict':cm_dict,
															'c_valid':recettes_valid, 'c_v_sdir':recettes_v_sdir, 'chapitre':chapitre })

def depense_fonc_comptes_notif(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=6)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=6)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)
	#for c in comptes:
	#	if c.regle_par != unite:
	#		comptes_regle_par_autre.append(c)	
	
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
	
	# clacule les pos 2 saisier state -----------------------
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	state_sdir_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False and comptes_valid:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_unite[c2.numero]= state_sdir		

	# comptes par autre -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	state_sdir_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2)
		comptes_all = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, compte__ref__ref__ref=c2)
		comptes_autre = comptes_all.difference(comptes_unite)  

		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, compte__ref__ref__ref=c2).count()
		#comptes_nbr = comptes_all_nbr - comptes_unite_nbr
		comptes_nbr = comptes_all.difference(comptes_unite).count()


		done_par_unite = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6)
		done_all = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N",  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6)
		comptes_done = done_all.difference(done_par_unite)
		

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N",  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		#comptes_done_nbr = done_all_nbr - done_par_unite_nbr
		comptes_done_nbr = comptes_done.count()


		#check chef dep validation 
		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		#check sous dir validation
		comptes_vsdir_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_vsdir_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_sdir_nbr = comptes_vsdir_all_nbr - comptes_vsdir_unite_nbr
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False and comptes_valid:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_autre[c2.numero]= state_sdir	

	# --------------------------------------------------------

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
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=6).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_fonc_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=6).count()


	depense_fonc_s = depense_fonc_nbr==depense_fonc_done_nbr
	depense_fonc_non_s = depense_fonc_done_nbr == 0
	depense_fonc_v = depense_fonc_nbr==depense_fonc_valid_nbr
	depense_fonc_v_sdir = depense_fonc_nbr==depense_fonc_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	depense_fonc_valid = is_valid(6)	

	return render(request,"notif/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes, 'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																"c_s":depense_fonc_s, "c_non_s":depense_fonc_non_s, "c_v":depense_fonc_v, 'budget':budget,
																"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																"c_valid":depense_fonc_valid, 'c_v_sdir':depense_fonc_v_sdir, 'chapitre':chapitre,
																'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre,
																'state_sdir_dic_par_unite':state_sdir_dic_par_unite, 'state_sdir_dic_par_autre':state_sdir_dic_par_autre })

def depense_exp_comptes_notif(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=7)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	

	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=7)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)

	#for c in comptes:
	#	if c.regle_par != unite:
	#		comptes_regle_par_autre.append(c)	

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

	# clacule les pos 2 saisier state--------------------- 
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	state_sdir_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_unite[c2.numero]= state_sdir		

	# comptes par autre -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	state_sdir_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2)
		comptes_all = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, compte__ref__ref__ref=c2)
		comptes_autre = comptes_all.difference(comptes_unite)  

		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, compte__ref__ref__ref=c2).count()
		#comptes_nbr = comptes_all_nbr - comptes_unite_nbr
		comptes_nbr = comptes_all.difference(comptes_unite).count()


		done_par_unite = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7)
		done_all = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7)
		comptes_done = done_all.difference(done_par_unite)
		

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		#comptes_done_nbr = done_all_nbr - done_par_unite_nbr
		comptes_done_nbr = comptes_done.count()


		#check chef dep validation 
		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		#check sous dir validation
		comptes_vsdir_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_vsdir_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_sdir_nbr = comptes_vsdir_all_nbr - comptes_vsdir_unite_nbr
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False and comptes_valid:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_autre[c2.numero]= state_sdir	

	# --------------------------------------------------------

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
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=7).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()
	depense_exp_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, vld_sous_dir=True, unite_compte__compte__chapitre__code_num=7).count()

	depense_exp_s = depense_exp_nbr==depense_exp_done_nbr
	depense_exp_non_s = depense_exp_done_nbr == 0
	depense_exp_v = depense_exp_nbr==depense_exp_valid_nbr
	depense_exp_v_sdir = depense_exp_nbr==depense_exp_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_chef_dep or cd.vld_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	depense_exp_valid = is_valid(7)	

	return render(request,"notif/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes,  'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																	"c_s":depense_exp_s, "c_non_s":depense_exp_non_s, "c_v":depense_exp_v, 'budget':budget,
																	"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																	"c_valid":depense_exp_valid, 'c_v_sdir':depense_exp_v_sdir, 'chapitre':chapitre,
																	'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																	'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre,
																	'state_sdir_dic_par_unite':state_sdir_dic_par_unite, 'state_sdir_dic_par_autre':state_sdir_dic_par_autre })

# add montant to compte 
def add_montant_notif(request, id):
	unite_compte = Unite_has_Compte.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]
	# get proposition and reun of this compte
	m_propos_l = Compte_has_Montant.objects.filter(unite_compte=unite_compte, annee_budgetaire__annee=budget.annee, annee_budgetaire__type_bdg="PROPOS")
	m_reun_l = Compte_has_Montant.objects.filter(unite_compte=unite_compte, annee_budgetaire__annee=budget.annee, annee_budgetaire__type_bdg="REUN")
	
	if len(m_propos_l) == 0:
		m_propos = "null"
	else: 
		m_propos = m_propos_l[0]

	if len(m_reun_l) == 0:
		m_reun = "null"
	else: 
		m_reun = m_reun_l[0]

	comment_form = CommentaireForm(request.POST or None)
	montant_form = MontantOnlyForm(request.POST or None)
	if request.method == "POST":
		if  montant_form.is_valid():
			montant_compte = montant_form.save(commit=False)
			montant_compte.unite_compte = unite_compte
			montant_compte.type_bdg = "NOTIF"
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
			messages.success(request, "compte saisié successfuly." )
		# Redirecter vers chaque chapitre
			if unite_compte.compte.chapitre.code_num== 1:
				return redirect("/notif/unite/offre/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 2:
				return redirect("/notif/unite/traffic/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 3:
				return redirect("/notif/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 4:
				return redirect("/notif/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 5:
				return redirect("/notif/unite/recettes/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 6:
				return redirect("/notif/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 7:
				return redirect("/notif/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
			else:
				return redirect("/notif/unites")
		messages.error(request, "Unsuccessful . Invalid information.")
	
	return render (request=request, template_name="notif/add_montant.html", context={"montant_form":montant_form, "comment_form":comment_form, "unite_compte":unite_compte, "budget":budget,
																						'm_propos':m_propos, 'm_reun':m_reun })

def update_montant_notif(request, id): 
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]	

	form = MontantOnlyForm(request.POST or None, instance = montant)
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
			return redirect("/notif/unite/offre/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 2:
			return redirect("/notif/unite/traffic/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 3:
			return redirect("/notif/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 4:
			return redirect("/notif/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 5:
			return redirect("/notif/unite/recettes/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 6:
			return redirect("/notif/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 7:
			return redirect("/notif/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
		else:
			return redirect("/notif/unites")
	return render (request=request, template_name="notif/update_montant.html", context={"form":form, "unite_compte":unite_compte, "montant":montant, "budget":budget})

def valid_montant_notif(request, id):
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
		return HttpResponseRedirect("/notif/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/notif/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/notif/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/notif/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/notif/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/notif/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/notif/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/notif/unites")

#valider tous 
def valid_tous_notif(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, type_maj="N", annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_chef_dep = True
			m.validation = "CHEFD"
			m.save()
		elif request.user.user_type == 4:
			m.vld_sous_dir = True
			m.validation = "SOUSD"
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/notif/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/notif/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/notif/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/notif/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/notif/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/notif/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/notif/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/notif/unites")

def cancel_valid_tous_notif(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]
	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, type_maj="N", annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_chef_dep = False
			m.save()
		elif request.user.user_type == 4:
			m.vld_sous_dir = False
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/notif/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/notif/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/notif/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/notif/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/notif/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/notif/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/notif/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/notif/unites")	

def cancel_valid_montant_notif(request, id):
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
		return HttpResponseRedirect("/notif/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/notif/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/notif/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/notif/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/notif/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/notif/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/notif/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/notif/unites")

def add_new_compte_notif(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]
	form = AddCompteUniteForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			compte_unite = form.save(commit=False)
			compte_unite.unite = unite
			compte_unite.added_by = request.user
			compte_unite.code = compte_unite.unite.code_alpha + str(compte_unite.compte.numero) + compte_unite.regle_par.code_alpha + compte_unite.reseau_compte
			compte_unite.save()
			messages.success(request, "compte added successfuly." )
			return HttpResponseRedirect("/notif/unite/"+ str(unite.id)+"")
			
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="notif/add_new_compte.html", context={"form":form, 'budget':budget, 'unite':unite})

def delete_added_compte_notif(request,id):
	form = Unite_has_Compte.objects.get(id=id)
	unite = form.unite
	compte = form.compte
	form.delete()
	# Redirecter vers chaque chapitre
	if compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/notif/unite/offre/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/notif/unite/traffic/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/notif/unite/ca_emmission/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/notif/unite/ca_transport/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/notif/unite/recettes/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/notif/unite/depense_fonc/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/notif/unite/depense_exp/"+ str(unite.id)+"")
	else:
		return HttpResponseRedirect("/notif/unites")	

# comments
def update_comment_notif(request, id): 
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]
	comment = get_object_or_404(Commentaire, id = id)
	form = CommentaireForm(request.POST or None, instance = comment)
	if form.is_valid():
		form.save()
		messages.success(request, "Commentaire updated successfuly." )
		return redirect("/notif/unites")

	return render (request=request, template_name="notif/update_comment.html", context={"form":form, "comment":comment, "budget":budget})

def delete_comment_notif(request, id):
    form = Commentaire.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/notif/unites")


# ---------------- Budget Mensulle -----------
# send comptes_montants and update the 
# new form first update (config type decoupage )
# new form second update months 
# check if equals montants else rise error
# initialise edition to 0 &  maj_type none

def unite_detail_notif_m(request, id):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id)
	comptes_nbr = Unite_has_Compte.objects.filter(unite=unite).count()
	comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True).count()
	comptes_vld_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget,  mens_done=True, vld_mens_chef_dep=True).count()	
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
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par chef dep
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par sous dir
	offre_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=7).count()
	
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

	#Check if chapitre is validé par sous directeur
	offre_v_sdir = offre_nbr==offre_valid_sdir_nbr
	traffic_v_sdir = traffic_nbr==traffic_valid_sdir_nbr
	ca_emmission_v_sdir = ca_emmission_nbr==ca_emmission_valid_sdir_nbr
	ca_transport_v_sdir = ca_transport_nbr==ca_transport_valid_sdir_nbr
	recettes_v_sdir = recettes_nbr==recettes_valid_sdir_nbr
	depense_fonc_v_sdir = depense_fonc_nbr==depense_fonc_valid_sdir_nbr
	depense_exp_v_sdir = depense_exp_nbr==depense_exp_valid_sdir_nbr

	#Check if chapitre is not validé par chef dep ( = compte validé)
	offre_non_v = offre_valid_nbr == 0
	traffic_non_v = traffic_valid_nbr == 0
	ca_emmission_non_v = ca_emmission_valid_nbr == 0
	ca_transport_non_v = ca_transport_valid_nbr == 0
	recettes_non_v = recettes_valid_nbr == 0
	depense_fonc_non_v = depense_fonc_valid_nbr == 0
	depense_exp_non_v = depense_exp_valid_nbr == 0

	#Check if chapitre is not validé par sous directeur( = compte validé)
	offre_non_v_sdir = offre_valid_sdir_nbr == 0
	traffic_non_v_sdir = traffic_valid_sdir_nbr == 0
	ca_emmission_non_v_sdir = ca_emmission_valid_sdir_nbr == 0
	ca_transport_non_v_sdir = ca_transport_valid_sdir_nbr == 0
	recettes_non_v_sdir = recettes_valid_sdir_nbr == 0
	depense_fonc_non_v_sdir = depense_fonc_valid_sdir_nbr == 0
	depense_exp_non_v_sdir = depense_exp_valid_sdir_nbr == 0

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True,  annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	offre_valid = is_valid(1)
	traffic_valid = is_valid(2)
	ca_emmission_valid = is_valid(3)
	ca_transport_valid = is_valid(4)
	recettes_valid = is_valid(5)
	depense_fonc_valid = is_valid(6)
	depense_exp_valid = is_valid(7)

	return render(request,"notif/mens/unite_detail.html", {'unite':unite, 'comptes_nbr':comptes_nbr, 'comptes_done_nbr':comptes_done_nbr, 'pr_cdr':pr_cdr, 'pr_vcd':pr_vcd, 'budget':budget, 
															'offre_s':offre_s, 'traffic_s':traffic_s, 'ca_emmission_s':ca_emmission_s, 'ca_transport_s':ca_transport_s,
															'recettes_s':recettes_s, 'depense_fonc_s':depense_fonc_s, 'depense_exp_s':depense_exp_s,
															'offre_v':offre_v, 'traffic_v':traffic_v, 'ca_emmission_v':ca_emmission_v, 'ca_transport_v':ca_transport_v,
															'recettes_v':recettes_v, 'depense_fonc_v':depense_fonc_v, 'depense_exp_v':depense_exp_v,
															'offre_non_s':offre_non_s, 'traffic_non_s':traffic_non_s, 'ca_emmission_non_s':ca_emmission_non_s, 'ca_transport_non_s':ca_transport_non_s,
															'recettes_non_s':recettes_non_s, 'depense_fonc_non_s':depense_fonc_non_s, 'depense_exp_non_s':depense_exp_non_s,
															'offre_non_v':offre_non_v, 'traffic_non_v':traffic_non_v, 'ca_emmission_non_v':ca_emmission_non_v, 'ca_transport_non_v':ca_transport_non_v,
															'recettes_non_v':recettes_non_v, 'depense_fonc_non_v':depense_fonc_non_v, 'depense_exp_non_v':depense_exp_non_v,

															'offre_non_v_sdir':offre_non_v_sdir, 'traffic_non_v_sdir':traffic_non_v_sdir, 'ca_emmission_non_v_sdir':ca_emmission_non_v_sdir, 'ca_transport_non_v_sdir':ca_transport_non_v_sdir,
															'recettes_non_v_sdir':recettes_non_v_sdir, 'depense_fonc_non_v_sdir':depense_fonc_non_v_sdir, 'depense_exp_non_v_sdir':depense_exp_non_v_sdir,
															'offre_v_sdir':offre_v_sdir, 'traffic_v_sdir':traffic_v_sdir, 'ca_emmission_v_sdir':ca_emmission_v_sdir, 'ca_transport_v_sdir':ca_transport_v_sdir,
															'recettes_v_sdir':recettes_v_sdir, 'depense_fonc_v_sdir':depense_fonc_v_sdir, 'depense_exp_v_sdir':depense_exp_v_sdir,

															'offre_valid':offre_valid, 'traffic_valid':traffic_valid, 'ca_emmission_valid':ca_emmission_valid, 'ca_transport_valid':ca_transport_valid, 'recettes_valid':recettes_valid,
															'depense_fonc_valid':depense_fonc_valid, 'depense_exp_valid':depense_exp_valid
															})

def offre_comptes_notif_m(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	# chapitre (offre)
	chapitre = Chapitre.objects.get(code_num=1)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	c_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=chapitre.code_num).count()
	c_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()

	c_s = c_nbr==c_done_nbr
	c_non_s = c_done_nbr == 0
	c_v = c_nbr==c_valid_nbr
	c_v_sdir = c_nbr==c_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	c_valid = is_valid(chapitre.code_num)	

	return render(request,"notif/mens/offre_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
														 'c_valid':c_valid, 'c_v_sdir':c_v_sdir, "c_s":c_s, "c_non_s":c_non_s, "c_v":c_non_s})

def traffic_comptes_notif_m(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=2)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, type_maj="N", unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	c_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=chapitre.code_num).count()
	c_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()

	c_s = c_nbr==c_done_nbr
	c_non_s = c_done_nbr == 0
	c_v = c_nbr==c_valid_nbr
	c_v_sdir = c_nbr==c_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	c_valid = is_valid(chapitre.code_num)	


	return render(request,"notif/mens/traffic_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
														 'c_valid':c_valid, 'c_v_sdir':c_v_sdir, "c_s":c_s, "c_non_s":c_non_s, "c_v":c_non_s })

def ca_emmission_comptes_notif_m(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=3)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c, type_maj="N")
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	c_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=chapitre.code_num).count()
	c_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()

	c_s = c_nbr==c_done_nbr
	c_non_s = c_done_nbr == 0
	c_v = c_nbr==c_valid_nbr
	c_v_sdir = c_nbr==c_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	c_valid = is_valid(chapitre.code_num)	

	return render(request,"notif/mens/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
														 'c_valid':c_valid, 'c_v_sdir':c_v_sdir, "c_s":c_s, "c_non_s":c_non_s, "c_v":c_non_s })

def ca_transport_comptes_notif_m(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=4)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num).order_by('-reseau_compte')
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c, type_maj="N")
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	c_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=chapitre.code_num).count()
	c_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()

	c_s = c_nbr==c_done_nbr
	c_non_s = c_done_nbr == 0
	c_v = c_nbr==c_valid_nbr
	c_v_sdir = c_nbr==c_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite,  type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	c_valid = is_valid(chapitre.code_num)		

	return render(request,"notif/mens/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
														 'c_valid':c_valid, 'c_v_sdir':c_v_sdir, "c_s":c_s, "c_non_s":c_non_s, "c_v":c_non_s })

def recettes_comptes_notif_m(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]
	chapitre = Chapitre.objects.get(code_num=5)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c, type_maj="N")
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	c_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=chapitre.code_num).count()
	c_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()

	c_s = c_nbr==c_done_nbr
	c_non_s = c_done_nbr == 0
	c_v = c_nbr==c_valid_nbr
	c_v_sdir = c_nbr==c_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	c_valid = is_valid(chapitre.code_num)	

	return render(request,"notif/mens/recettes_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict, 'chapitre':chapitre,
															'c_valid':c_valid, 'c_v_sdir':c_v_sdir, "c_s":c_s, "c_non_s":c_non_s, "c_v":c_non_s })

def depense_fonc_comptes_notif_m(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=6)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c, type_maj="N")
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	c_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=chapitre.code_num).count()
	c_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()

	c_s = c_nbr==c_done_nbr
	c_non_s = c_done_nbr == 0
	c_v = c_nbr==c_valid_nbr
	c_v_sdir = c_nbr==c_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	c_valid = is_valid(chapitre.code_num)	

	# ---------- status détailleé---------
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=6)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)
	#for c in comptes:
	#	if c.regle_par != unite:
	#		comptes_regle_par_autre.append(c)	
	
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
	
	# clacule les pos 2 saisier state -----------------------
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	state_sdir_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite, mens_done=True,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite, mens_done=True,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite, mens_done=True,  vld_mens_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite,mens_done=True,  vld_mens_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False and comptes_valid:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_unite[c2.numero]= state_sdir		

	# comptes par autre -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	state_sdir_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2)
		comptes_all = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, compte__ref__ref__ref=c2)
		comptes_autre = comptes_all.difference(comptes_unite)  

		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, compte__ref__ref__ref=c2).count()
		#comptes_nbr = comptes_all_nbr - comptes_unite_nbr
		comptes_nbr = comptes_all.difference(comptes_unite).count()


		done_par_unite = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite, mens_done=True,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6)
		done_all = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire=budget, mens_done=True, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6)
		comptes_done = done_all.difference(done_par_unite)
		

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		#comptes_done_nbr = done_all_nbr - done_par_unite_nbr
		comptes_done_nbr = comptes_done.count()


		#check chef dep validation 
		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True,  vld_mens_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		#check sous dir validation
		comptes_vsdir_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_vsdir_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, vld_mens_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_sdir_nbr = comptes_vsdir_all_nbr - comptes_vsdir_unite_nbr
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False and comptes_valid:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_autre[c2.numero]= state_sdir	

	# --------------------------------------------------------

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

	

	return render(request,"notif/mens/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes, 'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																'c_valid':c_valid, 'c_v_sdir':c_v_sdir, "c_s":c_s, "c_non_s":c_non_s, "c_v":c_non_s, 'budget':budget, 'chapitre':chapitre,
																"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre,
																'state_sdir_dic_par_unite':state_sdir_dic_par_unite, 'state_sdir_dic_par_autre':state_sdir_dic_par_autre })

def depense_exp_comptes_notif_m(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=7)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c, type_maj="N")
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	c_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=chapitre.code_num).count()
	c_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_chef_dep=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()
	c_valid_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, vld_mens_sous_dir=True, unite_compte__compte__chapitre__code_num=chapitre.code_num).count()

	c_s = c_nbr==c_done_nbr
	c_non_s = c_done_nbr == 0
	c_v = c_nbr==c_valid_nbr
	c_v_sdir = c_nbr==c_valid_sdir_nbr

	# valid tout chef or sdir
	def is_valid(num):
		compte_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num)
		compte_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", annee_budgetaire = budget, mens_done=True, unite_compte__compte__chapitre__code_num=num).count()
		i = 0
		for cd in compte_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			return False
		else: 
			return compte_done_nbr == i
	#--------------------------
	c_valid = is_valid(chapitre.code_num)	

	# ---- status detailleé -------------------------------
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=7)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)

	#for c in comptes:
	#	if c.regle_par != unite:
	#		comptes_regle_par_autre.append(c)	

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

	# clacule les pos 2 saisier state--------------------- 
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	state_sdir_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite, mens_done=True, annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite, mens_done=True,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite, mens_done=True,  vld_mens_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_sdir_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", unite_compte__regle_par=unite, mens_done=True, vld_mens_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_unite[c2.numero]= state_sdir		

	# comptes par autre -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	state_sdir_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2)
		comptes_all = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, compte__ref__ref__ref=c2)
		comptes_autre = comptes_all.difference(comptes_unite)  

		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, compte__ref__ref__ref=c2).count()
		#comptes_nbr = comptes_all_nbr - comptes_unite_nbr
		comptes_nbr = comptes_all.difference(comptes_unite).count()


		done_par_unite = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7)
		done_all = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7)
		comptes_done = done_all.difference(done_par_unite)
		

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		#comptes_done_nbr = done_all_nbr - done_par_unite_nbr
		comptes_done_nbr = comptes_done.count()


		#check chef dep validation 
		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, vld_mens_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		#check sous dir validation
		comptes_vsdir_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, unite_compte__regle_par=unite,  vld_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_vsdir_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, type_maj="N", mens_done=True, vld_mens_sous_dir=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_sdir_nbr = comptes_vsdir_all_nbr - comptes_vsdir_unite_nbr
		
		#--------------------------
		i = 0
		for cd in comptes_done:
			if cd.vld_mens_chef_dep or cd.vld_mens_sous_dir : 
				i = i+1

		if i == 0:
			comptes_valid = False
		else: 
			comptes_valid = comptes_done_nbr == i
		#--------------------------	

		# nedded states 
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		comptes_v_sdir = comptes_nbr == comptes_v_sdir_nbr
		#comptes_valid
		
		# pour le cadre
		if comptes_s and comptes_valid == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_valid: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False and comptes_valid == False :
			state_chef = "Instance"
		elif comptes_v and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_valid and comptes_s and comptes_v_sdir == False:
			state_chef = "Terminé"
		elif comptes_v_sdir:
			state_chef = "Validé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef

		# pour sous dir
		if comptes_non_s:
			state_sdir = "Non saisie"
		elif comptes_s and comptes_v_sdir == False and comptes_valid:
			state_sdir = "Instance"
		elif comptes_v_sdir and comptes_s:
			state_sdir = "Terminé"
		else:
			state_sdir = "En cours"
		state_sdir_dic_par_autre[c2.numero]= state_sdir	

	# --------------------------------------------------------

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

	return render(request,"notif/mens/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes,  'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																	'c_valid':c_valid, 'c_v_sdir':c_v_sdir, "c_s":c_s, "c_non_s":c_non_s, "c_v":c_non_s, 'budget':budget, 'chapitre':chapitre,
																	"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																	'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																	'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre,
																	'state_sdir_dic_par_unite':state_sdir_dic_par_unite, 'state_sdir_dic_par_autre':state_sdir_dic_par_autre })

# add montant to compte 
def add_montant_notif_m(request, id):
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	form = TypeDecoupeMontantForm(request.POST or None, instance = montant)
	if  form.is_valid():
		form.save()
		# ajouter le montant mensuelle selon la dévision 
		new_montant = get_object_or_404(Compte_has_Montant, id = id)
		m_annul = new_montant.montant
		if new_montant.type_decoupage == "MS":
			m = int(m_annul/12 ) 
			rest = m_annul - (m*12)
			new_montant.janvier = m + rest
			new_montant.fevrier = m
			new_montant.mars = m
			new_montant.avril = m
			new_montant.mai = m
			new_montant.juin = m
			new_montant.juillet = m
			new_montant.aout = m
			new_montant.septemre = m
			new_montant.octobre = m
			new_montant.novembre = m
			new_montant.decembre = m
		elif new_montant.type_decoupage == "BM": 
			m = int(m_annul/6 ) 
			rest = m_annul - (m*6)
			new_montant.janvier = m + rest
			new_montant.fevrier = 0
			new_montant.mars = m
			new_montant.avril = 0
			new_montant.mai = m
			new_montant.juin = 0
			new_montant.juillet = m
			new_montant.aout = 0
			new_montant.septemre = m
			new_montant.octobre = 0
			new_montant.novembre = m
			new_montant.decembre = 0			
		elif new_montant.type_decoupage == "TR": 
			m = int(m_annul/4 )
			rest = m_annul - (m*4) 
			new_montant.janvier = m + rest
			new_montant.fevrier = 0
			new_montant.mars = 0
			new_montant.avril = m
			new_montant.mai =0 
			new_montant.juin = 0
			new_montant.juillet = m
			new_montant.aout = 0
			new_montant.septemre = 0
			new_montant.octobre = m
			new_montant.novembre = 0
			new_montant.decembre = 0			
		elif new_montant.type_decoupage == "SM": 
			m = int(m_annul/2 ) 
			rest = m_annul - (m*2)
			new_montant.janvier = m + rest
			new_montant.fevrier = 0
			new_montant.mars = 0
			new_montant.avril = 0
			new_montant.mai = 0
			new_montant.juin = 0
			new_montant.juillet = m
			new_montant.aout = 0
			new_montant.septemre = 0
			new_montant.octobre = 0
			new_montant.novembre = 0
			new_montant.decembre = 0
		elif new_montant.type_decoupage == "AU": 
			new_montant.janvier = 0
			new_montant.fevrier = 0
			new_montant.mars = 0
			new_montant.avril = 0
			new_montant.mai = 0
			new_montant.juin = 0
			new_montant.juillet = 0
			new_montant.aout = 0
			new_montant.septemre = 0
			new_montant.octobre = 0
			new_montant.novembre = 0
			new_montant.decembre = 0

		if request.user.user_type==6:
			new_montant.vld_mens_cadre = True
			new_montant.validation_mens = "CADRE"

		if request.user.user_type==5:
			new_montant.vld_mens_chef_dep = True
			new_montant.validation_mens = "CHEFD"

		if request.user.user_type==4:
			new_montant.vld_mens_sous_dir = True
			new_montant.validation_mens = "SOUSD"				
		
		new_montant.mens_done = True
		new_montant.save()
		messages.success(request, "done successfuly." )
	# Redirecter vers chaque chapitre
		if unite_compte.compte.chapitre.code_num== 1:
			return redirect("/notif/mens/unite/offre/update_montant/"+ str(new_montant.id)+"")
			# /notif/mens/unite/recettes/update_montant/1
		elif unite_compte.compte.chapitre.code_num== 2:
			return redirect("/notif/mens/unite/traffic/update_montant/"+ str(new_montant.id)+"")
		elif unite_compte.compte.chapitre.code_num== 3:
			return redirect("/notif/mens/unite/ca_emmission/update_montant/"+ str(new_montant.id)+"")
		elif unite_compte.compte.chapitre.code_num== 4:
			return redirect("/notif/mens/unite/ca_transport/update_montant/"+ str(new_montant.id)+"")
		elif unite_compte.compte.chapitre.code_num== 5:
			return redirect("/notif/mens/unite/recettes/update_montant/"+ str(new_montant.id)+"")
		elif unite_compte.compte.chapitre.code_num== 6:
			return redirect("/notif/mens/unite/depense_fonc/update_montant/"+ str(new_montant.id)+"")
		elif unite_compte.compte.chapitre.code_num== 7:
			return redirect("/notif/mens/unite/depense_exp/update_montant/"+ str(new_montant.id)+"")
		else:
			return redirect("/notif/unites")
	
	#messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="notif/mens/add_montant.html", context={"form":form, "unite_compte":unite_compte, "budget":budget, 'montant':montant })

def update_montant_notif_m(request, id): 
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]	

	comment_form = CommentaireForm(request.POST or None)
	update_comment_form = CommentaireForm(request.POST or None, instance = montant.commentaire_mens)
	form = UpdateMontantNotifForm(request.POST or None, instance = montant)
	if form.is_valid():
		mm = form.save(commit=False)
		mens_accu = mm.janvier+mm.fevrier+mm.mars+mm.avril+mm.mai+mm.juin+mm.juillet+mm.aout+mm.septemre+mm.octobre+mm.novembre+mm.decembre
		diff = mm.montant - mens_accu
		if mm.montant == mens_accu:
			mm.save()
			messages.success(request, "Done successfuly." )
			new_montant = get_object_or_404(Compte_has_Montant, id = id)
			if request.user.user_type==6:
				new_montant.vld_mens_cadre = True
			if request.user.user_type==5:
				new_montant.vld_mens_chef_dep = True
				new_montant.validation_mens = "CHEFD"
			if request.user.user_type==4:
				new_montant.vld_mens_sous_dir = True
				new_montant.validation_mens = "SOUSD"		
			# add mens comment 
			if comment_form.is_valid():
				comment = comment_form.save(commit=False)
				comment.comment_type = "M"
				comment.user = request.user
				comment.save()
				new_montant.commentaire_mens = comment
			
			# update existed comment 
			if update_comment_form.is_valid():
				updated_comm = update_comment_form.save(commit=False)
				updated_comm.comment_type = "M"
				updated_comm.user = request.user
				updated_comm.save()
				new_montant.commentaire_mens = updated_comm

			new_montant.save()
			# Redirecter vers chaque chapitre
			if unite_compte.compte.chapitre.code_num== 1:
				return redirect("/notif/mens/unite/offre/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 2:
				return redirect("/notif/mens/unite/traffic/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 3:
				return redirect("/notif/mens/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 4:
				return redirect("/notif/mens/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 5:
				return redirect("/notif/mens/unite/recettes/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 6:
				return redirect("/notif/mens/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 7:
				return redirect("/notif/mens/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
			else:
				return redirect("/notif/unites")
		else:
			messages.error(request, "Invalid: les montants mensuel ne correspondant pas au montant Annuel (différence : " + str(diff) + " )" )




	return render (request=request, template_name="notif/mens/update_montant.html", context={"form":form, "comment_form":comment_form, "update_comment_form":update_comment_form, "unite_compte":unite_compte, "montant":montant, "budget":budget})

def valid_montant_notif_m(request, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte
	if request.user.user_type==6:
		new_montant.vld_mens_cadre = True
		new_montant.save()
	if request.user.user_type==5:
		new_montant.vld_mens_chef_dep = True
		new_montant.validation_mens = "CHEFD"
		new_montant.save()
	if request.user.user_type==4:
		new_montant.vld_mens_sous_dir = True
		new_montant.validation_mens = "SOUSD"
		new_montant.save()

	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/notif/mens/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/notif/mens/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/notif/mens/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/notif/mens/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/notif/mens/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/notif/mens/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/notif/mens/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/notif/mens/unites")

#valider tous 
def valid_tous_notif_m(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, type_maj="N", mens_done=True, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_mens_chef_dep = True
			m.validation_mens = "CHEFD"
			m.save()
		elif request.user.user_type == 4:
			m.vld_mens_sous_dir = True
			m.validation_mens = "SOUSD"
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/notif/mens/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/notif/mens/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/notif/mens/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/notif/mens/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/notif/mens/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/notif/mens/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/notif/mens/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/notif/mens/unites")

def cancel_valid_tous_notif_m(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, type_maj="N", mens_done=True, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_mens_chef_dep = False
			m.save()
		elif request.user.user_type == 4:
			m.vld_mens_sous_dir = False
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/notif/mens/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/notif/mens/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/notif/mens/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/notif/mens/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/notif/mens/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/notif/mens/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/notif/mens/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/notif/mens/unites")	

def cancel_valid_montant_notif_m(request, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte
	if request.user.user_type==6:
		new_montant.vld_mens_cadre = False
		new_montant.save()
	if request.user.user_type==5:
		new_montant.vld_mens_chef_dep = False
		new_montant.validation_mens = "CHEFD"
		new_montant.save()
	if request.user.user_type==4:
		new_montant.vld_mens_sous_dir = False
		new_montant.validation_mens = "SOUSD"
		new_montant.save()
	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/notif/mens/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/notif/mens/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/notif/mens/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/notif/mens/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/notif/mens/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/notif/mens/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/notif/mens/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/notif/mens/unites")

def delete_added_compte_notif_m(request,id):
	form = Unite_has_Compte.objects.get(id=id)
	unite = form.unite
	compte = form.compte
	form.delete()
	# Redirecter vers chaque chapitre
	if compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/notif/unite/offre/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/notif/unite/traffic/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/notif/unite/ca_emmission/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/notif/unite/ca_transport/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/notif/unite/recettes/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/notif/unite/depense_fonc/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/notif/unite/depense_exp/"+ str(unite.id)+"")
	else:
		return HttpResponseRedirect("/notif/unites")	

def add_new_compte_notif_m(request, id):
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
			return HttpResponseRedirect("/notif/unite/"+ str(unite.id)+"")
			
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="notif/add_new_compte.html", context={"form":form})

# comments
def update_comment_notif_m(request, id): 
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]
	comment = get_object_or_404(Commentaire, id = id)
	form = CommentaireForm(request.POST or None, instance = comment)
	if form.is_valid():
		form.save()
		messages.success(request, "Commentaire updated successfuly." )
		return redirect("/notif/unites")

	return render (request=request, template_name="notif/mens/update_comment.html", context={"form":form, "comment":comment, "budget":budget})

def delete_comment_notif_m(request, id):
    form = Commentaire.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/notif/unites")

# -------------------------------------- Fin Notif budget --------------------------------------------------------



# Réalisation budget  (Balance Comptable) --------------------------------------------------------------------

# affichage des unites et leur comptes par chapitre

def unites_realisation(request):
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]
	dep_unites = Unite.objects.filter(departement=request.user.departement)
	all_unites = Unite.objects.all()

	# montant total consolidé of unite --------
	total_unite_dic = {}
	bdg_total = 0
	state_cadre_dic = {}
	state_chef_dic = {}
	pr_dic = {}
	for u in all_unites:
		# calculer le montant
		total = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire=budget).aggregate(Sum('montant'))
		total_unite_dic[u.id] = total['montant__sum']
		if total['montant__sum'] != None:
			bdg_total = bdg_total + total['montant__sum']

		# get state of unite (Terminé , En cours, ...)
		comptes_nbr = Unite_has_Compte.objects.filter(unite=u).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget).count()
		comptes_done = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget)		
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=u, annee_budgetaire = budget, vld_chef_dep=True).count()
		
		# needed status comptes_valid
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr

		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic[u.id]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False :
			state_chef = "Instance"
		elif comptes_v and comptes_s :
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic[u.id]= state_chef

		# porcentage de saiser pour l unite
		if comptes_nbr == 0:
			pr = 0
		else :
			pr = int(math.modf((comptes_done_nbr / comptes_nbr)*100)[1])						
		pr_dic[u.id] = pr
	#------------------------------------------

	return render(request,"realisation/unites.html", {'unites':unites, 'dep_unites':dep_unites, 'budget':budget, 'total_unite_dic':total_unite_dic, 'bdg_total':bdg_total,
														'state_cadre_dic':state_cadre_dic, 'state_chef_dic':state_chef_dic, 'pr_dic':pr_dic })

def unite_detail_realisation(request, id):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id)
	comptes_nbr = Unite_has_Compte.objects.filter(unite=unite).count()
	comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget).count()
	comptes_vld_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True).count()	
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
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=1).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=4).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=7).count()
	# nombre de comptes Validé par chef dep
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()
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

	return render(request,"realisation/unite_detail.html", {'unite':unite, 'comptes_nbr':comptes_nbr, 'comptes_done_nbr':comptes_done_nbr, 'pr_cdr':pr_cdr, 'pr_vcd':pr_vcd, 'budget':budget,
															'offre_s':offre_s, 'traffic_s':traffic_s, 'ca_emmission_s':ca_emmission_s, 'ca_transport_s':ca_transport_s,
															'recettes_s':recettes_s, 'depense_fonc_s':depense_fonc_s, 'depense_exp_s':depense_exp_s,
															'offre_v':offre_v, 'traffic_v':traffic_v, 'ca_emmission_v':ca_emmission_v, 'ca_transport_v':ca_transport_v,
															'recettes_v':recettes_v, 'depense_fonc_v':depense_fonc_v, 'depense_exp_v':depense_exp_v,
															'offre_non_s':offre_non_s, 'traffic_non_s':traffic_non_s, 'ca_emmission_non_s':ca_emmission_non_s, 'ca_transport_non_s':ca_transport_non_s,
															'recettes_non_s':recettes_non_s, 'depense_fonc_non_s':depense_fonc_non_s, 'depense_exp_non_s':depense_exp_non_s,
															'offre_non_v':offre_non_v, 'traffic_non_v':traffic_non_v, 'ca_emmission_non_v':ca_emmission_non_v, 'ca_transport_non_v':ca_transport_non_v,
															'recettes_non_v':recettes_non_v, 'depense_fonc_non_v':depense_fonc_non_v, 'depense_exp_non_v':depense_exp_non_v
															})

def offre_comptes_realisation(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=1)

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
	offre_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=1).count()
	offre_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=1).count()
	
	c_s = offre_nbr==offre_done_nbr
	c_non_s = offre_done_nbr == 0
	c_v = offre_nbr==offre_valid_nbr

	return render(request,"realisation/offre_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict,
															"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre })

def traffic_comptes_realisation(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=2)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=2)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	traffic_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=2).count()
	traffic_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=2).count()
	traffic_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=2).count()

	c_s = traffic_nbr==traffic_done_nbr
	c_non_s = traffic_done_nbr == 0
	c_v = traffic_nbr==traffic_valid_nbr

	return render(request,"realisation/traffic_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict,
																"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre  })

def ca_emmission_comptes_realisation(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=3)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=3)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	ca_emmission_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=3).count()
	ca_emmission_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=3).count()
	ca_emmission_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=3).count()
	
	c_s = ca_emmission_nbr==ca_emmission_done_nbr
	c_non_s = ca_emmission_done_nbr == 0
	c_v = ca_emmission_nbr==ca_emmission_valid_nbr

	return render(request,"realisation/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict,
																	"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre  })

def ca_transport_comptes_realisation(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=4)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=4).order_by('-reseau_compte')
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	ca_transport_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=4).count()
	ca_transport_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=4).count()
	ca_transport_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=4).count()

	c_s = ca_transport_nbr==ca_transport_done_nbr
	c_non_s = ca_transport_done_nbr == 0
	c_v = ca_transport_nbr==ca_transport_valid_nbr

	return render(request,"realisation/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict, 
																	"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre })

def recettes_comptes_realisation(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=5)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=5)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
	
	recettes_nbr = Unite_has_Compte.objects.filter(unite=unite,compte__chapitre__code_num=5).count()
	recettes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=5).count()
	recettes_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=5).count()

	c_s = recettes_nbr==recettes_done_nbr
	c_non_s = recettes_done_nbr == 0
	c_v = recettes_nbr==recettes_valid_nbr

	return render(request,"realisation/recettes_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict, 
																"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre })

def depense_fonc_comptes_realisation(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=6)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
		
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
	
	# clacule les pos 2 saisier state 
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		
		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False:
			state_chef = "Instance"
		elif comptes_v and comptes_s:
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

	# comptes par autre -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6, compte__ref__ref__ref=c2).count()
		comptes_nbr = comptes_all_nbr - comptes_unite_nbr

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()
		comptes_done_nbr = done_all_nbr - done_par_unite_nbr

		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=6).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		
		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False:
			state_chef = "Instance"
		elif comptes_v and comptes_s:
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef
	# ------------------------------------



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
	depense_fonc_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=6).count()
	depense_fonc_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=6).count()


	c_s = depense_fonc_nbr==depense_fonc_done_nbr
	c_non_s = depense_fonc_done_nbr == 0
	c_v = depense_fonc_nbr==depense_fonc_valid_nbr

	return render(request,"realisation/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes, 'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																  "c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre, 'budget':budget,
																  "c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																  'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																  'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre })

def depense_exp_comptes_realisation(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]

	chapitre = Chapitre.objects.get(code_num=7)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c)
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]	
		
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

	# clacule les pos 2 saisier state 
	# comptes par unité ------------
	state_cadre_dic_par_unite = {}
	state_chef_dic_par_unite = {}
	for c2 in c2_par_unite:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		comptes_v_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		
		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_unite[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False:
			state_chef = "Instance"
		elif comptes_v and comptes_s:
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_unite[c2.numero]= state_chef

	# comptes par unité -----------
	state_cadre_dic_par_autre = {}
	state_chef_dic_par_autre = {}
	for c2 in c2_par_autre:
		comptes_unite_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, regle_par=unite, compte__ref__ref__ref=c2).count()
		comptes_all_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7, compte__ref__ref__ref=c2).count()
		comptes_nbr = comptes_all_nbr - comptes_unite_nbr

		done_par_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		done_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite,  annee_budgetaire=budget, unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()
		comptes_done_nbr = done_all_nbr - done_par_unite_nbr

		comptes_v_unite_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, unite_compte__regle_par=unite,  vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_all_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, vld_chef_dep=True,  annee_budgetaire=budget , unite_compte__compte__ref__ref__ref=c2 , unite_compte__compte__chapitre__code_num=7).count()	
		comptes_v_nbr = comptes_v_all_nbr - comptes_v_unite_nbr
		
		comptes_s = comptes_nbr == comptes_done_nbr
		comptes_non_s = comptes_done_nbr == 0
		comptes_v = comptes_nbr == comptes_v_nbr
		
		# pour le cadre
		if comptes_s and comptes_v == False: 
			state_cadre = "Terminé"
		elif comptes_s and comptes_v: 
			state_cadre = "Validé"
		elif comptes_non_s:
			state_cadre = "Non saisie"
		else:
			state_cadre = "En cours"
		state_cadre_dic_par_autre[c2.numero]= state_cadre

		# pour chef dep
		if comptes_non_s:
			state_chef = "Non saisie"
		elif comptes_s and comptes_v == False:
			state_chef = "Instance"
		elif comptes_v and comptes_s:
			state_chef = "Terminé"
		else:
			state_chef = "En cours"
		state_chef_dic_par_autre[c2.numero]= state_chef
	# ------------------------------------

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
	depense_exp_done_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, unite_compte__compte__chapitre__code_num=7).count()
	depense_exp_valid_nbr = Compte_has_Montant.objects.filter(unite_compte__unite=unite, annee_budgetaire = budget, vld_chef_dep=True, unite_compte__compte__chapitre__code_num=7).count()

	c_s = depense_exp_nbr==depense_exp_done_nbr
	c_non_s = depense_exp_done_nbr == 0
	c_v = depense_exp_nbr==depense_exp_valid_nbr

	return render(request,"realisation/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes,  'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																	"c_s":c_s, "c_non_s":c_non_s, "c_v":c_v, "chapitre":chapitre, 'budget':budget,
																	"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																	'state_cadre_dic_par_unite':state_cadre_dic_par_unite, 'state_chef_dic_par_unite':state_chef_dic_par_unite,
																	'state_cadre_dic_par_autre':state_cadre_dic_par_autre, 'state_chef_dic_par_autre':state_chef_dic_par_autre})

# add montant to compte 
def add_montant_realisation(request, id):
	unite_compte = Unite_has_Compte.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]

	comment_form = CommentaireForm(request.POST or None)
	montant_form = MontantOnlyForm(request.POST or None)
	if request.method == "POST":
		if  montant_form.is_valid():
			montant_compte = montant_form.save(commit=False)
			montant_compte.unite_compte = unite_compte
			montant_compte.type_bdg = "RELS"
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
				return redirect("/realisation/unite/offre/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 2:
				return redirect("/realisation/unite/traffic/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 3:
				return redirect("/realisation/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 4:
				return redirect("/realisation/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 5:
				return redirect("/realisation/unite/recettes/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 6:
				return redirect("/realisation/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 7:
				return redirect("/realisation/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
			else:
				return redirect("/realisation/unites")
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="realisation/add_montant.html", context={"montant_form":montant_form, "comment_form":comment_form, "unite_compte":unite_compte, "budget":budget})

def update_montant_realisation(request, id): 
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]	
	form = MontantOnlyForm(request.POST or None, instance = montant)
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
			return redirect("/realisation/unite/offre/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 2:
			return redirect("/realisation/unite/traffic/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 3:
			return redirect("/realisation/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 4:
			return redirect("/realisation/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 5:
			return redirect("/realisation/unite/recettes/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 6:
			return redirect("/realisation/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 7:
			return redirect("/realisation/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
		else:
			return redirect("/realisation/unites")
	return render (request=request, template_name="realisation/update_montant.html", context={"form":form, "unite_compte":unite_compte, "montant":montant, "budget":budget})

def valid_montant_realisation(request, id):
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
		return HttpResponseRedirect("/realisation/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/realisation/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/realisation/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/realisation/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/realisation/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/realisation/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/realisation/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/realisation/unites")

def cancel_valid_montant_realisation(request, id):
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
		return HttpResponseRedirect("/realisation/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/realisation/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/realisation/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/realisation/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/realisation/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/realisation/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/realisation/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/realisation/unites")

def add_new_compte_realisation(request, id):
	unite = Unite.objects.get(id=id)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]
	form = AddCompteUniteForm(request.POST or None)
	if request.method == "POST":
		if  form.is_valid():
			compte_unite = form.save(commit=False)
			compte_unite.unite = unite
			compte_unite.added_by = request.user
			compte_unite.code = compte_unite.unite.code_alpha + str(compte_unite.compte.numero) + compte_unite.regle_par.code_alpha + compte_unite.reseau_compte
			compte_unite.save()
			messages.success(request, "compte added successfuly." )
			return HttpResponseRedirect("/realisation/unite/"+ str(unite.id)+"")
			
		messages.error(request, "Unsuccessful . Invalid information.")
	return render (request=request, template_name="realisation/add_new_compte.html", context={"form":form, "budget":budget, "unite":unite})

def delete_added_compte_realisation(request,id):
	form = Unite_has_Compte.objects.get(id=id)
	unite = form.unite
	compte = form.compte
	form.delete()
	# Redirecter vers chaque chapitre
	if compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/realisation/unite/offre/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/realisation/unite/traffic/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/realisation/unite/ca_emmission/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/realisation/unite/ca_transport/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/realisation/unite/recettes/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/realisation/unite/depense_fonc/"+ str(unite.id)+"")
	elif compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/realisation/unite/depense_exp/"+ str(unite.id)+"")
	else:
		return HttpResponseRedirect("/realisation/unites")	

#valider tous 
def valid_tous_realisation(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_chef_dep = True
			m.validation = "CHEFD"
			m.save()
		elif request.user.user_type == 4:
			m.vld_sous_dir = True
			m.validation = "SOUSD"
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/realisation/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/realisation/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/realisation/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/realisation/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/realisation/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/realisation/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/realisation/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/realisation/unites")

def cancel_valid_tous_realisation(request, id_unite, ch_num):
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')
	budget = all_budgets[0]

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_chef_dep = False
			m.save()
		elif request.user.user_type == 4:
			m.vld_sous_dir = False
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/realisation/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/realisation/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/realisation/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/realisation/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/realisation/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/realisation/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/realisation/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/realisation/unites")	

# comments
def update_comment_realisation(request, id): 
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS", lancement=True, cloture=False).order_by('-annee')
	budget = all_budgets[0]
	comment = get_object_or_404(Commentaire, id = id)
	form = CommentaireForm(request.POST or None, instance = comment)
	if form.is_valid():
		form.save()
		messages.success(request, "Commentaire updated successfuly." )
		return redirect("/realisation/unites")

	return render (request=request, template_name="realisation/update_comment.html", context={"form":form, "comment":comment, "budget":budget})

def delete_comment_realisation(request, id):
    form = Commentaire.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/realisation/unites")

# -------------------------------------- Fin Réalisation budget --------------------------------------------------------


# Actualisation et réajustement  -------------------------------------------------------------------------------------

def unites_actualis(request):
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	dep_unites = Unite.objects.filter(departement=request.user.departement)
	all_unites = Unite.objects.all()
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	
	budget_1 = all_budgets[0]
	budget_2 = all_budgets[1]

	# check all_budgets length
	# montants where budget = budget1 for all unites and vld mens sdir
	# all comptes of all unites
	# all_comptes = Unite_has_Compte.objects.filter().count()
	# all_montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget).count()
	# all_montants >= all_comptes (valid mens)


	edition_budget_1 = {}
	state_sdir_budget_1 = {}
	state_cadre_budget_1 = {}
	state_chef_budget_1 = {}

	edition_budget_2 = {}
	state_sdir_budget_2 = {}
	state_cadre_budget_2 = {}
	state_chef_budget_2 = {}

	for u in all_unites:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=u).count()
		# budget 2 (N) 2022 -----------------------------------------------------------------------	
		montants_2 = Compte_has_Montant.objects.filter(annee_budgetaire=budget_2, unite_compte__unite=u, mens_done=True).order_by('-edition_budget')
		montants_nbr_2 = len(montants_2)
		#edited_montants -----------------
		edited_montants_2 = []
		for em in montants_2:
			if em.edition != em.edition_v:
				edited_montants_2.append(em)
		#----------------------------------
		edited_montants_nbr_2 = len(edited_montants_2)
		montants_valid_sdir_2 = 0
		montants_valid_chef_2 = 0
		montants_valid_2 = 0
		for em in edited_montants_2:
			if em.vld_mens_sous_dir :
				montants_valid_sdir_2 = montants_valid_sdir_2 + 1
			if em.vld_mens_chef_dep :
				montants_valid_chef_2 = montants_valid_chef_2 + 1 
			if em.vld_mens_sous_dir or em.vld_mens_chef_dep :
				montants_valid_2 = montants_valid_2 + 1

		# edition 2 ---------------------------------
		if len(montants_2) > 0:
			m = montants_2[0]
			edition_budget_2[u.id] = m.edition_budget
		else:
			edition_budget_2[u.id] = 0
		# ------------------------------------------

		#sdir state
		if montants_nbr_2 == comptes_nbr: 
			state_sdir="-"
		elif edited_montants_nbr_2 == montants_valid_chef_2 and edited_montants_nbr_2 != montants_valid_sdir_2  :
			state_sdir="Instance"
		elif edited_montants_nbr_2 == montants_valid_sdir_2 and edited_montants_nbr_2 > 0 : 
			state_sdir="Terminé"
		elif edited_montants_nbr_2 == 0 and montants_nbr_2 != comptes_nbr: 
			state_sdir="Validé"
		else:
			state_sdir="En cours"
		state_sdir_budget_2[u.id] = state_sdir
		
		#cadre state
		if montants_nbr_2 == comptes_nbr : 
			state_cadre="-"
		elif edited_montants_nbr_2 == montants_valid_2: 
			state_cadre="Validé"
		else : 
			state_cadre="En cours"
		state_cadre_budget_2[u.id] = state_cadre
		
		#chef state
		if montants_nbr_2 == comptes_nbr : 
			state_chef = "-"
		elif edited_montants_nbr_2 != montants_valid_2 and  edited_montants_nbr_2 != montants_valid_sdir_2:
			state_chef="Instance"
		elif edited_montants_nbr_2 == montants_valid_sdir_2:
			state_chef="Validé"
		elif edited_montants_nbr_2 == montants_valid_2 and edited_montants_nbr_2 != montants_valid_sdir_2:		
			state_chef="Terminé"

		state_chef_budget_2[u.id] = state_chef
		# ---------------------------------------------------------------------------------------------------------
		
		# # budget 1 (N) 2023 -------------------------------------------------------------------------------------
		montants_1 = Compte_has_Montant.objects.filter(annee_budgetaire=budget_1, unite_compte__unite=u, mens_done=True).order_by('-edition_budget')
		montants_nbr_1 = len(montants_1)
		#edited_montants -----------------
		edited_montants_1 = []
		for em in montants_1:
			if em.edition != em.edition_v:
				edited_montants_1.append(em)
		#----------------------------------
		edited_montants_nbr_1 = len(edited_montants_1)
		montants_valid_sdir_1 = 0
		montants_valid_chef_1 = 0
		montants_valid_1 = 0
		for em in edited_montants_1:
			if em.vld_mens_sous_dir :
				montants_valid_sdir_1 = montants_valid_sdir_1 + 1
			if em.vld_mens_chef_dep :
				montants_valid_chef_1 = montants_valid_chef_1 + 1 
			if em.vld_mens_sous_dir or em.vld_mens_chef_dep :
				montants_valid_1 = montants_valid_1 + 1

		# edition 1 ---------------------------------
		if len(montants_1) > 0:
			m1 = montants_1[0]
			edition_budget_1[u.id] = m1.edition_budget
		else:
			edition_budget_1[u.id] = 0
		# ------------------------------------------

		#sdir state 1
		if montants_nbr_1 == comptes_nbr: 
			state_sdir_1="-"
		elif edited_montants_nbr_1 == montants_valid_chef_1 and edited_montants_nbr_1 != montants_valid_sdir_1  :
			state_sdir_1="Instance"
		elif edited_montants_nbr_1 == montants_valid_sdir_1 and edited_montants_nbr_1 > 0 : 
			state_sdir_1="Terminé"
		elif edited_montants_nbr_1 == 0 and montants_nbr_1 != comptes_nbr: 
			state_sdir_1="Validé"
		else:
			state_sdir_1="En cours"
		state_sdir_budget_1[u.id] = state_sdir_1
		
		#cadre state
		if montants_nbr_1 == comptes_nbr : 
			state_cadre_1="-"
		elif edited_montants_nbr_1 == montants_valid_1: 
			state_cadre_1="Validé"
		else : 
			state_cadre_1="En cours"
		state_cadre_budget_1[u.id] = state_cadre_1
		
		#chef state
		if montants_nbr_1 == comptes_nbr : 
			state_chef_1 = "-"
		elif edited_montants_nbr_1 != montants_valid_1 and  edited_montants_nbr_1 != montants_valid_sdir_1:
			state_chef_1="Instance"
		elif edited_montants_nbr_1 == montants_valid_sdir_1:
			state_chef_1="Validé"
		elif edited_montants_nbr_1 == montants_valid_1 and edited_montants_nbr_1 != montants_valid_sdir_1:		
			state_chef_1="Terminé"

		state_chef_budget_1[u.id] = state_chef_1
		# --------------------------------------------------------------------------------------------------------------
		


	return render(request,"actualis/unites.html", {'unites':unites, 'dep_unites':dep_unites, 'all_unites':all_unites, 'budget_1':budget_1, 'budget_2':budget_2,
													'edition_budget_2':edition_budget_2, 'edition_budget_1':edition_budget_1,
													'state_cadre_budget_2':state_cadre_budget_2, 'state_chef_budget_2':state_chef_budget_2, 'state_sdir_budget_2':state_sdir_budget_2,
													'state_cadre_budget_1':state_cadre_budget_1, 'state_chef_budget_1':state_chef_budget_1, 'state_sdir_budget_1':state_sdir_budget_1 })

# get the chapter satatus and modifs
def get_chapitre_status(ch_num, budget, unite):
	montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite, mens_done=True , unite_compte__compte__chapitre__code_num= ch_num).order_by('edition_budget')
	edited_montants = []
	# get edited montants
	for em in montants:
		if em.edition != em.edition_v:
			edited_montants.append(em)
	# indicateurs to check status 
	edited_montants_nbr = len(edited_montants)
	montants_valid_sdir = 0
	montants_valid_chef = 0
	montants_valid = 0
	for em in edited_montants:
		if em.vld_mens_sous_dir :
			montants_valid_sdir = montants_valid_sdir + 1
		if em.vld_mens_chef_dep :
			montants_valid_chef = montants_valid_chef + 1 
		if em.vld_mens_sous_dir or em.vld_mens_chef_dep :
			montants_valid = montants_valid + 1	
	# states
	result_status = {}
	modifs_nbr = edited_montants_nbr
	state_cadre = ""
	state_chef = ""
	state_sdir = ""

	# cadre state
	if edited_montants_nbr == 0:
		state_cadre = "-"
	elif edited_montants_nbr == montants_valid:
		state_cadre = "Validé"
	else:
		state_cadre = "En cours"
	# chef state
	if edited_montants_nbr == 0:
		state_chef = "-"
	elif edited_montants_nbr == montants_valid and edited_montants_nbr != montants_valid_sdir:
		state_chef = "Terminé"
	elif edited_montants_nbr == montants_valid and edited_montants_nbr == montants_valid_sdir:
		state_chef = "Validé"
	elif edited_montants_nbr != montants_valid:
		state_chef = "Instance"
	else:
		state_chef = ""

	# sdir state
	if edited_montants_nbr == 0:
		state_sdir = "-"
	elif edited_montants_nbr == montants_valid and edited_montants_nbr != montants_valid_sdir:
		state_sdir = "Instance"
	elif edited_montants_nbr == montants_valid and edited_montants_nbr == montants_valid_sdir:
		state_sdir = "Terminé"
	else:
		state_sdir = "En cours"
	
	# dict result 
	result_status["modifs"] = modifs_nbr
	result_status["cadre"] = state_cadre
	result_status["chef"] = state_chef
	result_status["sdir"] = state_sdir

	return result_status

def unite_detail_actualis(request, id_ann, id):
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	unite = Unite.objects.get(id=id)
	all_montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite, mens_done=True).order_by('edition_budget')

	if len(all_montants) > 0:
		m1 = all_montants[0]
		edition = m1.edition_budget
	else:
		edition = 0


	off_status = get_chapitre_status(1, budget, unite)
	trf_status = get_chapitre_status(2, budget, unite)
	cae_status = get_chapitre_status(3, budget, unite)
	cat_status = get_chapitre_status(4, budget, unite)
	rct_status = get_chapitre_status(5, budget, unite)
	dpf_status = get_chapitre_status(6, budget, unite)
	dpe_status = get_chapitre_status(7, budget, unite)

	print("------------------------------------")
	print(off_status)

	return render(request,"actualis/unite_detail.html", {'unite':unite, 'budget':budget, 'edition':edition,
														'off_status':off_status, 'trf_status':trf_status, 'cae_status':cae_status, 'cat_status':cat_status, 'rct_status':rct_status,
														'dpf_status':dpf_status, 'dpe_status':dpe_status })

#valid_edition_actualis
def valid_edition_actualis(request, id_ann, id):
	unite = get_object_or_404(Unite, id = id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite)
	for m in montants:
		m.edition_budget = m.edition_budget + 1
		if m.edition != m.edition_v:
			m.edition_v = m.edition

		m.save()


	return HttpResponseRedirect("/actualis/unites")

def offre_comptes_actualis(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	# chapitre (offre)
	chapitre = Chapitre.objects.get(code_num=1)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]			

	ch_status = get_chapitre_status(chapitre.code_num, budget, unite)
	modifs = ch_status["modifs"] > 0
	valid_sdir = ch_status["sdir"] == "Terminé"
	valid_chef = ch_status["chef"] == "Terminé"

	print("valid chef dep -----------------")
	print(valid_chef)

	return render(request,"actualis/offre_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
														'ch_status':ch_status, 'modifs':modifs, 'valid_sdir':valid_sdir, 'valid_chef':valid_chef  })

def traffic_comptes_actualis(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	chapitre = Chapitre.objects.get(code_num=2)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	ch_status = get_chapitre_status(chapitre.code_num, budget, unite)
	modifs = ch_status["modifs"] > 0
	valid_sdir = ch_status["sdir"] == "Terminé"
	valid_chef = ch_status["chef"] == "Terminé"

	return render(request,"actualis/traffic_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
															'ch_status':ch_status, 'modifs':modifs, 'valid_sdir':valid_sdir, 'valid_chef':valid_chef })

def ca_emmission_comptes_actualis(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	chapitre = Chapitre.objects.get(code_num=3)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	ch_status = get_chapitre_status(chapitre.code_num, budget, unite)
	modifs = ch_status["modifs"] > 0
	valid_sdir = ch_status["sdir"] == "Terminé"
	valid_chef = ch_status["chef"] == "Terminé"

	return render(request,"actualis/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
														 		'ch_status':ch_status, 'modifs':modifs, 'valid_sdir':valid_sdir, 'valid_chef':valid_chef })

def ca_transport_comptes_actualis(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	chapitre = Chapitre.objects.get(code_num=4)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num).order_by('-reseau_compte')
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	ch_status = get_chapitre_status(chapitre.code_num, budget, unite)
	modifs = ch_status["modifs"] > 0
	valid_sdir = ch_status["sdir"] == "Terminé"
	valid_chef = ch_status["chef"] == "Terminé"	

	return render(request,"actualis/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
																'ch_status':ch_status, 'modifs':modifs, 'valid_sdir':valid_sdir, 'valid_chef':valid_chef })

def recettes_comptes_actualis(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	chapitre = Chapitre.objects.get(code_num=5)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	ch_status = get_chapitre_status(chapitre.code_num, budget, unite)
	modifs = ch_status["modifs"] > 0
	valid_sdir = ch_status["sdir"] == "Terminé"
	valid_chef = ch_status["chef"] == "Terminé"

	return render(request,"actualis/recettes_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict, 'chapitre':chapitre,
															'ch_status':ch_status, 'modifs':modifs, 'valid_sdir':valid_sdir, 'valid_chef':valid_chef })

def depense_fonc_comptes_actualis(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	chapitre = Chapitre.objects.get(code_num=6)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]			

	# ---------- status détailleé---------
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=6)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)

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

	ch_status = get_chapitre_status(chapitre.code_num, budget, unite)
	modifs = ch_status["modifs"] > 0
	valid_sdir = ch_status["sdir"] == "Terminé"
	valid_chef = ch_status["chef"] == "Terminé"

	

	return render(request,"actualis/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes, 'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																'budget':budget, 'chapitre':chapitre,
																"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																'ch_status':ch_status, 'modifs':modifs, 'valid_sdir':valid_sdir, 'valid_chef':valid_chef
																})

def depense_exp_comptes_actualis(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	chapitre = Chapitre.objects.get(code_num=7)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	# ---- status detailleé -------------------------------
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=7)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)

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

	ch_status = get_chapitre_status(chapitre.code_num, budget, unite)
	modifs = ch_status["modifs"] > 0
	valid_sdir = ch_status["sdir"] == "Terminé"
	valid_chef = ch_status["chef"] == "Terminé"

	return render(request,"actualis/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes,  'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																	'budget':budget, 'chapitre':chapitre,
																	"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																	'ch_status':ch_status, 'modifs':modifs, 'valid_sdir':valid_sdir, 'valid_chef':valid_chef
																	})

# add montant to compte 
def add_montant_actualis(request, id_ann, id):
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte

	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	new_edition = montant.edition + 1

	# create a new edition of same compte
	actualised_montant = Compte_has_Montant(
		code = montant.code + str(new_edition) ,
		unite_compte = montant.unite_compte ,
		type_bdg = montant.type_bdg ,
		annee_budgetaire = montant.annee_budgetaire ,
		janvier = montant.janvier ,
		fevrier = montant.fevrier ,
		mars = montant.mars ,
		avril = montant.avril ,
		mai = montant.mai ,
		juin = montant.juin ,
		juillet = montant.juillet ,
		aout = montant.aout ,
		septemre = montant.septemre ,
		octobre = montant.octobre ,
		novembre = montant.novembre ,
		decembre = montant.decembre ,
		type_decoupage = montant.type_decoupage,
		edition = new_edition ,
		edition_v = montant.edition_v ,
		edition_budget = montant.edition_budget  ,
		type_maj = "A",
		montant_cadre = montant.montant_cadre,
		montant = montant.montant ,
		montant_chef_dep = montant.montant_chef_dep ,
		montant_sous_dir = montant.montant_sous_dir ,
		vld_cadre = True ,
		vld_chef_dep = True ,
		vld_sous_dir = True , 
		validation = montant.validation ,
		mens_done = True ,
	)

	actualised_montant.save()

	if request.user.user_type==6:
		actualised_montant.vld_mens_cadre = True
		actualised_montant.validation_mens = "CADRE"

	if request.user.user_type==5:
		actualised_montant.vld_mens_chef_dep = True
		actualised_montant.validation_mens = "CHEFD"

	if request.user.user_type==4:
		actualised_montant.vld_mens_sous_dir = True
		actualised_montant.validation_mens = "SOUSD"

	actualised_montant.save()

	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num == 1:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/offre/update_montant/"+ str(actualised_montant.id)+"")
		# /notif/mens/unite/recettes/update_montant/1
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/traffic/update_montant/"+ str(actualised_montant.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_emmission/update_montant/"+ str(actualised_montant.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_transport/update_montant/"+ str(actualised_montant.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/recettes/update_montant/"+ str(actualised_montant.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_fonc/update_montant/"+ str(actualised_montant.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_exp/update_montant/"+ str(actualised_montant.id)+"")
	else:
		return HttpResponseRedirect("/actualis/unites")
	
	#messages.error(request, "Unsuccessful . Invalid information.")
	#return render (request=request, template_name="actualis/add_montant.html", context={"unite_compte":unite_compte, "budget":budget })

def update_montant_actualis(request, id_ann, id): 
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	comment_form = CommentaireForm(request.POST or None)
	update_comment_form = CommentaireForm(request.POST or None, instance = montant.commentaire_mens)
	form = ActualisMontantNotifForm(request.POST or None, instance = montant)
	if form.is_valid():
		mm = form.save(commit=False)
		mens_accu = mm.janvier+mm.fevrier+mm.mars+mm.avril+mm.mai+mm.juin+mm.juillet+mm.aout+mm.septemre+mm.octobre+mm.novembre+mm.decembre
		diff = mm.montant - mens_accu
		if mm.montant == mens_accu:
			mm.save()
			messages.success(request, "Mis à jour avec succés." )
			new_montant = get_object_or_404(Compte_has_Montant, id = id)
			if request.user.user_type==6:
				new_montant.vld_mens_cadre = True
			if request.user.user_type==5:
				new_montant.vld_mens_chef_dep = True
				new_montant.validation_mens = "CHEFD"
			if request.user.user_type==4:
				new_montant.vld_mens_sous_dir = True
				new_montant.validation_mens = "SOUSD"		
			# add mens comment 
			if comment_form.is_valid():
				comment = comment_form.save(commit=False)
				comment.comment_type = "M"
				comment.user = request.user
				comment.save()
				new_montant.commentaire_mens = comment
			
			# update existed comment 
			if update_comment_form.is_valid():
				updated_comm = update_comment_form.save(commit=False)
				updated_comm.comment_type = "M"
				updated_comm.user = request.user
				updated_comm.save()
				new_montant.commentaire_mens = updated_comm

			new_montant.save()

			# Redirecter vers chaque chapitre
			if unite_compte.compte.chapitre.code_num== 1:
				return redirect("/actualis/"+ str(id_ann)+ "/unite/offre/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 2:
				return redirect("/actualis/"+ str(id_ann)+ "/unite/traffic/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 3:
				return redirect("/actualis/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 4:
				return redirect("/actualis/"+ str(id_ann)+ "/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 5:
				return redirect("/actualis/"+ str(id_ann)+ "/unite/recettes/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 6:
				return redirect("/actualis/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 7:
				return redirect("/actualis/"+ str(id_ann)+ "/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
			else:
				return redirect("/actualis/unites")
		else:
			messages.error(request, "Invalid: les montants mensuel ne correspondant pas au montant Annuel (différence : " + str(diff) + " )" )


	return render (request=request, template_name="actualis/update_montant.html", context={"form":form, "comment_form":comment_form, "update_comment_form":update_comment_form, "unite_compte":unite_compte, "montant":montant, "budget":budget})

def valid_montant_actualis(request, id_ann, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte
	if request.user.user_type==6:
		new_montant.vld_mens_cadre = True
		new_montant.save()
	if request.user.user_type==5:
		new_montant.vld_mens_chef_dep = True
		new_montant.validation_mens = "CHEFD"
		new_montant.save()
	if request.user.user_type==4:
		new_montant.vld_mens_sous_dir = True
		new_montant.validation_mens = "SOUSD"
		new_montant.save()

	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/actualis/unites")

#valider tous 
def valid_tous_actualis(request, id_ann, id_unite, ch_num):
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, mens_done=True, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_mens_chef_dep = True
			m.validation_mens = "CHEFD"
			m.save()
		elif request.user.user_type == 4:
			m.vld_mens_sous_dir = True
			m.validation_mens = "SOUSD"
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/actualis/unites")

def cancel_valid_tous_actualis(request, id_ann, id_unite, ch_num):
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, mens_done=True, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_mens_chef_dep = False
			m.save()
		elif request.user.user_type == 4:
			m.vld_mens_sous_dir = False
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/actualis/unites")	

def cancel_valid_montant_actualis(request,id_ann, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte
	if request.user.user_type==6:
		new_montant.vld_mens_cadre = False
		new_montant.save()
	if request.user.user_type==5:
		new_montant.vld_mens_chef_dep = False
		new_montant.validation_mens = "CHEFD"
		new_montant.save()
	if request.user.user_type==4:
		new_montant.vld_mens_sous_dir = False
		new_montant.validation_mens = "SOUSD"
		new_montant.save()
	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/actualis/"+ str(id_ann)+ "/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/actualis/unites")

# comments
def update_comment_actualis(request, id_ann, id): 
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF", lancement=True, cloture=False).order_by('-annee')
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	comment = get_object_or_404(Commentaire, id = id)
	form = CommentaireForm(request.POST or None, instance = comment)
	if form.is_valid():
		form.save()
		messages.success(request, "Commentaire updated successfuly." )
		return redirect("/actualis/unites")

	return render (request=request, template_name="actualis/update_comment.html", context={"form":form, "comment":comment, "budget":budget})

def delete_comment_actualis(request, id):
    form = Commentaire.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/actualis/unites")


# ----------------------------- Fin Actualisation et réajustement  -------------------------------------------------------------------------------------


# Control et suivi budget -------------------------------------------------------------------------------------

months =  [
	(1, 'Janvier'),
	(2, 'Février'),
	(3, 'Mars'),
	(4, 'Avril'),
	(5, 'Mai'),
	(6, 'Juin'),
	(7, 'Juilet'),
	(8, 'Aout'),
	(9, 'Septembre'),
	(10, 'Octobre'),
	(11, 'Novembre'),
	(12, 'Décembre'),
]

def unites_controle(request):
	unites = Cadre_has_Unite.objects.filter(cadre=request.user)
	all_budgets = Annee_Budgetaire.objects.filter(type_bdg="CTRL").order_by('-annee')
	
	budget_1 = all_budgets[0]
	budget_2 = all_budgets[1]


	dep_unites = Unite.objects.filter(departement=request.user.departement)
	all_unites = Unite.objects.all()

	edition_budget_1 = {}
	state_sdir_budget_1 = {}
	state_cadre_budget_1 = {}
	state_chef_budget_1 = {}

	edition_budget_2 = {}
	state_sdir_budget_2 = {}
	state_cadre_budget_2 = {}
	state_chef_budget_2 = {}

	for u in all_unites:
		comptes_nbr = Unite_has_Compte.objects.filter(unite=u).count()
		# budget 2 (N) 2022 -----------------------------------------------------------------------	
		montants_2 = Compte_has_Montant.objects.filter(annee_budgetaire=budget_2, unite_compte__unite=u, mens_done=True).order_by('-edition_budget')
		montants_nbr_2 = len(montants_2)
		#edited_montants -----------------
		edited_montants_2 = []
		for em in montants_2:
			if em.edition != em.edition_v:
				edited_montants_2.append(em)
		#----------------------------------
		edited_montants_nbr_2 = len(edited_montants_2)
		montants_valid_sdir_2 = 0
		montants_valid_chef_2 = 0
		montants_valid_2 = 0
		for em in edited_montants_2:
			if em.vld_mens_sous_dir :
				montants_valid_sdir_2 = montants_valid_sdir_2 + 1
			if em.vld_mens_chef_dep :
				montants_valid_chef_2 = montants_valid_chef_2 + 1 
			if em.vld_mens_sous_dir or em.vld_mens_chef_dep :
				montants_valid_2 = montants_valid_2 + 1

		# edition 2 ---------------------------------
		if len(montants_2) > 0:
			m = montants_2[0]
			edition_budget_2[u.id] = m.edition_budget
		else:
			edition_budget_2[u.id] = 0
		# ------------------------------------------

		#sdir state
		if montants_nbr_2 == comptes_nbr: 
			state_sdir="-"
		elif edited_montants_nbr_2 == montants_valid_chef_2 and edited_montants_nbr_2 != montants_valid_sdir_2  :
			state_sdir="Instance"
		elif edited_montants_nbr_2 == montants_valid_sdir_2 and edited_montants_nbr_2 > 0 : 
			state_sdir="Terminé"
		elif edited_montants_nbr_2 == 0 and montants_nbr_2 != comptes_nbr: 
			state_sdir="Validé"
		else:
			state_sdir="En cours"
		state_sdir_budget_2[u.id] = state_sdir
		
		#cadre state
		if montants_nbr_2 == comptes_nbr : 
			state_cadre="-"
		elif edited_montants_nbr_2 == montants_valid_2: 
			state_cadre="Validé"
		else : 
			state_cadre="En cours"
		state_cadre_budget_2[u.id] = state_cadre
		
		#chef state
		if montants_nbr_2 == comptes_nbr : 
			state_chef = "-"
		elif edited_montants_nbr_2 != montants_valid_2 and  edited_montants_nbr_2 != montants_valid_sdir_2:
			state_chef="Instance"
		elif edited_montants_nbr_2 == montants_valid_sdir_2:
			state_chef="Validé"
		elif edited_montants_nbr_2 == montants_valid_2 and edited_montants_nbr_2 != montants_valid_sdir_2:		
			state_chef="Terminé"

		state_chef_budget_2[u.id] = state_chef
		# ---------------------------------------------------------------------------------------------------------
		
		# # budget 1 (N) 2023 -------------------------------------------------------------------------------------
		montants_1 = Compte_has_Montant.objects.filter(annee_budgetaire=budget_1, unite_compte__unite=u, mens_done=True).order_by('-edition_budget')
		montants_nbr_1 = len(montants_1)
		#edited_montants -----------------
		edited_montants_1 = []
		for em in montants_1:
			if em.edition != em.edition_v:
				edited_montants_1.append(em)
		#----------------------------------
		edited_montants_nbr_1 = len(edited_montants_1)
		montants_valid_sdir_1 = 0
		montants_valid_chef_1 = 0
		montants_valid_1 = 0
		for em in edited_montants_1:
			if em.vld_mens_sous_dir :
				montants_valid_sdir_1 = montants_valid_sdir_1 + 1
			if em.vld_mens_chef_dep :
				montants_valid_chef_1 = montants_valid_chef_1 + 1 
			if em.vld_mens_sous_dir or em.vld_mens_chef_dep :
				montants_valid_1 = montants_valid_1 + 1

		# edition 1 ---------------------------------
		if len(montants_1) > 0:
			m1 = montants_1[0]
			edition_budget_1[u.id] = m1.edition_budget
		else:
			edition_budget_1[u.id] = 0
		# ------------------------------------------

		#sdir state 1
		if montants_nbr_1 == comptes_nbr: 
			state_sdir_1="-"
		elif edited_montants_nbr_1 == montants_valid_chef_1 and edited_montants_nbr_1 != montants_valid_sdir_1  :
			state_sdir_1="Instance"
		elif edited_montants_nbr_1 == montants_valid_sdir_1 and edited_montants_nbr_1 > 0 : 
			state_sdir_1="Terminé"
		elif edited_montants_nbr_1 == 0 and montants_nbr_1 != comptes_nbr: 
			state_sdir_1="Validé"
		else:
			state_sdir_1="En cours"
		state_sdir_budget_1[u.id] = state_sdir_1
		
		#cadre state
		if montants_nbr_1 == comptes_nbr : 
			state_cadre_1="-"
		elif edited_montants_nbr_1 == montants_valid_1: 
			state_cadre_1="Validé"
		else : 
			state_cadre_1="En cours"
		state_cadre_budget_1[u.id] = state_cadre_1
		
		#chef state
		if montants_nbr_1 == comptes_nbr : 
			state_chef_1 = "-"
		elif edited_montants_nbr_1 != montants_valid_1 and  edited_montants_nbr_1 != montants_valid_sdir_1:
			state_chef_1="Instance"
		elif edited_montants_nbr_1 == montants_valid_sdir_1:
			state_chef_1="Validé"
		elif edited_montants_nbr_1 == montants_valid_1 and edited_montants_nbr_1 != montants_valid_sdir_1:		
			state_chef_1="Terminé"

		state_chef_budget_1[u.id] = state_chef_1
		# --------------------------------------------------------------------------------------------------------------
		


	return render(request,"controle/unites.html", {'unites':unites, 'dep_unites':dep_unites, 'all_unites':all_unites, 'budget_1':budget_1, 'budget_2':budget_2,
													'edition_budget_2':edition_budget_2, 'edition_budget_1':edition_budget_1,
													'state_cadre_budget_2':state_cadre_budget_2, 'state_chef_budget_2':state_chef_budget_2, 'state_sdir_budget_2':state_sdir_budget_2,
													'state_cadre_budget_1':state_cadre_budget_1, 'state_chef_budget_1':state_chef_budget_1, 'state_sdir_budget_1':state_sdir_budget_1 })

# get the chapter satatus and modifs
def get_chapitre_status_by_month(ch_num, id_month, budget, unite):
	montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite, unite_compte__compte__chapitre__code_num= ch_num)
	comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num= ch_num ).count()
	m_done = 0
	m_vld = 0
	for mm in montants:
		if mm.vld_controle_chef_dep >= id_month:
				m_vld = m_vld + 1

		if id_month == 1:
			if mm.janvier != None:
				m_done = m_done + 1
		elif id_month == 2:
			if mm.fevrier != None:
				m_done = m_done + 1
		elif id_month == 3:
			if mm.mars != None:
				m_done = m_done + 1
		elif id_month == 4:
			if mm.avril != None:
				m_done = m_done + 1
		elif id_month == 5:
			if mm.mai != None:
				m_done = m_done + 1
		elif id_month == 6:
			if mm.juin != None:
				m_done = m_done + 1
		elif id_month == 7:
			if mm.juillet != None:
				m_done = m_done + 1
		elif id_month == 8:
			if mm.aout != None:
				m_done = m_done + 1
		elif id_month == 9:
			if mm.septemre != None:
				m_done = m_done + 1
		elif id_month == 10:
			if mm.octobre != None:
				m_done = m_done + 1
		elif id_month == 11:
			if mm.novembre != None:
				m_done = m_done + 1
		elif id_month == 12:
			if mm.decembre != None:
				m_done = m_done + 1
	
	result_status = {}
	state_cadre = ""
	state_chef = ""
	# cadre state
	if m_done == 0:
		state_cadre = "-"
	elif m_done == comptes_nbr and m_vld != comptes_nbr:
		state_cadre = "Terminé"
	elif m_vld == comptes_nbr:
		state_cadre = "Validé"
	else:
		state_cadre = "En cours"
	
	# chef state
	if m_done == 0:
		state_chef = "-"
	elif m_done == comptes_nbr and m_vld != comptes_nbr:
		state_chef = "Instance"
	elif m_done == comptes_nbr and m_vld == comptes_nbr:
		state_chef = "Terminé"
	else:
		state_chef = "En cours"	

	
	# dict result 

	result_status["cadre"] = state_cadre
	result_status["chef"] = state_chef


	return result_status

def unite_detail_controle(request, id_ann, id):
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	unite = Unite.objects.get(id=id)
	all_montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite, mens_done=True).order_by('edition_budget')

	# check current month
	def is_month_done(ch_num, id_month):
		montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite, unite_compte__compte__chapitre__code_num= ch_num)
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num= ch_num ).count()
		m_done = 0
		m_vld = 0
		for mm in montants:
				if mm.vld_controle_chef_dep >= id_month:
						m_vld = m_vld + 1

				if id_month == 1:
					if mm.janvier != None:
						m_done = m_done + 1
				elif id_month == 2:
					if mm.fevrier != None:
						m_done = m_done + 1
				elif id_month == 3:
					if mm.mars != None:
						m_done = m_done + 1
				elif id_month == 4:
					if mm.avril != None:
						m_done = m_done + 1
				elif id_month == 5:
					if mm.mai != None:
						m_done = m_done + 1
				elif id_month == 6:
					if mm.juin != None:
						m_done = m_done + 1
				elif id_month == 7:
					if mm.juillet != None:
						m_done = m_done + 1
				elif id_month == 8:
					if mm.aout != None:
						m_done = m_done + 1
				elif id_month == 9:
					if mm.septemre != None:
						m_done = m_done + 1
				elif id_month == 10:
					if mm.octobre != None:
						m_done = m_done + 1
				elif id_month == 11:
					if mm.novembre != None:
						m_done = m_done + 1
				elif id_month == 12:
					if mm.decembre != None:
						m_done = m_done + 1
			
		return m_done == comptes_nbr

	def is_month_begin(ch_num, id_month):
		montants = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte__unite=unite, unite_compte__compte__chapitre__code_num= ch_num)
		comptes_nbr = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num= ch_num ).count()
		m_done = 0
		m_vld = 0
		for mm in montants:
			if mm.vld_controle_chef_dep >= id_month:
					m_vld = m_vld + 1

			if id_month == 1:
				if mm.janvier != None:
					m_done = m_done + 1
			elif id_month == 2:
				if mm.fevrier != None:
					m_done = m_done + 1
			elif id_month == 3:
				if mm.mars != None:
					m_done = m_done + 1
			elif id_month == 4:
				if mm.avril != None:
					m_done = m_done + 1
			elif id_month == 5:
				if mm.mai != None:
					m_done = m_done + 1
			elif id_month == 6:
				if mm.juin != None:
					m_done = m_done + 1
			elif id_month == 7:
				if mm.juillet != None:
					m_done = m_done + 1
			elif id_month == 8:
				if mm.aout != None:
					m_done = m_done + 1
			elif id_month == 9:
				if mm.septemre != None:
					m_done = m_done + 1
			elif id_month == 10:
				if mm.octobre != None:
					m_done = m_done + 1
			elif id_month == 11:
				if mm.novembre != None:
					m_done = m_done + 1
			elif id_month == 12:
				if mm.decembre != None:
					m_done = m_done + 1
			
		return m_done > 0

	def get_current_month(ch_num):
		month = {}
		month["month"] = "Janvier"
		month["id"] = 1
		for (id_m,m) in months:
			if is_month_begin(ch_num, id_m) :
				month["month"] = m
				month["id"] = id_m
		return month

	def get_current_done_month(ch_num):
		month = {}
		month["month"] = "J"
		month["id"] = 1
		for (id_m,m) in months:
			if is_month_done(ch_num, id_m) :
				month["month"] = m
				month["id"] = id_m
		return month

	# current month
	off_month = get_current_month(1)
	trf_month = get_current_month(2)
	cae_month = get_current_month(3)
	cat_month = get_current_month(4)
	rct_month = get_current_month(5)
	dpf_month = get_current_month(6)
	dpe_month = get_current_month(7)
	# currnet done month
	off_month_done = get_current_done_month(1)
	trf_month_done = get_current_done_month(2)
	cae_month_done = get_current_done_month(3)
	cat_month_done = get_current_done_month(4)
	rct_month_done = get_current_done_month(5)
	dpf_month_done = get_current_done_month(6)
	dpe_month_done = get_current_done_month(7)

	# check status 
	ch_status = {}
	off_status = {}
	trf_status = {}
	cae_status = {}
	cat_status = {}
	rct_status = {}
	dpf_status = {}
	dpe_status = {}

	for (id_m,m) in months:
		#ch_status[id_m] = get_chapitre_status_by_month(chapitre.code_num, id_m, budget, unite)
		off_status[id_m] = get_chapitre_status_by_month(1, id_m, budget, unite)
	for (id_m,m) in months:	
		trf_status[id_m] = get_chapitre_status_by_month(2, id_m, budget, unite)
	for (id_m,m) in months:
		cae_status[id_m] = get_chapitre_status_by_month(3, id_m, budget, unite)
	for (id_m,m) in months:
		cat_status[id_m] = get_chapitre_status_by_month(4, id_m, budget, unite)
	for (id_m,m) in months:
		rct_status[id_m] = get_chapitre_status_by_month(5, id_m, budget, unite)
	for (id_m,m) in months:
		dpf_status[id_m] = get_chapitre_status_by_month(6, id_m, budget, unite)
	for (id_m,m) in months:
		dpe_status[id_m] = get_chapitre_status_by_month(7, id_m, budget, unite)
	# ------------------

	print("--------- off status---------------------------")
	print(off_month)

	return render(request,"controle/unite_detail.html", {'unite':unite, 'budget':budget,
														'off_status':off_status, 'trf_status':trf_status, 'cae_status':cae_status, 'cat_status':cat_status, 'rct_status':rct_status,
														'dpf_status':dpf_status, 'dpe_status':dpe_status,
														'off_month':off_month, 'trf_month':trf_month, 'cae_month':cae_month, 'cat_month':cat_month, 'rct_month':rct_month,
														'dpf_month':dpf_month, 'dpe_month':dpe_month,
														'off_month_done':off_month_done, 'trf_month_done':trf_month_done, 'cae_month_done':cae_month_done, 'cat_month_done':cat_month_done, 'rct_month_done':rct_month_done,
														'dpf_month_done':dpf_month_done, 'dpe_month_done':dpe_month_done, })

def offre_comptes_controle(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	chapitre = Chapitre.objects.get(code_num=1)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]			

	# check status 
	ch_status = {}
	for (id_m,m) in months:
		ch_status[id_m] = get_chapitre_status_by_month(chapitre.code_num, id_m, budget, unite)
	# ------------------

	print("status month  -----------------")
	print(ch_status)

	return render(request,"controle/offre_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre, 
														'ch_status':ch_status, 'months':months  })

def traffic_comptes_controle(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	chapitre = Chapitre.objects.get(code_num=2)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	# check status 
	ch_status = {}
	for (id_m,m) in months:
		ch_status[id_m] = get_chapitre_status_by_month(chapitre.code_num, id_m, budget, unite)
	# ------------------

	return render(request,"controle/traffic_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
															'ch_status':ch_status , 'months':months})

def ca_emmission_comptes_controle(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	chapitre = Chapitre.objects.get(code_num=3)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	# check status 
	ch_status = {}
	for (id_m,m) in months:
		ch_status[id_m] = get_chapitre_status_by_month(chapitre.code_num, id_m, budget, unite)
	# ------------------

	return render(request,"controle/ca_emmission_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
														 		'ch_status':ch_status, 'months':months })

def ca_transport_comptes_controle(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	chapitre = Chapitre.objects.get(code_num=4)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num).order_by('-reseau_compte')
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	# check status 
	ch_status = {}
	for (id_m,m) in months:
		ch_status[id_m] = get_chapitre_status_by_month(chapitre.code_num, id_m, budget, unite)
	# ------------------

	return render(request,"controle/ca_transport_comptes.html", {'unite':unite, 'comptes':comptes, 'cm_dict':cm_dict, 'budget':budget, 'chapitre':chapitre,
																'ch_status':ch_status, 'months':months})

def recettes_comptes_controle(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	chapitre = Chapitre.objects.get(code_num=5)
	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	# check status 
	ch_status = {}
	for (id_m,m) in months:
		ch_status[id_m] = get_chapitre_status_by_month(chapitre.code_num, id_m, budget, unite)
	# ------------------

	return render(request,"controle/recettes_comptes.html", {'unite':unite, 'comptes':comptes, 'budget':budget, 'cm_dict':cm_dict, 'chapitre':chapitre,
															'ch_status':ch_status , 'months':months})

def depense_fonc_comptes_controle(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	chapitre = Chapitre.objects.get(code_num=6)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]			

	# ---------- status détailleé---------
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=6)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)

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

	# check status 
	ch_status = {}
	for (id_m,m) in months:
		ch_status[id_m] = get_chapitre_status_by_month(chapitre.code_num, id_m, budget, unite)
	# ------------------

	

	return render(request,"controle/depense_fonc_comptes.html", {'unite':unite, 'comptes':comptes, 'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																'budget':budget, 'chapitre':chapitre,
																"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																'ch_status':ch_status, 'months':months
																})

def depense_exp_comptes_controle(request, id_ann, id):
	unite = Unite.objects.get(id=id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	chapitre = Chapitre.objects.get(code_num=7)

	comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)
	# join comptes with montants in dict
	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]		

	# ---- status detailleé -------------------------------
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=7)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)

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

	# check status 
	ch_status = {}
	for (id_m,m) in months:
		ch_status[id_m] = get_chapitre_status_by_month(chapitre.code_num, id_m, budget, unite)
	# ------------------

	return render(request,"controle/depense_exp_comptes.html", {'unite':unite, 'comptes':comptes,  'comptes_regle_par_unite':comptes_regle_par_unite, 'comptes_regle_par_autre':comptes_regle_par_autre,
																	'budget':budget, 'chapitre':chapitre,
																	"c2_par_unite":c2_par_unite, "c2_par_autre":c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre, 'cm_dict':cm_dict,
																	'ch_status':ch_status, 'months':months
																	})

# add montant to compte 
def add_montant_controle(request, id_ann, id_month, id):
	unite_compte = get_object_or_404(Unite_has_Compte, id = id)
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	m_preves_list = Compte_has_Montant.objects.filter(unite_compte=unite_compte, annee_budgetaire__annee=budget.annee, annee_budgetaire__type_bdg="NOTIF").order_by('-edition')
	
	preves_ann = "null"
	preves_mens = "null"
	if len(m_preves_list) == 0:
		montant_preves = "null"
		preves_ann = "null"
		preves_mens = "null"
	else : 
		montant_preves = m_preves_list[0]
		preves_ann = montant_preves.montant
		if id_month == 1:
			preves_mens = montant_preves.janvier
		elif id_month == 2:
			preves_mens = montant_preves.fevrier
		elif id_month == 3:
			preves_mens = montant_preves.mars
		elif id_month == 4:
			preves_mens = montant_preves.avril
		elif id_month == 5:
			preves_mens = montant_preves.mai
		elif id_month == 6:
			preves_mens = montant_preves.juin
		elif id_month == 7:
			preves_mens = montant_preves.juillet
		elif id_month == 8:
			preves_mens = montant_preves.aout
		elif id_month == 9:
			preves_mens = montant_preves.septemre
		elif id_month == 10:
			preves_mens = montant_preves.octobre
		elif id_month == 11:
			preves_mens = montant_preves.novembre
		elif id_month == 12:
			preves_mens = montant_preves.decembre


	comment_form = CommentaireForm(request.POST or None)
	montant_form = MontantOnlyForm(request.POST or None)
	if request.method == "POST":
		if  montant_form.is_valid():
			montant_compte = montant_form.save(commit=False)
			montant_compte.unite_compte = unite_compte
			montant_compte.type_bdg = "CTRL"
			montant_compte.annee_budgetaire = budget
			montant_compte.code = str(montant_compte.unite_compte.id) + montant_compte.annee_budgetaire.code + montant_compte.unite_compte.monnaie.code_alpha + montant_compte.unite_compte.regle_par.code_alpha + str(montant_compte.edition)
			if comment_form.is_valid():
				comment = comment_form.save(commit=False)
				comment.comment_type = "M"
				comment.user = request.user
				comment.save()
				montant_compte.commentaire_montant = comment
			# set month value 
			if id_month == 1:
				montant_compte.janvier = montant_compte.montant
			elif id_month == 2:
				montant_compte.fevrier = montant_compte.montant
			elif id_month == 3:
				montant_compte.mars = montant_compte.montant
			elif id_month == 4:
				montant_compte.avril = montant_compte.montant
			elif id_month == 5:
				montant_compte.mai = montant_compte.montant
			elif id_month == 6:
				montant_compte.juin = montant_compte.montant
			elif id_month == 7:
				montant_compte.juillet = montant_compte.montant
			elif id_month == 8:
				montant_compte.aout = montant_compte.montant
			elif id_month == 9:
				montant_compte.septemre = montant_compte.montant
			elif id_month == 10:
				montant_compte.octobre = montant_compte.montant
			elif id_month == 11:
				montant_compte.novembre = montant_compte.montant
			elif id_month == 12:
				montant_compte.decembre = montant_compte.montant
			else:
				messages.error(request, " Invalid informations " )

			# initial validations 
			if request.user.user_type==6:
				montant_compte.vld_cadre = True
				montant_compte.validation = "CADRE"

			if request.user.user_type==5:
				montant_compte.vld_chef_dep = True
				montant_compte.vld_controle_chef_dep = id_month
				montant_compte.validation = "CHEFD"
			
			if request.user.user_type==4:
				montant_compte.vld_sous_dir = True
				montant_compte.vld_controle_sous_dir = id_month
				montant_compte.validation = "SOUSD"				
			
			montant_compte.save()
			messages.success(request, " Montant saisié avec succes " )

		# Redirecter vers chaque chapitre
			if unite_compte.compte.chapitre.code_num== 1:
				return redirect("/controle/"+ str(id_ann)+ "/unite/offre/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 2:
				return redirect("/controle/"+ str(id_ann)+ "/unite/traffic/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 3:
				return redirect("/controle/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 4:
				return redirect("/controle/"+ str(id_ann)+ "/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 5:
				return redirect("/controle/"+ str(id_ann)+ "/unite/recettes/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 6:
				return redirect("/controle/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
			elif unite_compte.compte.chapitre.code_num== 7:
				return redirect("/controle/"+ str(id_ann)+ "/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
			else:
				return redirect("/controle/unites")
		messages.error(request, "Unsuccessful . Invalid information.")

	
	return render (request=request, template_name="controle/add_montant.html", context={"unite_compte":unite_compte, "budget":budget, 'montant_form':montant_form, 'comment_form':comment_form ,
																						 'id_month':id_month, 'preves_mens':preves_mens, 'preves_ann':preves_ann })

# update selon month 
def add_montant_month_controle(request, id_ann, id_month, id):
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	# prevesion 
	preves_ann = "null"
	preves_mens = "null"
	m_preves_list = Compte_has_Montant.objects.filter(unite_compte=unite_compte, annee_budgetaire__annee=budget.annee, annee_budgetaire__type_bdg="NOTIF").order_by('-edition')
	if len(m_preves_list) == 0:
		montant_preves = "null"
		preves_ann = "null"
		preves_mens = "null"
	else : 
		montant_preves = m_preves_list[0]
		preves_ann = montant_preves.montant
		if id_month == 1:
			preves_mens = montant_preves.janvier
		elif id_month == 2:
			preves_mens = montant_preves.fevrier
		elif id_month == 3:
			preves_mens = montant_preves.mars
		elif id_month == 4:
			preves_mens = montant_preves.avril
		elif id_month == 5:
			preves_mens = montant_preves.mai
		elif id_month == 6:
			preves_mens = montant_preves.juin
		elif id_month == 7:
			preves_mens = montant_preves.juillet
		elif id_month == 8:
			preves_mens = montant_preves.aout
		elif id_month == 9:
			preves_mens = montant_preves.septemre
		elif id_month == 10:
			preves_mens = montant_preves.octobre
		elif id_month == 11:
			preves_mens = montant_preves.novembre
		elif id_month == 12:
			preves_mens = montant_preves.decembre
	
	# cummulé jusqua mois m
	cummul = 0
	if True :
		if id_month == 1:
			cummul = 0
		elif id_month == 2:
			cummul = montant.janvier
		elif id_month == 3:
			cummul = montant.janvier + montant.fevrier
		elif id_month == 4:
			cummul = montant.janvier + montant.fevrier + montant.mars
		elif id_month == 5:
			cummul = montant.janvier + montant.fevrier + montant.mars + montant.avril
		elif id_month == 6:
			cummul = montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai 
		elif id_month == 7:
			cummul = montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin
		elif id_month == 8:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet)
		elif id_month == 9:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet + montant.aout)
		elif id_month == 10:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet + montant.aout + montant.septemre )
		elif id_month == 11:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet + montant.aout + montant.septemre + montant.octobre)
		elif id_month == 12:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet + montant.aout + montant.septemre + montant.octobre + montant.novembre)



	#initil montant to 0
	montant.montant = 0
	montant.save()

	update_comment_form = CommentaireForm(request.POST or None, instance = montant.commentaire_montant)
	form = MontantOnlyForm(request.POST or None, instance = montant)

	if form.is_valid():
		mm = form.save(commit=False)

		if id_month == 1:
			mm.janvier = mm.montant
		elif id_month == 2:
			mm.fevrier = mm.montant
		elif id_month == 3:
			mm.mars = mm.montant
		elif id_month == 4:
			mm.avril = mm.montant
		elif id_month == 5:
			mm.mai = mm.montant
		elif id_month == 6:
			mm.juin = mm.montant
		elif id_month == 7:
			mm.juillet = mm.montant
		elif id_month == 8:
			mm.aout = mm.montant
		elif id_month == 9:
			mm.septemre = mm.montant
		elif id_month == 10:
			mm.octobre = mm.montant
		elif id_month == 11:
			mm.novembre = mm.montant
		elif id_month == 12:
			mm.decembre = mm.montant	

		mm.montant = 0
		
		# update existed comment 
		if update_comment_form.is_valid():
			updated_comm = update_comment_form.save(commit=False)
			updated_comm.comment_type = "M"
			updated_comm.user = request.user
			updated_comm.save()
			mm.commentaire_montant = updated_comm

		mm.save()

		montant = get_object_or_404(Compte_has_Montant, id = id)

		# Redirecter vers chaque chapitre
		if unite_compte.compte.chapitre.code_num== 1:
			return redirect("/controle/"+ str(id_ann)+ "/unite/offre/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 2:
			return redirect("/controle/"+ str(id_ann)+ "/unite/traffic/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 3:
			return redirect("/controle/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 4:
			return redirect("/controle/"+ str(id_ann)+ "/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 5:
			return redirect("/controle/"+ str(id_ann)+ "/unite/recettes/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 6:
			return redirect("/controle/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 7:
			return redirect("/controle/"+ str(id_ann)+ "/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
		else:
			return redirect("/controle/unites")


	return render (request=request, template_name="controle/add_montant_month.html", context={"unite_compte":unite_compte, "budget":budget, 'montant':montant, 'update_comment_form':update_comment_form, 'form':form,
																								'id_month':id_month, 'preves_mens':preves_mens, 'preves_ann':preves_ann , 'cummul':cummul})

def update_montant_controle(request, id_ann, id_month, id): 
	montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = montant.unite_compte
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	# prevesion 
	preves_ann = "null"
	preves_mens = "null"
	m_preves_list = Compte_has_Montant.objects.filter(unite_compte=unite_compte, annee_budgetaire__annee=budget.annee, annee_budgetaire__type_bdg="NOTIF").order_by('-edition')
	if len(m_preves_list) == 0:
		montant_preves = "null"
		preves_ann = "null"
		preves_mens = "null"
	else : 
		montant_preves = m_preves_list[0]
		preves_ann = montant_preves.montant
		if id_month == 1:
			preves_mens = montant_preves.janvier
		elif id_month == 2:
			preves_mens = montant_preves.fevrier
		elif id_month == 3:
			preves_mens = montant_preves.mars
		elif id_month == 4:
			preves_mens = montant_preves.avril
		elif id_month == 5:
			preves_mens = montant_preves.mai
		elif id_month == 6:
			preves_mens = montant_preves.juin
		elif id_month == 7:
			preves_mens = montant_preves.juillet
		elif id_month == 8:
			preves_mens = montant_preves.aout
		elif id_month == 9:
			preves_mens = montant_preves.septemre
		elif id_month == 10:
			preves_mens = montant_preves.octobre
		elif id_month == 11:
			preves_mens = montant_preves.novembre
		elif id_month == 12:
			preves_mens = montant_preves.decembre
	
	# cummulé jusqua mois m
	cummul = 0
	if True :
		if id_month == 1:
			cummul = 0
		elif id_month == 2:
			cummul = montant.janvier
		elif id_month == 3:
			cummul = montant.janvier + montant.fevrier
		elif id_month == 4:
			cummul = montant.janvier + montant.fevrier + montant.mars
		elif id_month == 5:
			cummul = montant.janvier + montant.fevrier + montant.mars + montant.avril
		elif id_month == 6:
			cummul = montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai 
		elif id_month == 7:
			cummul = montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin
		elif id_month == 8:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet)
		elif id_month == 9:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet + montant.aout)
		elif id_month == 10:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet + montant.aout + montant.septemre )
		elif id_month == 11:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet + montant.aout + montant.septemre + montant.octobre)
		elif id_month == 12:
			cummul = (montant.janvier + montant.fevrier + montant.mars + montant.avril + montant.mai + montant.juin + 
					montant.juillet + montant.aout + montant.septemre + montant.octobre + montant.novembre)


	montant.montant = montant.janvier
	montant.save()

	comment_form = CommentaireForm(request.POST or None)
	update_comment_form = CommentaireForm(request.POST or None, instance = montant.commentaire_montant)
	form = MontantOnlyForm(request.POST or None, instance = montant)
	if form.is_valid():
		mm = form.save(commit=False)

		if id_month == 1:
			mm.janvier = mm.montant
		elif id_month == 2:
			mm.fevrier = mm.montant
		elif id_month == 3:
			mm.mars = mm.montant
		elif id_month == 4:
			mm.avril = mm.montant
		elif id_month == 5:
			mm.mai = mm.montant
		elif id_month == 6:
			mm.juin = mm.montant
		elif id_month == 7:
			mm.juillet = mm.montant
		elif id_month == 8:
			mm.aout = mm.montant
		elif id_month == 9:
			mm.septemre = mm.montant
		elif id_month == 10:
			mm.octobre = mm.montant
		elif id_month == 11:
			mm.novembre = mm.montant
		elif id_month == 12:
			mm.decembre = mm.montant	

		mm.montant = 0
		mm.save()
		
		messages.success(request, "Mis à jour avec succés." )
		new_montant = get_object_or_404(Compte_has_Montant, id = id)

		if request.user.user_type==6:
			new_montant.vld_cadre = True
		if request.user.user_type==5:
			new_montant.vld_chef_dep = True
			new_montant.validation = "CHEFD"
		if request.user.user_type==4:
			new_montant.vld_sous_dir = True
			new_montant.validation = "SOUSD"
					
		# add mens comment 
		if comment_form.is_valid():
			comment = comment_form.save(commit=False)
			comment.comment_type = "M"
			comment.user = request.user
			comment.save()
			new_montant.commentaire_montant = comment
		
		# update existed comment 
		if update_comment_form.is_valid():
			updated_comm = update_comment_form.save(commit=False)
			updated_comm.comment_type = "M"
			updated_comm.user = request.user
			updated_comm.save()
			new_montant.commentaire_montant = updated_comm

		new_montant.save()

		# Redirecter vers chaque chapitre
		if unite_compte.compte.chapitre.code_num== 1:
			return redirect("/controle/"+ str(id_ann)+ "/unite/offre/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 2:
			return redirect("/controle/"+ str(id_ann)+ "/unite/traffic/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 3:
			return redirect("/controle/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 4:
			return redirect("/controle/"+ str(id_ann)+ "/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 5:
			return redirect("/controle/"+ str(id_ann)+ "/unite/recettes/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 6:
			return redirect("/controle/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
		elif unite_compte.compte.chapitre.code_num== 7:
			return redirect("/actualis/"+ str(id_ann)+ "/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
		else:
			return redirect("/controle/unites")

	return render (request=request, template_name="controle/update_montant.html", context={"form":form, "comment_form":comment_form, "update_comment_form":update_comment_form,
																							"unite_compte":unite_compte, "montant":montant, "budget":budget, "id_month":id_month,
																							'preves_mens':preves_mens, 'preves_ann':preves_ann , 'cummul':cummul})

def valid_montant_controle(request, id_ann, id_month, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte

	if request.user.user_type==5:
		new_montant.vld_controle_chef_dep = id_month
		new_montant.validation = "CHEFD"
		new_montant.save()

	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/controle/unites")

#valider tous 
def valid_tous_controle(request, id_ann, id_month, id_unite, ch_num):
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_controle_chef_dep = id_month
			m.validation = "CHEFD"
			m.save()


	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/controle/unites")

def cancel_valid_tous_controle(request, id_ann, id_month, id_unite, ch_num):
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)

	unite = Unite.objects.get(id=id_unite)
	montants = Compte_has_Montant.objects.filter(unite_compte__unite = unite, annee_budgetaire=budget, unite_compte__compte__chapitre__code_num=ch_num)
	for m in montants: 
		if request.user.user_type == 5:
			m.vld_controle_chef_dep = id_month - 1
			m.validation = "CHEFD"
			m.save()

	# Redirecter vers chaque chapitre
	if ch_num == 1:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/offre/"+ str(id_unite)+"")
	elif ch_num == 2:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/traffic/"+ str(id_unite)+"")
	elif ch_num == 3:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(id_unite)+"")
	elif ch_num == 4:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/ca_transport/"+ str(id_unite)+"")
	elif ch_num == 5:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/recettes/"+ str(id_unite)+"")
	elif ch_num == 6:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(id_unite)+"")
	elif ch_num == 7:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/depense_exp/"+ str(id_unite)+"")
	else:
		return HttpResponseRedirect("/controle/unites")	

def cancel_valid_montant_controle(request, id_ann, id_month, id):
	new_montant = get_object_or_404(Compte_has_Montant, id = id)
	unite_compte = new_montant.unite_compte

	if request.user.user_type==5:
		new_montant.vld_controle_chef_dep = id_month - 1
		new_montant.validation = "CHEFD"
		new_montant.save()

	# Redirecter vers chaque chapitre
	if unite_compte.compte.chapitre.code_num== 1:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/offre/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 2:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/traffic/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 3:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/ca_emmission/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 4:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/ca_transport/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 5:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/recettes/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 6:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/depense_fonc/"+ str(unite_compte.unite.id)+"")
	elif unite_compte.compte.chapitre.code_num== 7:
		return HttpResponseRedirect("/controle/"+ str(id_ann)+ "/unite/depense_exp/"+ str(unite_compte.unite.id)+"")
	else:
		return HttpResponseRedirect("/controle/unites")

# comments
def update_comment_controle(request, id_ann, id): 
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	comment = get_object_or_404(Commentaire, id = id)
	form = CommentaireForm(request.POST or None, instance = comment)
	if form.is_valid():
		form.save()
		messages.success(request, "Commentaire updated successfuly." )
		return redirect("/controle/unites")

	return render (request=request, template_name="controle/update_comment.html", context={"form":form, "comment":comment, "budget":budget})

def delete_comment_controle(request, id):
    form = Commentaire.objects.get(id=id)
    form.delete()
    return HttpResponseRedirect("/controle/unites")


# Control et suivi budget -------------------------------------------------------------------------------------

def unites_consultation(request, id_volet):
	# get the budget type by id_volet
	if id_volet == 1:
		budgets = Annee_Budgetaire.objects.filter(type_bdg="PROPOS").order_by('-annee')
	elif id_volet == 2:	
		budgets = Annee_Budgetaire.objects.filter(type_bdg="REUN").order_by('-annee')
	elif id_volet == 3:	
		budgets = Annee_Budgetaire.objects.filter(type_bdg="NOTIF").order_by('-annee')
	elif id_volet == 4:		
		budgets = Annee_Budgetaire.objects.filter(type_bdg="CTRL").order_by('-annee')
	elif id_volet == 5:	
		budgets = Annee_Budgetaire.objects.filter(type_bdg="RELS").order_by('-annee')

	# get unites depend on user 
	if request.user.user_type == 6:
		unites = []
		unites_cadre = Cadre_has_Unite.objects.filter(cadre=request.user)
		for uc in unites_cadre:
			unites.append(uc.unite)
	elif request.user.user_type == 5: 
		unites= Unite.objects.filter(departement=request.user.departement)
	elif request.user.user_type == 4 or request.user.user_type == 3: 
		unites = Unite.objects.all()

	return render(request,"consultation/unites.html", {'unites':unites, 'budgets':budgets, 'id_volet':id_volet})

def unite_detail_consultation(request, id_volet, id_ann, id_unite):
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	unite = Unite.objects.get(id=id_unite)
	# Taux de change
	unite_monn = unite.monnaie
	tch_unite = Taux_de_change.objects.filter(monnaie=unite_monn, annee=budget.annee)
	ch_unite_val = 1
	if len(tch_unite) != 0:
		ch_unite_val = tch_unite[0].value

	chapitres = Chapitre.objects.all()
	# offre:   PAX: 8000100 -- BCB: 8000110 --  FRET: 8000120 -- POSTE: 8000130 
	# trafic:  PAX: 8000200 -- BCB: 8000210 --  FRET: 8000220 -- POSTE: 8000230 

	off_pax_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__numero=8000100)
	off_bcb_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__numero=8000110)
	off_fret_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__numero=8000120)
	off_poste_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__numero=8000130)

	trf_pax_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__numero=8000200)
	trf_bcb_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__numero=8000210)
	trf_fret_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__numero=8000220)
	trf_poste_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__numero=8000230)


	# Totale pour chaque chapitre 
	emission_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=3)
	rct_trans_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=4)
	autre_rct_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=5)
	dpns_fonc_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=6)
	dpns_exp_comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=7)
	
	off_pax_total = 0
	off_bcb_total = 0
	off_fret_total = 0
	off_poste_total = 0

	trf_pax_total = 0
	trf_bcb_total = 0
	trf_fret_total = 0
	trf_poste_total = 0

	emission_total = 0
	rct_trans_total = 0
	autre_rct_total = 0
	dpns_fonc_total = 0
	dpns_exp_total = 0

	def get_total(comptes):
		chap_id = 0
		if len(comptes) != 0:
			chap_id = comptes[0].compte.chapitre.code_num
		result=0
		#print('-------------chapitre--------------------')
		for c in comptes:
			c_monn = c.monnaie
			#print(c_monn)

			tch = Taux_de_change.objects.filter(monnaie=c_monn, annee=budget.annee)
			ch_val = 1
			if len(tch) != 0:
				ch_val = tch[0].value

			if id_volet != 4:
				# Offre et traffic aucun monnaie
				if chap_id == 1 or chap_id == 2:
					m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
					if len(m) != 0:
						montant = m[0]
						result = result + montant.montant
				# Reccetes en Dinnar
				elif chap_id == 4 or chap_id == 5:
					m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
					if len(m) != 0:
						montant = m[0]
						result = result + (montant.montant * ch_val)
				# Depenses et CA Emmission (monnaie = unite monnaie)
				elif chap_id == 6 or chap_id == 7 or chap_id == 3:
					m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
					if len(m) != 0:
						montant = m[0]
						if c_monn == unite_monn:
							result = result + montant.montant
						else:
							#montant en dinar
							dzd_m = (montant.montant * ch_val)
							# montant en unite monnaie
							result = result + (dzd_m / ch_unite_val)
						
							
		return result

	off_pax_total = int(get_total(off_pax_comptes))
	off_bcb_total = float("{:.2f}".format(get_total(off_bcb_comptes)))
	off_fret_total = float("{:.2f}".format(get_total(off_fret_comptes)))
	off_poste_total = float("{:.2f}".format(get_total(off_poste_comptes)))

	trf_pax_total = int(get_total(trf_pax_comptes))
	trf_bcb_total = float("{:.2f}".format(get_total(trf_bcb_comptes)))
	trf_fret_total = float("{:.2f}".format(get_total(trf_fret_comptes)))
	trf_poste_total = float("{:.2f}".format(get_total(trf_poste_comptes)))

	
	emission_total = int(get_total(emission_comptes))
	rct_trans_total = int(get_total(rct_trans_comptes))
	autre_rct_total = int(get_total(autre_rct_comptes))
	dpns_fonc_total = int(get_total(dpns_fonc_comptes))
	dpns_exp_total = int(get_total(dpns_exp_comptes))

	return render(request, "consultation/unite_detail.html", {'unite':unite, 'budget':budget, 'chapitres':chapitres, 'id_volet':id_volet,
															'rct_trans_total':rct_trans_total, 'autre_rct_total':autre_rct_total, 'dpns_fonc_total':dpns_fonc_total,
															'dpns_exp_total':dpns_exp_total, 'emission_total':emission_total,
															'off_pax_total':off_pax_total, 'off_bcb_total':off_bcb_total, 'off_fret_total':off_fret_total, 'off_poste_total':off_poste_total,
															'trf_pax_total':trf_pax_total, 'trf_bcb_total':trf_bcb_total, 'trf_fret_total':trf_fret_total, 'trf_poste_total':trf_poste_total, })

def chapitre_consultation(request, id_volet, id_ann, id_unite, id_chap):
	budget = get_object_or_404(Annee_Budgetaire, id = id_ann)
	unite = Unite.objects.get(id=id_unite)
	chapitre = Chapitre.objects.get(code_num=id_chap)
	if id_chap == 4:
		comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num).order_by('-reseau_compte')
	else:
		comptes = Unite_has_Compte.objects.filter(unite=unite, compte__chapitre__code_num=chapitre.code_num)


	cm_dict = {}
	for c in comptes:
		m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
		if len(m) == 0:
			cm_dict[c.id] = "null"
		else:
			cm_dict[c.id] = m[0]

	# pour les depenses 
	comptes_regle_par_unite = Unite_has_Compte.objects.filter(unite=unite, regle_par=unite, compte__chapitre__code_num=id_chap)
	comptes_regle_par_autre = comptes.difference(comptes_regle_par_unite)
	# pos 2 comptes -------------------------------------
	all_c2 = SCF_Pos_2.objects.all()
	all_c3 = SCF_Pos_3.objects.all()
	c2_par_unite = []
	c2_par_autre = []	
	c3_par_unite = []
	c3_par_autre = []

	if id_chap == 6 or id_chap == 7:
		for c2 in all_c2:
			for cu in comptes_regle_par_unite:
				if c2.numero == cu.compte.ref.ref.ref.numero:
					c2_par_unite.append(c2)

		for c2 in all_c2:
			for cu in comptes_regle_par_autre:
				if c2.numero == cu.compte.ref.ref.ref.numero:
					c2_par_autre.append(c2)
		
		for c3 in all_c3:
			for cu in comptes_regle_par_unite:
				if c3.numero == cu.compte.ref.ref.numero:
					c3_par_unite.append(c3)

		for c3 in all_c3:
			for cu in comptes_regle_par_autre:
				if c3.numero == cu.compte.ref.ref.numero:
					c3_par_autre.append(c3)
		
		c3_par_unite = list(dict.fromkeys(c3_par_unite))
		c3_par_autre = list(dict.fromkeys(c3_par_autre))
		c2_par_unite = list(dict.fromkeys(c2_par_unite))
		c2_par_autre = list(dict.fromkeys(c2_par_autre))
	# -----------------------------------------------------------
	
	s1_dict = {}
	s2_dict = {}
	total_dict = {}

	if id_volet == 3 or id_volet == 4:
		for c in comptes:
			s1 = 0
			s2 = 0
			t = s1 + s2
			all_m = Compte_has_Montant.objects.filter(annee_budgetaire=budget, unite_compte=c).order_by('-edition')
			if len(all_m) != 0:
				m = all_m[0]
				# ----- S1 ----------
				if m.janvier != None:
					s1 = s1 + m.janvier
				if m.fevrier != None:
					s1 = s1 + m.fevrier
				if m.mars != None:
					s1 = s1 + m.mars
				if m.avril != None:
					s1 = s1 + m.avril
				if m.mai != None:
					s1 = s1 + m.mai
				if m.juin != None:
					s1 = s1 + m.juin
				# ----- S2 ----------
				if m.juillet != None:
					s2 = s2 + m.juillet
				if m.aout != None:
					s2 = s2 + m.aout
				if m.septemre != None:
					s2 = s2 + m.septemre
				if m.octobre != None:
					s2 = s2 + m.octobre
				if m.novembre != None:
					s2 = s2 + m.novembre
				if m.decembre != None:
					s2 = s2 + m.decembre
				# --------------
				s1_dict[c.id] = s1
				s2_dict[c.id] = s2
				total_dict[c.id] = s1 + s2


	return render(request, "consultation/comptes.html", {'unite':unite, 'budget':budget, 'chapitre':chapitre, 'comptes':comptes, 'cm_dict':cm_dict,
														 'id_volet':id_volet, 's1_dict':s1_dict, 's2_dict':s2_dict, 'comptes_regle_par_unite':comptes_regle_par_unite,
														 'comptes_regle_par_autre':comptes_regle_par_autre,
														 'c2_par_unite':c2_par_unite, 'c2_par_autre':c2_par_autre, 'c3_par_unite':c3_par_unite, 'c3_par_autre':c3_par_autre,  'total_dict':total_dict, })




