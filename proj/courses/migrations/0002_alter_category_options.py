# Generated by Django 5.1.2 on 2024-11-02 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория курсов', 'verbose_name_plural': 'Категории курсов'},
        ),
    ]