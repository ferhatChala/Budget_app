from django.db import models
from django.utils import timezone
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

    id = models.IntegerField(primary_key = True) # yes 
    code_alpha = models.CharField(max_length=10) # yes
    lib = models.CharField(max_length=150) # no 
    departement = models.ForeignKey("Departement", related_name="unites", on_delete=models.CASCADE) # no
    monnaie = models.ForeignKey("Monnaie", on_delete=models.CASCADE) # yes
    pays = models.ForeignKey("Pays",  on_delete=models.CASCADE) # (yes) get id
    reseau_unite = models.CharField(max_length=50, choices=RES_CHOICES,default='DZ',) # yes (change name brk)
    region = models.CharField(max_length=50, choices=REG_CHOICES,default='DOM',) #  yes (etranger indecator)
    # indicateurs 
    comm = models.BooleanField('Commercial indicateur', default=False) # yes
    tresorie = models.BooleanField('Tresorie indicateur', default=False) # yes
    traffic = models.BooleanField('Traffic indicateur', default=False) # yes
    recette = models.BooleanField('Recette indicateur', default=False) # yes
    exploitation = models.BooleanField('Exploitation indicateur', default=False) # yes
    emmission = models.BooleanField('Emmession indicateur', default=False) # yes
    regle_possible = models.BooleanField('Possibilité de reglé pour autre unité indicateur', default=False) # no (default)

    #class Meta:
        #db_table = 'Unite'

    def __str__(self):
        return self.code_alpha

class Departement(models.Model):
    # id : 1 = ALG , 2 = etranger
    # ALG & ETG 
    code = models.CharField(max_length=50)
    # Algérie & Etranger
    lib = models.CharField(max_length=100)

    #class Meta:
        #db_table = 'Departement'

    def __str__(self):
        return self.lib

class Pays(models.Model):
    code_num = models.IntegerField()
    code_alpha_two = models.CharField(max_length=2)
    code_alpha_three = models.CharField(max_length=3)
    lib = models.CharField(max_length=50)

    #class Meta:
        #db_table = 'Pays'


    def __str__(self):
        return self.lib
    
class Monnaie(models.Model):
    id = models.IntegerField(primary_key = True) # yes
    code_alpha = models.CharField(max_length=50) # yes
    lib = models.CharField(max_length=50) # yes

    #class Meta:
        #db_table = 'Monnaie'
    def __str__(self):
        return self.code_alpha

class Taux_de_change(models.Model):
    code = models.CharField(max_length=50, unique=True)
    monnaie = models.ForeignKey("Monnaie", on_delete=models.CASCADE)
    annee = models.IntegerField()
    value = models.FloatField() # la valeur de la monnaie par rapport au Dinnar DZD
    #class Meta:
        #db_table = 'Taux_de_change'


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

    def __str__(self):
        return str(self.numero) +" - " + self.rubrique

class SCF_Pos_7(models.Model):
    numero = models.IntegerField(primary_key = True)
    rubrique = models.CharField(max_length=100)
    chapitre = models.ForeignKey("Chapitre", null=True, related_name="ch_comptes" , on_delete=models.CASCADE)
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
    ('ALL', 'All'),
    ]

    # code = unite.id-compte.numero-regle-resau
    code = models.CharField(max_length=200, unique=True)
    unite   = models.ForeignKey("Unite", related_name="unites", on_delete=models.CASCADE)
    compte  = models.ForeignKey("SCF_Pos_7", related_name="unite_comptes", on_delete=models.CASCADE)
    regle_par = models.ForeignKey("Unite", related_name="unite_regle" , null=True, blank=True, on_delete=models.SET_NULL)
    reseau_compte  = models.CharField(max_length=50, choices=RES_CHOICES, default="ALL")
    added_by = models.ForeignKey("User", null=True, blank=True, related_name="other_comptes_added", on_delete=models.CASCADE)
    monnaie = models.ForeignKey("Monnaie",  null=True, blank=True, default=1, on_delete=models.SET_NULL) #  add default

    def __str__(self):
        return self.unite.code_alpha + " - " + str(self.compte.numero) 
    
