# Generated by Django 4.0 on 2022-01-10 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_compte_scf_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte_scf',
            name='ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comptes', to='main.compte_scf'),
        ),
    ]
