from django.db import models
from django.utils.timezone import now
from proj.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Код промокода")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Скидка (%)",
        help_text="Укажите процент скидки, например, 10.00 для 10%"
    )
    max_uses = models.PositiveIntegerField(
        verbose_name="Максимальное количество использований",
        blank=True,
        null=True,
        help_text="Оставьте пустым для неограниченного количества использований."
    )
    users_used = models.ManyToManyField(
        User,
        blank=True,
        null=True,
        verbose_name="Пользователи, использовавшие код",
        related_name="used_promo_codes"
    )
    valid_from = models.DateTimeField(
        verbose_name="Начало действия",
        default=now,
        help_text="Дата и время, с которого код становится активным."
    )
    valid_to = models.DateTimeField(
        verbose_name="Окончание действия",
        blank=True,
        null=True,
        help_text="Дата и время, до которого код активен. Оставьте пустым для бессрочного действия."
    )
    is_active = models.BooleanField(
        verbose_name="Активен",
        default=True,
        help_text="Установите в False, чтобы отключить промокод."
    )

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% скидки)"

    def is_valid(self):
        """Проверяет, является ли промокод действительным."""
        if not self.is_active:
            return False
        if self.valid_to and now() > self.valid_to:
            return False
        if self.max_uses and self.users_used.count() >= self.max_uses:
            return False
        return True

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
