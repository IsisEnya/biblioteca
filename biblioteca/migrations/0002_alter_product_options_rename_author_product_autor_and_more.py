# Generated by Django 4.2.3 on 2023-07-22 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-criado',), 'verbose_name_plural': 'Products'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='author',
            new_name='autor',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='categoria',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='created',
            new_name='criado',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='created_by',
            new_name='criado_por',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='descrição',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='in_stock',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='is_active',
            new_name='no_estoque',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='titulo',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='quantidade',
            field=models.IntegerField(default=1),
        ),
    ]
