from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (User, Cadre, Chef_Dep, Sous_Dir, Content_Admin,
                    Departement, Unite, Pays, Monnaie, Taux_de_change, Chapitre,
                    SCF_Pos_1, SCF_Pos_2, SCF_Pos_3, SCF_Pos_6, SCF_Pos_7,
                    Unite_has_Compte, Compte_has_Montant, Cadre_has_Unite
                    )
from django.contrib.auth import get_user_model
User = get_user_model()


# Create user and profiles forms

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("email", "password1", "password2", "Nom", "prenom", 'telephone', "adresse", "user_type")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class CadreForm(forms.ModelForm):
	class Meta:
		model = Cadre
		fields = ("departement",)

class ChefDepForm(forms.ModelForm):
	class Meta:
		model = Chef_Dep
		fields = ("departement",)

class SousDirForm(forms.ModelForm):
	class Meta:
		model = Sous_Dir
		fields = ()

class ContentAdminForm(forms.ModelForm):
	class Meta:
		model = Content_Admin
		fields = ()


# Create Unite form
class AddUniteForm(forms.ModelForm):
	class Meta:
		model = Unite
		fields = ("code_num","code_alpha","lib","departement","monnaie","pays","reseau","region",
					"comm","tresorie","traffic","recette","commerciale","exploitation","regle_possible")
					
# Create Departement form
class AddDepForm(forms.ModelForm):
	class Meta:
		model = Departement
		fields = ("code","lib")

# Create Comptes SCF form
class AddPos1Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_1
		fields = ("numero","rubrique")

class AddPos2Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_2
		fields = ("numero","rubrique","ref")

class AddPos3Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_3
		fields = ("numero","rubrique","ref")

class AddPos6Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_6
		fields = ("numero","rubrique","ref","chapitre")

class AddPos7Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_7
		fields = ("numero","rubrique","ref","chapitre")


# Create Monnaie form
# Create Taux de change form
# Create Chapitre form
# Create Pays form
# Affectation des cadres aux unités 
# Affectation des comptes aux unités






