# Generated by Django 4.1.1 on 2022-11-03 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_pedidos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedidos',
            old_name='telfono',
            new_name='telefono',
        ),
    ]
