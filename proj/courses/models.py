from django.db import models
from django.contrib.auth import get_user_model
from proj.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL #get_user_model()


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='Название в URL', max_length=200, unique=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория курсов'
        verbose_name_plural = 'Категории курсов'


class Course(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='Название в URL', max_length=200, unique=True)
    category = models.ForeignKey(
        'Category',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='courses_in_category',
        verbose_name='Категория',
    )
    number_of_problems = models.IntegerField(verbose_name='Количество задач в курсе', blank=False, null=False)
    image = models.ImageField(
        'Обложка курса',
        upload_to='courses_img/',
        default='/courses_img/default_course_img.png'
    )
    free = models.BooleanField("Бесплатный", default=False)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class CourseProblem(models.Model):
    course = models.ForeignKey(
        'Course',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='problems',
        verbose_name='Курс',
    )
    number = models.IntegerField(verbose_name='Номер задачи в курсе', blank=False, null=False)
    text = models.TextField(verbose_name='Текст задачи', blank=False, null=False)
    right_answer = models.IntegerField('Правильный ответ', blank=False, null=False)
    theory = models.TextField(verbose_name='Теория для задачи', blank=True, null=True)
    answer1_text = models.IntegerField('Текст ответа 1', blank=False, null=False)
    answer1_image = models.ImageField(
        'Картинка ответа 1',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    answer2_text = models.IntegerField('Текст ответа 2', blank=False, null=False)
    answer2_image = models.ImageField(
        'Картинка ответа 2',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    answer3_text = models.IntegerField('Текст ответа 3', blank=True, null=True)
    answer3_image = models.ImageField(
        'Картинка ответа 3',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    answer4_text = models.IntegerField('Текст ответа 4', blank=True, null=True)
    answer4_image = models.ImageField(
        'Картинка ответа 4',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    points = models.IntegerField('Баллы за решение', blank=False, null=False, default=1)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class PersonalCourse(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='Название в URL', max_length=200, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='personal_courses',
        verbose_name='Пользователя'
    )
    number_of_problems = models.IntegerField(verbose_name='Количество задач в курсе', blank=False, null=False)
    image = models.ImageField(
        'Обложка курса',
        upload_to='courses_img/',
        default='/courses_img/default_course_img.png'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Личный курс'
        verbose_name_plural = 'Личные курсы'


class PersonalProblem(models.Model):
    course = models.ForeignKey(
        'PersonalCourse',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='problems',
        verbose_name='Личный курс',
    )
    number = models.IntegerField(verbose_name='Номер задачи в курсе', blank=False, null=False)
    text = models.TextField(verbose_name='Текст задачи', blank=False, null=False)
    right_answer = models.IntegerField('Правильный ответ', blank=False, null=False)
    theory = models.TextField(verbose_name='Теория для задачи', blank=True, null=True)
    answer1_text = models.IntegerField('Текст ответа 1', blank=False, null=False)
    answer1_image = models.ImageField(
        'Картинка ответа 1',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    answer2_text = models.IntegerField('Текст ответа 2', blank=False, null=False)
    answer2_image = models.ImageField(
        'Картинка ответа 2',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    answer3_text = models.IntegerField('Текст ответа 3', blank=True, null=True)
    answer3_image = models.ImageField(
        'Картинка ответа 3',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    answer4_text = models.IntegerField('Текст ответа 4', blank=True, null=True)
    answer4_image = models.ImageField(
        'Картинка ответа 4',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    points = models.IntegerField('Баллы за решение', blank=False, null=False, default=1)

    class Meta:
        verbose_name = 'Задача личного курса'
        verbose_name_plural = 'Задачи личного курса'


class Tournament(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    participants = models.ManyToManyField(
        User,
        related_name='tournaments',
        verbose_name='Участники'
    )
    start_date = models.DateField(verbose_name='Дата начала', auto_now_add=False)
    end_date = models.DateField(verbose_name='Дата завершения', auto_now_add=False)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'


class TournamentProblem(models.Model):
    tournament = models.ForeignKey(
        'Tournament',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='problems',
        verbose_name='Турнир',
    )
    number = models.IntegerField(verbose_name='Номер задачи в турнире', blank=False, null=False)
    text = models.TextField(verbose_name='Текст задачи', blank=False, null=False)
    right_answer = models.IntegerField('Правильный ответ', blank=False, null=False)
    answer1_text = models.IntegerField('Текст ответа 1', blank=False, null=False)
    answer1_image = models.ImageField(
        'Картинка ответа 1',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    answer2_text = models.IntegerField('Текст ответа 2', blank=False, null=False)
    answer2_image = models.ImageField(
        'Картинка ответа 2',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    answer3_text = models.IntegerField('Текст ответа 3', blank=True, null=True)
    answer3_image = models.ImageField(
        'Картинка ответа 3',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    answer4_text = models.IntegerField('Текст ответа 4', blank=True, null=True)
    answer4_image = models.ImageField(
        'Картинка ответа 4',
        upload_to='answers_img/',
        blank=True,
        null=True
    )
    points = models.IntegerField('Баллы за решение', blank=False, null=False, default=1)

    class Meta:
        verbose_name = 'Задача турнира'
        verbose_name_plural = 'Задачи турнира'
