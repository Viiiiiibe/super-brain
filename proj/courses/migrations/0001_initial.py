# Generated by Django 5.1.2 on 2024-10-25 15:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Название в URL')),
            ],
            options={
                'verbose_name': 'Категория задач',
                'verbose_name_plural': 'Категории задач',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Название в URL')),
                ('number_of_problems', models.IntegerField(verbose_name='Количество задач в курсе')),
                ('image', models.ImageField(default='/courses_img/default_course_img.png', upload_to='courses_img/', verbose_name='Обложка курса')),
                ('free', models.BooleanField(default=False, verbose_name='Бесплатный')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_in_category', to='courses.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='PersonalCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Название в URL')),
                ('number_of_problems', models.IntegerField(verbose_name='Количество задач в курсе')),
                ('image', models.ImageField(default='/courses_img/default_course_img.png', upload_to='courses_img/', verbose_name='Обложка курса')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_courses', to=settings.AUTH_USER_MODEL, verbose_name='Пользователя')),
            ],
            options={
                'verbose_name': 'Личный курс',
                'verbose_name_plural': 'Личные курсы',
            },
        ),
        migrations.CreateModel(
            name='PersonalProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер задачи в курсе')),
                ('text', models.TextField(verbose_name='Текст задачи')),
                ('right_answer', models.IntegerField(verbose_name='Правильный ответ')),
                ('theory', models.TextField(blank=True, null=True, verbose_name='Теория для задачи')),
                ('answer1_text', models.IntegerField(verbose_name='Текст ответа 1')),
                ('answer1_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 1')),
                ('answer2_text', models.IntegerField(verbose_name='Текст ответа 2')),
                ('answer2_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 2')),
                ('answer3_text', models.IntegerField(blank=True, null=True, verbose_name='Текст ответа 3')),
                ('answer3_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 3')),
                ('answer4_text', models.IntegerField(blank=True, null=True, verbose_name='Текст ответа 4')),
                ('answer4_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 4')),
                ('points', models.IntegerField(default=1, verbose_name='Баллы за решение')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='courses.personalcourse', verbose_name='Личный курс')),
            ],
            options={
                'verbose_name': 'Задача личного курса',
                'verbose_name_plural': 'Задачи личного курса',
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер задачи в курсе')),
                ('text', models.TextField(verbose_name='Текст задачи')),
                ('right_answer', models.IntegerField(verbose_name='Правильный ответ')),
                ('theory', models.TextField(blank=True, null=True, verbose_name='Теория для задачи')),
                ('answer1_text', models.IntegerField(verbose_name='Текст ответа 1')),
                ('answer1_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 1')),
                ('answer2_text', models.IntegerField(verbose_name='Текст ответа 2')),
                ('answer2_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 2')),
                ('answer3_text', models.IntegerField(blank=True, null=True, verbose_name='Текст ответа 3')),
                ('answer3_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 3')),
                ('answer4_text', models.IntegerField(blank=True, null=True, verbose_name='Текст ответа 4')),
                ('answer4_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 4')),
                ('points', models.IntegerField(default=1, verbose_name='Баллы за решение')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='courses.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата завершения')),
                ('participants', models.ManyToManyField(related_name='tournaments', to=settings.AUTH_USER_MODEL, verbose_name='Участники')),
            ],
            options={
                'verbose_name': 'Турнир',
                'verbose_name_plural': 'Турниры',
            },
        ),
        migrations.CreateModel(
            name='TournamentProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер задачи в турнире')),
                ('text', models.TextField(verbose_name='Текст задачи')),
                ('right_answer', models.IntegerField(verbose_name='Правильный ответ')),
                ('answer1_text', models.IntegerField(verbose_name='Текст ответа 1')),
                ('answer1_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 1')),
                ('answer2_text', models.IntegerField(verbose_name='Текст ответа 2')),
                ('answer2_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 2')),
                ('answer3_text', models.IntegerField(blank=True, null=True, verbose_name='Текст ответа 3')),
                ('answer3_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 3')),
                ('answer4_text', models.IntegerField(blank=True, null=True, verbose_name='Текст ответа 4')),
                ('answer4_image', models.ImageField(blank=True, null=True, upload_to='answers_img/', verbose_name='Картинка ответа 4')),
                ('points', models.IntegerField(default=1, verbose_name='Баллы за решение')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='courses.tournament', verbose_name='Турнир')),
            ],
            options={
                'verbose_name': 'Задача турнира',
                'verbose_name_plural': 'Задачи турнира',
            },
        ),
    ]
