import random

from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, TemplateView, View

from users.forms import UserRegisterForm, UserProfileForm, \
    UserLoginForm  # , UserForgotPasswordForm, UserSetNewPasswordForm
from users.models import User
#User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    # def form_valid(self, form):
    #     self.object = form.save()
    #     send_mail(
    #         subject='Поздравляем с регистрацией',
    #         message='Вы зарегистрировались на нашей платформе, добро пожаловать!',
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[self.object.email]
    #     )
    #     return super().form_valid(form)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = '127.0.0.1:8000'
        set_site = Site.objects.get_current().domain
        print(set_site)
        send_mail(
            subject='Подтвердите свой электронный адрес',
            message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            from_email='fuckup@oscarbot.ru',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return redirect('users:email_confirmation_sent')


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'
    next_page = '/'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    # def form_valid(self, form):
    #     # Метод, который отрабатывает при успешной валидации формы
    #     if form.is_valid():
    #         self.object = form.save()
    #         # Сохранение объекта перед тем, как установить ему пароль
    #         if form.data.get('need_generate', False):
    #             self.object.set_passeword(  # Функция установки пароля,
    #                 # которая хеширует строку для того,
    #                 # чтобы не хранить пароль в открытом виде в БД
    #                 self.object.make_random_password(12)  # Функция генерации пароля
    #             )
    #             self.object.save()
    #
    #     return super().form_valid(form)


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:home'))


class UserConfirmEmailView(View):

    def get(self, request, uidb64, token):
        print(User)
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context

    class EmailConfirmationFailedView(TemplateView):
        template_name = 'users/email_confirmation_failed.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Ваш электронный адрес не активирован'
            return context


# class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
#     """
#     Контроллер по сбросу пароля по почте
#     """
#     form_class = UserForgotPasswordForm
#     template_name = 'system/user_password_reset.html'
#     success_url = reverse_lazy('home')
#     success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
#     subject_template_name = 'system/email/password_subject_reset_mail.txt'
#     email_template_name = 'system/email/password_reset_mail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Запрос на восстановление пароля'
#         return context
#
#
# class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
#     """
#     Контроллер установки нового пароля
#     """
#     form_class = UserSetNewPasswordForm
#     template_name = 'system/user_password_set_new.html'
#     success_url = reverse_lazy('home')
#     success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Установить новый пароль'
#         return context
