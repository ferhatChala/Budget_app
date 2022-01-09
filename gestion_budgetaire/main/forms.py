from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (User, Cadre, Chef_Dep, Sous_Dir, Content_Admin,
                    Departement, Unite, Pays, Monnaie, Taux_de_change, Chapitre,
                    SCF_Pos_1, SCF_Pos_2, SCF_Pos_3, SCF_Pos_6, SCF_Pos_7,Compte_SCF,
                    Unite_has_Compte, Compte_has_Montant, Cadre_has_Unite
                    )
from django.contrib.auth import get_user_model
User = get_user_model()


# Create user and profiles forms

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("email", "password1", "password2", "Nom", "prenom", 'telephone', "adresse")

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
		fields = '__all__'

class AddPos7Form(forms.ModelForm):
	class Meta:
		model = SCF_Pos_7
		fields = '__all__'

class CompteScfForm(forms.ModelForm):
	class Meta:
		model = Compte_SCF
		fields = ("numero" ,"rubrique" ,"ref")
		# pos doit etre rempli auto pos = numero.lenght


# Create Monnaie form
class AddMonnaieForm(forms.ModelForm):
	class Meta:
		model = Monnaie
		fields = '__all__'

# Create Taux de change form
class AddTauxChngForm(forms.ModelForm):
	class Meta:
		model = Taux_de_change
		fields = '__all__'

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






