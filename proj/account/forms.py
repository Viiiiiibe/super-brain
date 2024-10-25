from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import CustomUser

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Адрес электронной почты уже привязан к аккаунту или содержит ошибку")

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'email',
                  'points', 'tournament_points', 'end_of_subscription', 'solved_problems',
                  'solved_personal_problems', 'solved_tournament_problems', 'is_active',
                  'is_superuser', 'is_staff', 'groups', 'user_permissions', 'date_joined',
                  'last_login',)
