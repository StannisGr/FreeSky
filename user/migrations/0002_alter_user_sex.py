# Generated by Django 4.0.3 on 2022-03-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('female', 'ж'), ('male', 'м')], max_length=6, null=True),
        ),
    ]