class Compte_has_Montant(models.Model):
    #decoupage choices 
    TYPDCPG_CHOICES = [
        ('MS', 'Mensuel'), # chaque mois
        ('BM', 'Bimensuel'), # chaque 2 mois start with janvier
        ('TR', 'Trimestriel'), # Janvier , Avrile, Juillet, Octobre
        ('SM', 'Semestriel'), # Janvier , Juillet
        ('AU', 'Autre'), ] # mannuelle    
 
    TYPBDG_CHOICES = [
        ('PROPOS', 'Budget de proposition'),
        ('REUN', 'Budget de Réunion'),
        ('NOTIF', 'Budget notifié'),
        ('CTRL', 'Budget de contrôle'),
        ('RELS', 'Budget réalisation'), ]
    
    VALID_CHOICES = [
        ('CADRE', 'Cadre Budget'),
        ('CHEFD', 'Chef Département'),
        ('CHEFDPI', 'Chef Département DZ P/I'),
        ('CHEFDPI', 'Chef Département ET P/I'),
        ('SOUSD', 'Sous Directeur'),
        ('SOUSDPI', 'Sous Directeur P/I'),  ]
  
    TYPMAJ_CHOICES = [
        ('A', 'Actualisation'),
        ('R', 'Réajustement'),
        ('N', 'Initial'),  ]
   
    VLD_CTRL_CHOICES = [
        (0, 'Aucun'),
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
        (12, 'Décembre') ]
    
    # code = unite_compte.id + type_bdg + annee + unite_compte.monnaie + unite_compte.regle_par + edition  (unique)
    code = models.CharField(max_length=100, unique=True)
    unite_compte = models.ForeignKey("Unite_has_Compte", related_name="montants", on_delete=models.CASCADE) # auto
    type_bdg = models.CharField( max_length=50,choices=TYPBDG_CHOICES) # auto
    annee_budgetaire = models.ForeignKey("Annee_Budgetaire", related_name="montants", on_delete=models.CASCADE) # annee n+1

    # les montant menseuiles
    janvier = models.FloatField(null=True, blank=True) 
    fevrier = models.FloatField(null=True, blank=True) 
    mars = models.FloatField(null=True, blank=True)
    avril = models.FloatField(null=True, blank=True)
    mai = models.FloatField(null=True, blank=True)
    juin = models.FloatField(null=True, blank=True)
    juillet = models.FloatField(null=True, blank=True)
    aout = models.FloatField(null=True, blank=True) 
    septemre = models.FloatField(null=True, blank=True) 
    octobre = models.FloatField(null=True, blank=True) 
    novembre = models.FloatField(null=True, blank=True) 
    decembre = models.FloatField(null=True, blank=True)
    # mois :  
    type_decoupage = models.CharField( max_length=50, null=True, blank=True, choices=TYPDCPG_CHOICES, default="MS")
    
    # Actualisation et réajustement
    edition = models.PositiveIntegerField(default=0)
    edition_v = models.PositiveIntegerField(default=0)
    edition_budget = models.PositiveIntegerField(default=0)

    type_maj = models.CharField( max_length=50, null=True, blank=True, choices=TYPMAJ_CHOICES, default="N") 
    created_date = models.DateTimeField(default=timezone.now) 

    # les montant pour chaque acteur
    montant_cadre  = models.FloatField(default=0) # 
    montant = models.FloatField(default=0) # 
    montant_cloture = models.FloatField(default=0) # a   
    montant_chef_dep = models.FloatField(default=0) #
    montant_sous_dir = models.FloatField(default=0) #  
    # commentaire 
    commentaire_montant = models.ForeignKey("Commentaire", related_name="montants_comm",  null=True, blank=True,  on_delete=models.SET_NULL)
    commentaire_mens = models.ForeignKey("Commentaire", related_name="mens_comm",  null=True, blank=True,  on_delete=models.SET_NULL) # comment mens
    #la validation de chaque acteur
    vld_cadre = models.BooleanField(default=False)   # auto    
    vld_chef_dep = models.BooleanField(default=False) # auto
    vld_sous_dir = models.BooleanField(default=False)
    validation = models.CharField(max_length=50,choices=VALID_CHOICES) # auto depend de user
    # validation Controle
    vld_controle_chef_dep = models.PositiveSmallIntegerField(choices= VLD_CTRL_CHOICES, default=0)
    # valid menseulle
    mens_done = models.BooleanField(default=False) 
    vld_mens_cadre = models.BooleanField(default=False)   # auto    
    vld_mens_chef_dep = models.BooleanField(default=False) # auto
    vld_mens_sous_dir = models.BooleanField(default=False) 
    validation_mens = models.CharField(max_length=50,choices=VALID_CHOICES, null=True, blank=True) # auto depend de user

class Cadre_has_Unite(models.Model):
    # code = cadre.id + unite.code
    code = models.CharField(max_length=50, unique=True)
    cadre = models.ForeignKey("User", on_delete=models.CASCADE)
    unite = models.ForeignKey("Unite", on_delete=models.CASCADE)
    
class Annee_Budgetaire(models.Model):
    TYPBDG_CHOICES = [
    ('PROPOS', 'Budget de proposition'),
    ('REUN', 'Budget de Réunion'),
    ('NOTIF', 'Budget notifié'),
    ('CTRL', 'Budget de contrôle'),
    ('RELS', 'Budget réalisation'),
    ]
    # code =  type + annee
    code = models.CharField(max_length=50, unique=True) 
    annee = models.IntegerField()
    type_bdg = models.CharField( max_length=50,choices=TYPBDG_CHOICES)
    lancement = models.BooleanField(default=False)
    cloture = models.BooleanField(default=False)

    def __str__(self):
        return self.type_bdg + " " + str(self.annee)
 

# Historique & Notification & Commentaire & Reception
class Historique(models.Model):
    user = models.ForeignKey("User", related_name="historique", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=50)

class Notification(models.Model):
    user = models.ForeignKey("User", related_name="notifs", on_delete=models.CASCADE) # target user
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField(max_length=50)
    seen = models.BooleanField()

class Commentaire(models.Model):
    IMPORTANCE_CHOICES = [
        ('A', 'Aucun'),
        ('F', 'Faible'),
        ('M', 'Moyenne'),
        ('C', 'Critique'),]
    TYPE_CHOICES = [
        ('M', 'Montant'),
        ('C', 'Cloture'),]
    
    text = models.CharField(max_length=300, default='-')
    importance = models.CharField(max_length=50, choices=IMPORTANCE_CHOICES , default='A') 
    comment_type = models.CharField(max_length=50, choices=TYPE_CHOICES ) 
    user = models.ForeignKey("User", related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return self.text
        
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
    date_debut = models.DateField(auto_now=False)
    date_fin = models.DateField(auto_now=False)

    def __str__(self):
        return self.user.nom +"" + self.type_interim





