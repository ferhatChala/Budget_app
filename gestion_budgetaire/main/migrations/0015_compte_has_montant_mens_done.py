# Generated by Django 4.0 on 2022-02-22 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_compte_has_montant_validation_mens_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='compte_has_montant',
            name='mens_done',
            field=models.BooleanField(default=False),
        ),
    ]
