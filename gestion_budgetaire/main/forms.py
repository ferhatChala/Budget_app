from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cadre, Chef_Dep, Sous_Dir, Content_Admin
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
# Create Comptes SCF form
# Create Departement form
# Create Monnaie form
# Create Taux de change form
# Create Chapitre form
# Create Pays form
# Affectation des cadres aux unités 
# Affectation des comptes aux unités






