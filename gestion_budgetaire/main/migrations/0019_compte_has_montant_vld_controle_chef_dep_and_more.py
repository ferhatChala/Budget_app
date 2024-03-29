# Generated by Django 4.0 on 2022-03-16 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_compte_has_montant_edition_v'),
    ]

    operations = [
        migrations.AddField(
            model_name='compte_has_montant',
            name='vld_controle_chef_dep',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Aucun'), (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'), (7, 'Juilet'), (8, 'Aout'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')], default=0),
        ),
        migrations.AddField(
            model_name='compte_has_montant',
            name='vld_controle_sous_dir',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Aucun'), (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'), (7, 'Juilet'), (8, 'Aout'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')], default=0),
        ),
    ]
