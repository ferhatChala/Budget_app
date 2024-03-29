# Generated by Django 4.0 on 2022-03-11 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_rename_commentaire_cloture_compte_has_montant_commentaire_mens_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='compte_has_montant',
            name='edition_budget',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='compte_has_montant',
            name='commentaire_mens',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mens_comm', to='main.commentaire'),
        ),
    ]
