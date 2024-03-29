# Generated by Django 4.0 on 2022-01-12 14:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Full Admin'), (2, 'Content Admin'), (3, 'Directeur'), (4, 'Sous Directeur'), (5, 'Chef Département'), (6, 'Cadre')])),
            ],
            options={
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='Chapitre',
            fields=[
                ('code_num', models.IntegerField(primary_key=True, serialize=False)),
                ('lib', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('importance', models.CharField(choices=[('F', 'Faible'), ('M', 'Moyenne'), ('C', 'Critique')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('lib', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Monnaie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_num', models.IntegerField()),
                ('code_alpha', models.CharField(max_length=50)),
                ('lib', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_num', models.IntegerField()),
                ('code_alpha_two', models.CharField(max_length=2)),
                ('code_alpha_three', models.CharField(max_length=3)),
                ('lib', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SCF_Pos_1',
            fields=[
                ('numero', models.IntegerField(primary_key=True, serialize=False)),
                ('rubrique', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SCF_Pos_2',
            fields=[
                ('numero', models.IntegerField(primary_key=True, serialize=False)),
                ('rubrique', models.CharField(max_length=100)),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comptes', to='main.scf_pos_1')),
            ],
        ),
        migrations.CreateModel(
            name='SCF_Pos_3',
            fields=[
                ('numero', models.IntegerField(primary_key=True, serialize=False)),
                ('rubrique', models.CharField(max_length=100)),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comptes', to='main.scf_pos_2')),
            ],
        ),
        migrations.CreateModel(
            name='SCF_Pos_6',
            fields=[
                ('numero', models.IntegerField(primary_key=True, serialize=False)),
                ('rubrique', models.CharField(max_length=100)),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comptes', to='main.scf_pos_3')),
            ],
        ),
        migrations.CreateModel(
            name='Unite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_num', models.IntegerField()),
                ('code_alpha', models.CharField(max_length=10)),
                ('lib', models.CharField(max_length=100)),
                ('reseau_unite', models.CharField(choices=[('DOM', 'Domestique'), ('FR', 'France'), ('EU', 'Europe'), ('MG', 'Maghreb et Moyen Orient'), ('AF', 'Afrique'), ('AM', 'Amérique'), ('AS', 'Asie')], default='DZ', max_length=50)),
                ('region', models.CharField(choices=[('INT', 'Internationle'), ('DOM', 'Domestique')], default='DOM', max_length=50)),
                ('comm', models.BooleanField(default=False, verbose_name='Commercial indicateur')),
                ('tresorie', models.BooleanField(default=False, verbose_name='Tresorie indicateur')),
                ('traffic', models.BooleanField(default=False, verbose_name='Traffic indicateur')),
                ('recette', models.BooleanField(default=False, verbose_name='Recette indicateur')),
                ('exploitation', models.BooleanField(default=False, verbose_name='Exploitation indicateur')),
                ('emmission', models.BooleanField(default=False, verbose_name='Emmession indicateur')),
                ('regle_possible', models.BooleanField(default=False, verbose_name='Possibilité de reglé pour autre unité indicateur')),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unites', to='main.departement')),
                ('monnaie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.monnaie')),
                ('pays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pays')),
            ],
        ),
        migrations.CreateModel(
            name='Unite_has_Compte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reseau_compte', models.CharField(choices=[('INT', 'Internationle'), ('DOM', 'Domestique'), ('ALL', 'Les deux')], max_length=50)),
                ('added_by', models.CharField(max_length=50)),
                ('existe', models.BooleanField()),
                ('chapire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ch_comptes', to='main.chapitre')),
                ('compte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unite_comptes', to='main.scf_pos_6')),
                ('regle_par', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unite_regle', to='main.unite')),
                ('unite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unites', to='main.unite')),
            ],
        ),
        migrations.CreateModel(
            name='Taux_de_change',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('annee', models.IntegerField()),
                ('value', models.FloatField()),
                ('monnaie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.monnaie')),
            ],
        ),
        migrations.CreateModel(
            name='SCF_Pos_7',
            fields=[
                ('numero', models.IntegerField(primary_key=True, serialize=False)),
                ('rubrique', models.CharField(max_length=100)),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comptes', to='main.scf_pos_6')),
            ],
        ),
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_bdg', models.CharField(choices=[('PROPOS', 'Budget de proposition'), ('REUN', 'Budget de Réunion'), ('NOTIF', 'Budget notifié')], max_length=50)),
                ('moyenne_recep', models.CharField(max_length=200)),
                ('date_recep', models.DateField()),
                ('annee', models.IntegerField()),
                ('unite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.unite')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('message', models.CharField(max_length=50)),
                ('seen', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifs', to='main.user')),
            ],
        ),
        migrations.CreateModel(
            name='Interim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_interim', models.CharField(choices=[('PIDZ', 'P/I Département Algérie'), ('PIET', 'P/I Département Etranger'), ('PISD', 'P/I Sous Directeur')], default='PIDZ', max_length=50)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interims', to='main.user')),
            ],
        ),
        migrations.CreateModel(
            name='Historique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('action', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historique', to='main.user')),
            ],
        ),
        migrations.CreateModel(
            name='Compte_SCF',
            fields=[
                ('numero', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('rubrique', models.CharField(max_length=50)),
                ('pos', models.PositiveIntegerField()),
                ('ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comptes', to='main.compte_scf')),
            ],
        ),
        migrations.CreateModel(
            name='Compte_has_Montant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_bdg', models.CharField(choices=[('PROPOS', 'Budget de proposition'), ('REUN', 'Budget de Réunion'), ('NOTIF', 'Budget notifié')], max_length=50)),
                ('annee', models.IntegerField()),
                ('montant', models.FloatField(default=0)),
                ('validation', models.CharField(choices=[('CADRE', 'Cadre Budget'), ('CHEFD', 'Chef Département'), ('CHEFDPI', 'Chef Département DZ P/I'), ('CHEFDPI', 'Chef Département ET P/I'), ('SOUSD', 'Sous Directeur'), ('SOUSDPI', 'Sous Directeur P/I')], max_length=50)),
                ('montant_cadre', models.FloatField(default=0)),
                ('montant_chef_dep', models.FloatField(default=0)),
                ('montant_sous_dir', models.FloatField(default=0)),
                ('vld_cadre', models.BooleanField()),
                ('vld_chef_dep', models.BooleanField()),
                ('vld_sous_dir', models.BooleanField()),
                ('commentaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.commentaire')),
                ('monnaie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.monnaie')),
                ('unite_compte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.unite_has_compte')),
            ],
        ),
        migrations.CreateModel(
            name='Cadre_has_Unite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cadre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user')),
                ('unite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.unite')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='departement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dep_users', to='main.departement'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
