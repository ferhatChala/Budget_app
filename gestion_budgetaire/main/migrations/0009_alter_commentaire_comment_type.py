# Generated by Django 4.0 on 2022-01-21 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_annee_budgetaire_remove_compte_has_montant_annee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='comment_type',
            field=models.CharField(choices=[('M', 'Montant'), ('C', 'Cloture')], max_length=50),
        ),
    ]
