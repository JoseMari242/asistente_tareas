# Generated by Django 5.1 on 2024-09-09 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tarea',
            options={'ordering': ['completo']},
        ),
        migrations.AddField(
            model_name='tarea',
            name='fecha',
            field=models.DateField(blank=True, null=True),
        ),
    ]
