# Generated by Django 4.2.3 on 2023-07-23 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0004_product_genero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='genero',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='product', to='biblioteca.genero'),
        ),
    ]
