# Generated by Django 4.0 on 2022-01-13 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unite_has_compte',
            name='chapire',
        ),
        migrations.AddField(
            model_name='scf_pos_7',
            name='chapitre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ch_comptes', to='main.chapitre'),
        ),
        migrations.AlterField(
            model_name='unite_has_compte',
            name='compte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unite_comptes', to='main.scf_pos_7'),
        ),
    ]
