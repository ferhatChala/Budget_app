# Generated by Django 4.0 on 2022-01-17 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_interim_date_debut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interim',
            name='date_debut',
            field=models.DateField(),
        ),
    ]