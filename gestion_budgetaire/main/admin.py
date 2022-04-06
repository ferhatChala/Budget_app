from import_export.admin import ImportExportModelAdmin
from .models import User
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import (User, Annee_Budgetaire,
                    Departement, Unite, Pays, Monnaie, Taux_de_change, Chapitre,
                    SCF_Pos_1, SCF_Pos_2, SCF_Pos_3, SCF_Pos_6, SCF_Pos_7,Compte_SCF,
                    Unite_has_Compte, Compte_has_Montant, Cadre_has_Unite,
                    Historique, Notification, Commentaire, Reception, Interim
                    )


# User Registration
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
        'nom', 'prenom', 'email', 'telephone', 'departement', 'user_type')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('nom', 'prenom', 'email', 'password', 'telephone', 'departement', 'user_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'nom', 'prenom', 'email', 'telephone', 'departement', 'user_type')
    list_filter = ('user_type',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': ('nom', 'prenom', 'telephone', 'departement')}),
        (
        'Permissions', {'fields': ('user_type',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'nom', 'prenom', 'email', 'telephone', 'user_type', 'departement',
                'password1',
                'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)

class CompteAdmin(admin.ModelAdmin):
    list_display = ('numero', 'rubrique','pos','ref')
    list_filter = ('pos',)
admin.site.register(Compte_SCF,CompteAdmin)
#---------------------------------------------------------------------------

class SCF_Pos_1_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('numero', 'rubrique')
admin.site.register(SCF_Pos_1, SCF_Pos_1_Admin)

class SCF_Pos_2_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('numero', 'rubrique','ref')
admin.site.register(SCF_Pos_2, SCF_Pos_2_Admin)

class SCF_Pos_3_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('numero', 'rubrique','ref')
admin.site.register(SCF_Pos_3, SCF_Pos_3_Admin)

class SCF_Pos_6_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('numero', 'rubrique','ref')
admin.site.register(SCF_Pos_6, SCF_Pos_6_Admin)

class SCF_Pos_7_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('numero', 'rubrique', 'chapitre')
    list_filter = ('chapitre',)
admin.site.register(SCF_Pos_7, SCF_Pos_7_Admin)

class PaysAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code_alpha_two','code_alpha_three', 'lib')
    search_fields = ['lib', 'code_alpha_two', 'id', ]
admin.site.register(Pays, PaysAdmin)

class MonnaieAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code_alpha', 'lib')
admin.site.register(Monnaie, MonnaieAdmin)

class UniteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code_alpha', 'lib', 'pays', 'reseau_unite', 'monnaie', 'traffic')
    list_filter = ('reseau_unite','traffic')
    search_fields = ['id', 'code_alpha', 'lib' ]
admin.site.register(Unite, UniteAdmin)

class DepartementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code', 'lib')
admin.site.register(Departement, DepartementAdmin)

class ChapitreAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('code_num', 'lib')
admin.site.register(Chapitre, ChapitreAdmin)

class TauxAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('annee', 'monnaie', 'value')
    list_filter = ('monnaie',)
admin.site.register(Taux_de_change, TauxAdmin)

class Annee_BudgetaireAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('annee', 'type_bdg', 'lancement', 'cloture')
    list_filter = ('type_bdg',)
admin.site.register(Annee_Budgetaire, Annee_BudgetaireAdmin)


class Unite_has_CompteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('unite', 'compte', 'reseau_compte', 'monnaie')
    list_filter = ('reseau_compte','unite',)
admin.site.register(Unite_has_Compte, Unite_has_CompteAdmin)

class Compte_has_MontantAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('unite_compte', 'annee_budgetaire', 'montant',)
    list_filter = ('annee_budgetaire',)
admin.site.register(Compte_has_Montant, Compte_has_MontantAdmin)

#admin.site.register(Departement)
#admin.site.register(Unite)
#admin.site.register(Pays)
#admin.site.register(Monnaie)
#admin.site.register(Taux_de_change)
#admin.site.register(Chapitre)

#admin.site.register(SCF_Pos_1)
#admin.site.register(SCF_Pos_2)
#admin.site.register(SCF_Pos_3)
#admin.site.register(SCF_Pos_6)
#admin.site.register(SCF_Pos_7)

#admin.site.register(Annee_Budgetaire)
#admin.site.register(Unite_has_Compte)
#admin.site.register(Compte_has_Montant)
admin.site.register(Cadre_has_Unite)

admin.site.register(Historique)
admin.site.register(Notification)
admin.site.register(Commentaire)
admin.site.register(Reception)
admin.site.register(Interim)



