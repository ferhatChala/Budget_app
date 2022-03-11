from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (User, Interim, Commentaire,
                    Departement, Unite, Pays, Monnaie, Taux_de_change, Chapitre,
                    SCF_Pos_1, SCF_Pos_2, SCF_Pos_3, SCF_Pos_6, SCF_Pos_7,Compte_SCF,
                    Unite_has_Compte, Compte_has_Montant, Cadre_has_Unite, Annee_Budgetaire
                    )
from django.contrib.auth import get_user_model
User = get_user_model()


# Create user and profiles forms
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("email", "password1", "password2", "nom", "prenom", 'telephone', "departement")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

# Create Unite form
class AddUniteForm(forms.ModelForm):
	class Meta:
		model = Unite
		fields = '__all__'
					
# Create Departement form
class AddDepForm(forms.ModelForm):
	class Meta:
		model = Departement
		fields = '__all__'

# Create Comptes SCF form
class AddPos1Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_1
		fields = '__all__'

class AddPos2Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_2
		fields = '__all__'

class AddPos3Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_3
		fields = '__all__'

class AddPos6Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_6
		fields = ("numero","rubrique")

class AddPos7Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_7
		fields = ("numero","rubrique","chapitre")

class CompteScfForm(forms.ModelForm):
	class Meta:
		model = Compte_SCF
		fields = ("numero" ,"rubrique" ,"ref")
		# pos doit etre rempli auto pos = numero.lenght

# annee budgétaire 
class AnneeBdgForm(forms.ModelForm):
	class Meta:
		model = Annee_Budgetaire
		fields = ("annee","type_bdg","lancement","cloture")

class UpdateAnneeBdgForm(forms.ModelForm):
	class Meta:
		model = Annee_Budgetaire
		fields = ("lancement","cloture")

# Create Monnaie form
class AddMonnaieForm(forms.ModelForm):
	class Meta:
		model = Monnaie
		fields = '__all__'

# Create Taux de change form
class AddTauxChngForm(forms.ModelForm):
	class Meta:
		model = Taux_de_change
		fields = ("annee","monnaie","value")

# Create Chapitre form
class AddChapitreForm(forms.ModelForm):
	class Meta:
		model = Chapitre
		fields = '__all__'

# Create Pays form
class AddPaysForm(forms.ModelForm):
	class Meta:
		model = Pays
		fields = '__all__'

# Affectation des cadres aux unités
class AffectCadreForm(forms.ModelForm):
	class Meta:
		model = Cadre_has_Unite
		fields = ("unite",)


# Affectation des comptes aux unités
class AddCompteUniteForm(forms.ModelForm):
	class Meta:
		model = Unite_has_Compte
		fields = ("compte","regle_par","reseau_compte","monnaie")

# add montant to compte 
class MontantCompteForm(forms.ModelForm):
	class Meta:
		model = Compte_has_Montant
		fields = ("montant","montant_cloture")

class MontantOnlyForm(forms.ModelForm):
	class Meta:
		model = Compte_has_Montant
		fields = ("montant",)

class CommentaireForm(forms.ModelForm):
	class Meta:
		model = Commentaire
		fields = ("text","importance")

class UpdateMontantCompteForm(forms.ModelForm):
	class Meta:
		model = Compte_has_Montant
		fields = ("montant","montant_cloture")

# choisi la config de découpage de bdg notifié 
class TypeDecoupeMontantForm(forms.ModelForm):
	class Meta:
		model = Compte_has_Montant
		fields = ("type_decoupage",)

class UpdateMontantNotifForm(forms.ModelForm):
	class Meta:
		model = Compte_has_Montant
		fields = ("janvier","fevrier","mars","avril","mai",
				"juin","juillet","aout","septemre","octobre","novembre","decembre")

class ActualisMontantNotifForm(forms.ModelForm):
	class Meta:
		model = Compte_has_Montant
		fields = ("montant","type_maj","janvier","fevrier","mars","avril","mai",
				"juin","juillet","aout","septemre","octobre","novembre","decembre")


class InterimForm(forms.ModelForm):
	class Meta:
		model = Interim
		fields = '__all__'

class AnneeBudgetForm(forms.ModelForm):
	class Meta:
		model = Annee_Budgetaire
		fields =  ("annee","type_bdg","lancement","cloture")






