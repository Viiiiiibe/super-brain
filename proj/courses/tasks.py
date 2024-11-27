from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Window, F
from django.db.models.functions import Rank
from proj.settings import DEFAULT_FROM_EMAIL
from promocodes.models import PromoCode
from .models import Tournament
from django.utils.timezone import now
import uuid  # Для генерации уникального кода
from account.models import CustomUser


@shared_task
def send_emails_after_tournament():
    # Выбираем завершенный турнир с end_date, равной вчерашнему дню
    yesterday = now().date() - timedelta(days=1)
    try:
        tournament_obj = Tournament.objects.filter(end_date=yesterday).first()
    except:
        tournament_obj = None

    if tournament_obj:
        # Получаем участников и их места
        tournament_obj_participants = tournament_obj.participants.annotate(
            rank=Window(
                expression=Rank(),
                order_by=F('tournament_points').desc()
            )
        ).order_by('-tournament_points')

        if tournament_obj_participants:
            for user in tournament_obj_participants:
                if user.rank == 1:
                    # Создаем промокод для победителя
                    promo_code = PromoCode.objects.create(
                        code=str(uuid.uuid4())[:8].upper(),  # Генерируем уникальный код
                        description="100% скидка на следующий турнир",
                        discount_percentage=100.0,
                        max_uses=1,  # Промокод можно использовать только один раз
                        valid_from=now(),
                        valid_to=now() + timedelta(days=30),  # Действителен 30 дней
                        is_active=True
                    )
                    # Отправляем email
                    send_mail(
                        subject='Ура ты выиграл турнир!',
                        message=(
                            f'Ура турнир {tournament_obj.title} окончен!\n'
                            f'Ты занял {user.rank} место и это просто невероятно!\n'
                            f'Мы дарим тебе промокод на ПОЛНОСТЬЮ БЕСПЛАТНОЕ участие в следующем турнире: '
                            f'{promo_code.code}\n'
                            f'Срок действия: до {promo_code.valid_to.date()}'
                        ),
                        from_email=DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                else:
                    # Отправляем email
                    send_mail(
                        subject='Ура турнир окончен!',
                        message=(
                            f'Ура турнир {tournament_obj.title} окончен!\n'
                            f'Привет, {user.username}!\n'
                            f'Ты занял {user.rank} место и это реально круто!'
                        ),
                        from_email=DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )


@shared_task
def clearing_the_tournament_top_of_users():
    today = now().date()
    try:
        tournament_obj = Tournament.objects.filter(start_date=today).first()
    except:
        tournament_obj = None

    if tournament_obj:
        all_users_list = CustomUser.objects.all()
        for user in all_users_list:
            user.tournament_points = 0
            user.save()
