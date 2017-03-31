from django.db import models

from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    User 관리자 클래스 
    """
    
    def _create_user(self, email, password, name, is_staff, is_superuser,
            is_active, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(u'잘못된 이메일 참조')
        email = self.normalize_email(email)
        user = self.model(email=email,
                name=name,
                is_staff=is_staff,
                is_active=is_active,
                is_superuser=is_superuser,
                last_login=now,
                date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, name, **extra_fields):
        return self._create_user(email, password, name, False, False,
                False, **extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        return self._create_user(email, name, password, True, True, 
                True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User 클래스 재정의
    """
    email = models.EmailField(_('Email address'), unique=True,
            max_length=255)
    name = models.CharField(_('name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.email