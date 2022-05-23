# Generated by Django 4.0.3 on 2022-05-11 16:32

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_document_options_alter_paymentdata_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='pasport_num',
            field=models.CharField(blank=True, max_length=6, null=True, validators=[user.models.DocumentValidator.num_validator]),
        ),
        migrations.AlterField(
            model_name='document',
            name='pasport_series',
            field=models.CharField(blank=True, max_length=4, null=True, validators=[user.models.DocumentValidator.num_validator]),
        ),
    ]