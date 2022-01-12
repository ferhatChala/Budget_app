from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser

# Costume Users
class MyUserManager(BaseUserManager):
    def create_user(self, nom, prenom, email, user_type, password):
        """
        Creates and saves a User with the given data
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nom=nom,
            prenom=prenom,
            user_type=user_type
        )

        user.set_password(password)
        user.save(using=self._db)
        print(user.email)
        return user

    def create_superuser(self, email, nom, prenom, user_type ,password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(password=password,
                                email=self.normalize_email(email),
                                nom=nom,
                                prenom=prenom,
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
      (1, 'Full Admin'),
      (2, 'Content Admin'),
      (3, 'Directeur'),
      (4, 'Sous Directeur'),
      (5, 'Chef Département'),
      (6, 'Cadre'),
      )

    class Meta:
        db_table = 'auth_user'

    objects = MyUserManager()
    username = None
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField('email address', unique=True)
    telephone = models.CharField(max_length=255, null=True, blank=True,)
    departement = models.ForeignKey("Departement", null=True, blank=True, related_name="dep_users" , on_delete=models.CASCADE)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    #is_admin = models.BooleanField('admin status', default=False)
    #is_cadre = models.BooleanField('Cadre status', default=False)
    #is_chef_dep = models.BooleanField('Chef Departement status', default=False)
    #is_sous_dir = models.BooleanField('Sous Directeur status', default=False)
    #is_content_admin = models.BooleanField('Content admin status', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'user_type']

    def __str__(self):
        return self.email



# unite & Departement & pays & monnaie & taux de change
class Unite(models.Model):
    RES_CHOICES = [
    ('DOM', 'Domestique'),
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
    departement = models.ForeignKey("Departement", related_name="unites", on_delete=models.CASCADE)
    monnaie = models.ForeignKey("Monnaie", on_delete=models.CASCADE)
    pays = models.ForeignKey("Pays",  on_delete=models.CASCADE)
    reseau_unite = models.CharField(max_length=50, choices=RES_CHOICES,default='DZ',)
    region = models.CharField(max_length=50, choices=REG_CHOICES,default='DOM',)
    comm = models.BooleanField('Commercial indicateur', default=False)
    tresorie = models.BooleanField('Tresorie indicateur', default=False)
    traffic = models.BooleanField('Traffic indicateur', default=False)
    recette = models.BooleanField('Recette indicateur', default=False)
    exploitation = models.BooleanField('Exploitation indicateur', default=False)
    emmission = models.BooleanField('Emmession indicateur', default=False)
    regle_possible = models.BooleanField('Possibilité de reglé pour autre unité indicateur', default=False)

    def __str__(self):
        return self.code_alpha

class Departement(models.Model):
    # ALG & ETG 
    code = models.CharField(max_length=50)
    # Algérie & Etranger
    lib = models.CharField(max_length=100)

    def __str__(self):
        return self.lib

class Pays(models.Model):
    code_num = models.IntegerField()
    code_alpha_two = models.CharField(max_length=2)
    code_alpha_three = models.CharField(max_length=3)
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
    code = models.CharField(max_length=50, unique=True)
    monnaie = models.ForeignKey("Monnaie", on_delete=models.CASCADE)
    annee = models.IntegerField()
    value = models.FloatField() # la valeur de la monnaie par rapport au Dinnar DZD


# Comptes scf & Chapitre
class SCF_Pos_1(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=50)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class SCF_Pos_2(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=100)
    ref = models.ForeignKey("SCF_Pos_1", related_name= "comptes", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class SCF_Pos_3(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=100)
    ref = models.ForeignKey("SCF_Pos_2", related_name= "comptes", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class SCF_Pos_6(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=100)
    ref = models.ForeignKey("SCF_Pos_3", related_name= "comptes", on_delete=models.CASCADE) # auto / 
    #chapire = models.ForeignKey("Chapitre", on_delete=models.CASCADE)


    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class SCF_Pos_7(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=100)
    ref = models.ForeignKey("SCF_Pos_6", related_name= "comptes", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class Chapitre(models.Model):
    code_num = models.IntegerField(primary_key = True)
    lib = models.CharField(max_length=100)

    def __str__(self):
        return self.lib

# vesrion comptes one entity
class Compte_SCF(models.Model):
    numero = models.PositiveIntegerField(primary_key = True)
    rubrique = models.CharField(max_length=50)
    pos = models.PositiveIntegerField()
    ref = models.ForeignKey("Compte_SCF", null=True, blank=True, related_name="comptes" , on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique
    

# Afféctation des comptes scf 6 position pour chaque Unité
class Unite_has_Compte(models.Model):
    RES_CHOICES = [
    ('INT', 'Internationle'),
    ('DOM', 'Domestique'),
    ('ALL', 'Les deux'),
    ]


    unite   = models.ForeignKey("Unite", related_name="unites", on_delete=models.CASCADE)
    compte  = models.ForeignKey("SCF_Pos_6", related_name="unite_comptes", on_delete=models.CASCADE)
    # delete chapitre
    chapire = models.ForeignKey("Chapitre", related_name="ch_comptes" , on_delete=models.CASCADE)
    regle_par = models.ForeignKey("Unite", related_name="unite_regle", on_delete=models.CASCADE)
    reseau_compte   = models.CharField(max_length=50, choices=RES_CHOICES) # resau_compte
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
    ('CHEFDPI', 'Chef Département DZ P/I'),
    ('CHEFDPI', 'Chef Département ET P/I'),
    ('SOUSD', 'Sous Directeur'),
    ('SOUSDPI', 'Sous Directeur P/I'),
    ]

    unite_compte = models.ForeignKey("Unite_has_Compte", on_delete=models.CASCADE) # auto
    type_bdg = models.CharField( max_length=50,choices=TYPBDG_CHOICES) # auto
    monnaie = models.ForeignKey("Monnaie", on_delete=models.CASCADE) # saisier
    annee = models.IntegerField() # auto (année courant + 1)
    montant = models.FloatField(default=0) # auto (egale la dernier de valeur de user )
    validation = models.CharField(max_length=50,choices=VALID_CHOICES) # auto depend de user

    #les montant pour chaque acteur
    montant_cadre  = models.FloatField(default=0) # saiser cadre
    commentaire = models.ForeignKey("Commentaire",  on_delete=models.CASCADE)
    montant_chef_dep = models.FloatField(default=0) # saiser chef dep
    montant_sous_dir = models.FloatField(default=0) # saiser sous_sdir 
    #la validation de chaque acteur
    vld_cadre = models.BooleanField()   # auto    
    vld_chef_dep = models.BooleanField() # auto
    vld_sous_dir = models.BooleanField()  # auto
    #ajouter commentaires avec degre d'importance (faible, moyenne, critique)
    #ajouter la valeur de cloture pour l année courant N

class Cadre_has_Unite(models.Model):
    cadre = models.ForeignKey("User", on_delete=models.CASCADE)
    unite = models.ForeignKey("Unite", on_delete=models.CASCADE)


# Historique & Notification & Commentaire & Reception
class Historique(models.Model):
    user = models.ForeignKey("User", related_name="historique", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    action = models.CharField(max_length=50)

class Notification(models.Model):
    user = models.ForeignKey("User", related_name="notifs", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    message = models.CharField(max_length=50)
    seen = models.BooleanField()

class Commentaire(models.Model):
    IMPORTANCE_CHOICES = [
    ('F', 'Faible'),
    ('M', 'Moyenne'),
    ('C', 'Critique'),
    ]
    text = models.CharField(max_length=200)
    importance = models.CharField(max_length=50, choices=IMPORTANCE_CHOICES) 
    
class Reception(models.Model):
    TYPBDG_CHOICES = [
    ('PROPOS', 'Budget de proposition'),
    ('REUN', 'Budget de Réunion'),
    ('NOTIF', 'Budget notifié'),
    ]
    unite = models.ForeignKey("Unite", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    type_bdg = models.CharField( max_length=50,choices=TYPBDG_CHOICES) # auto
    moyenne_recep = models.CharField(max_length=200)
    date_recep = models.DateField(auto_now=False, auto_now_add=False)
    annee = models.IntegerField() # Anne budget N 

# Intérim 
class Interim(models.Model):
    INTERIM_CHOICES = [
    ('PIDZ', 'P/I Département Algérie'),
    ('PIET', 'P/I Département Etranger'),
    ('PISD', 'P/I Sous Directeur'),
    ]
    user = models.ForeignKey("User", related_name="interims", on_delete=models.CASCADE)
    type_interim = models.CharField(max_length=50, choices=INTERIM_CHOICES,default='PIDZ',)
    date_debut = models.DateField(auto_now=False, auto_now_add=False)
    date_fin = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.user.nom +"" + self.type_interim





