# Generated by Django 4.1.1 on 2022-10-29 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_alter_stockproducts_image_prod'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockproducts',
            old_name='image_prod',
            new_name='thumbnail',
        ),
    ]
