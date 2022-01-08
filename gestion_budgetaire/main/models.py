from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser

# Costume Users

class MyUserManager(BaseUserManager):
    def create_user(self, Nom, prenom, email, telephone, adresse, user_type, password):
        """
        Creates and saves a User with the given data
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            adresse=adresse,
            telephone=telephone,
            Nom=Nom,
            prenom=prenom,
            user_type=user_type
        )

        user.set_password(password)
        user.save(using=self._db)
        print(user.email)
        return user

    def create_superuser(self, email, Nom, prenom, telephone, adresse, user_type ,password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(password=password,
                                email=self.normalize_email(email),
                                Nom=Nom,
                                prenom=prenom,
                                telephone=telephone,
                                adresse=adresse,
                                user_type=user_type,
                                )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'content_admin'),
      (2, 'sous_dir'),
      (3, 'chef_dep'),
      (4, 'cadre'),
      )

    class Meta:
        db_table = 'auth_user'

    objects = MyUserManager()
    username = None
    Nom = models.CharField(max_length=50, default="user")
    prenom = models.CharField(max_length=50, default="prenom")
    email = models.EmailField('email address', unique=True)
    telephone = models.CharField(max_length=255, default="tel")
    adresse = models.CharField(max_length=255, default="adresse")
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    #is_admin = models.BooleanField('admin status', default=False)
    #is_cadre = models.BooleanField('Cadre status', default=False)
    #is_chef_dep = models.BooleanField('Chef Departement status', default=False)
    #is_sous_dir = models.BooleanField('Sous Directeur status', default=False)
    #is_content_admin = models.BooleanField('Content admin status', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Nom', 'prenom', 'telephone', 'adresse', 'user_type']

    def __str__(self):
        return self.email

# profiles (multi roles)

class Cadre(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    departement = models.ForeignKey("Departement", on_delete=models.CASCADE)    

class Chef_Dep(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    departement = models.ForeignKey("Departement", on_delete=models.CASCADE)    

class Sous_Dir(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    
class Content_Admin(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)



# Other entities

class Departement(models.Model):
    code = models.CharField(max_length=50)
    lib = models.CharField(max_length=100)

    def __str__(self):
        return self.lib

class Unite(models.Model):
    RES_CHOICES = [
    ('FR', 'France'),
    ('EU', 'Europe'),
    ('MG', 'Maghreb et Moyen Orient'),
    ('AF', 'Afrique'),
    ('AM', 'Amérique'),
    ('AS', 'Asie'),
    ]
    REG_CHOICES = [
    ('INT', 'Internationle'),
    ('DOM', 'Domestique'),
    ]
    code_num = models.IntegerField()
    code_alpha = models.CharField(max_length=10)
    lib = models.CharField(max_length=100)
    departement = models.ForeignKey("Departement", on_delete=models.CASCADE)
    monnaie = models.ForeignKey("Monnaie", on_delete=models.CASCADE)
    pays = models.ForeignKey("Pays",  on_delete=models.CASCADE)
    reseau = models.CharField(max_length=50, choices=RES_CHOICES,default='DZ',)
    region = models.CharField(max_length=50, choices=REG_CHOICES,default='DOM',)
    comm = models.BooleanField('Commercial indicateur', default=False)
    tresorie = models.BooleanField('Tresorie indicateur', default=False)
    traffic = models.BooleanField('Traffic indicateur', default=False)
    recette = models.BooleanField('Recette indicateur', default=False)
    commerciale = models.BooleanField('Recette indicateur', default=False)
    exploitation = models.BooleanField('Exploiatation indicateur', default=False)
    regle_possible = models.BooleanField('Possibilité de reglé pour autre unité indicateur', default=False)

    def __str__(self):
        return self.code_alpha

class Pays(models.Model):
    code = models.CharField(max_length=50)
    lib = models.CharField(max_length=50)

    def __str__(self):
        return self.lib
    
class Monnaie(models.Model):
    code_num = models.IntegerField()
    code_alpha = models.CharField(max_length=50)
    lib = models.CharField(max_length=50)

    def __str__(self):
        return self.code_alpha

class Taux_de_change(models.Model):
    monnaie = models.ForeignKey("Monnaie", on_delete=models.CASCADE)
    annee = models.IntegerField() # primary key
    value = models.FloatField() # la valeur de la monnaie par rapport au Dinnar DZD

class Chapitre(models.Model):
    code_num = models.IntegerField(primary_key = True)
    lib = models.CharField(max_length=100)

    def __str__(self):
        return self.lib

# Comptes scf

class SCF_Pos_1(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=50)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class SCF_Pos_2(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=100)
    ref = models.ForeignKey("SCF_Pos_1", related_name= "next_position", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class SCF_Pos_3(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=100)
    ref = models.ForeignKey("SCF_Pos_2", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class SCF_Pos_6(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=100)
    ref = models.ForeignKey("SCF_Pos_3", on_delete=models.CASCADE)
    chapitre = models.ForeignKey("Chapitre", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class SCF_Pos_7(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=100)
    ref = models.ForeignKey("SCF_Pos_6", on_delete=models.CASCADE)
    chapitre = models.ForeignKey("Chapitre", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

# entities a rempli par users

class Unite_has_Compte(models.Model):
    RES_CHOICES = [
    ('INT', 'Internationle'),
    ('DOM', 'Domestique'),
    ]

    unite   = models.ForeignKey("Unite", related_name="unites", on_delete=models.CASCADE)
    compte  = models.ForeignKey("SCF_Pos_6", on_delete=models.CASCADE)
    chapire = models.ForeignKey("Chapitre", on_delete=models.CASCADE)
    regle_par = models.ForeignKey("Unite", related_name="unite_regle", on_delete=models.CASCADE)
    resau   = models.CharField(max_length=50, choices=RES_CHOICES)
    added_by = models.CharField(max_length=50)
    existe  = models.BooleanField()

    def __str__(self):
        return self.unite.code_alpha 
    
class Compte_has_Montant(models.Model):
    TYPBDG_CHOICES = [
    ('PROPOS', 'Budget de proposition'),
    ('REUN', 'Budget de Réunion'),
    ('NOTIF', 'Budget notifié'),
    ]
    VALID_CHOICES = [
    ('CADRE', 'Cadre Budget'),
    ('CHEFD', 'Chef Département'),
    ('SOUSD', 'Sous Directeur'),
    ]
    unite_compte = models.ForeignKey("Unite_has_Compte", on_delete=models.CASCADE)
    type_bdg = models.CharField( max_length=50,choices=TYPBDG_CHOICES)
    monnaie = models.ForeignKey("Monnaie", on_delete=models.CASCADE)
    montant = models.FloatField(default=0)
    validation = models.CharField(max_length=50,choices=VALID_CHOICES)

    #les montant pour chaque acteur
    montant_cadre  = models.FloatField(default=0)
    montant_chef_dep = models.FloatField(default=0)
    montant_sous_dir = models.FloatField(default=0)
    #la validation de chaque acteur
    vld_cadre = models.BooleanField()
    vld_chef_dep = models.BooleanField()
    vld_sous_dir = models.BooleanField()

    #ajouter commentaires avec degre d'importance (faible, moyenne, critique)
    #ajouter la valeur de cloture pour l année courant N

class Cadre_has_Unite(models.Model):
    cadre = models.ForeignKey("Cadre", on_delete=models.CASCADE)
    unite = models.ForeignKey("Unite", on_delete=models.CASCADE)