# Generated by Django 4.0.3 on 2022-05-10 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_paymentdata_cc_expiry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Документ', 'verbose_name_plural': 'Документы'},
        ),
        migrations.AlterModelOptions(
            name='paymentdata',
            options={'verbose_name': 'Платежная информация', 'verbose_name_plural': 'Платежная информация'},
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('мужчина', 'м'), ('женщина', 'ж')], max_length=7, null=True, verbose_name='Пол'),
        ),
    ]
