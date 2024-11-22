# Generated by Django 5.1.2 on 2024-11-22 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_remove_course_number_of_problems_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseproblem',
            name='answer1_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст ответа 1'),
        ),
        migrations.AlterField(
            model_name='courseproblem',
            name='answer2_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст ответа 2'),
        ),
        migrations.AlterField(
            model_name='personalproblem',
            name='answer1_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст ответа 1'),
        ),
        migrations.AlterField(
            model_name='personalproblem',
            name='answer2_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст ответа 2'),
        ),
        migrations.AlterField(
            model_name='tournamentproblem',
            name='answer1_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст ответа 1'),
        ),
        migrations.AlterField(
            model_name='tournamentproblem',
            name='answer2_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст ответа 2'),
        ),
    ]
