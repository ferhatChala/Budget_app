# Generated by Django 4.0 on 2022-03-20 11:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_compte_has_montant_vld_controle_chef_dep_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compte_has_montant',
            name='vld_controle_sous_dir',
        ),
        migrations.AlterField(
            model_name='compte_has_montant',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='historique',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(max_length=50),
        ),
    ]