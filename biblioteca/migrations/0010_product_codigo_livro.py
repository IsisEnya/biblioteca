# Generated by Django 4.2.3 on 2023-07-23 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0009_product_data_publicacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='codigo_livro',
            field=models.CharField(default='adimin', max_length=255),
        ),
    ]
