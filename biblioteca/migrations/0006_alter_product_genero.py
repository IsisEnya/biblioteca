# Generated by Django 4.2.3 on 2023-07-23 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0005_alter_product_genero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='genero',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='biblioteca.genero'),
        ),
    ]
