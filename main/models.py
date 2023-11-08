from datetime import datetime
from re import search

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from root.utils.utils import slug_generate

# Create your models here.


class APIKeyManager(models.Manager):
    def create_key(self, *args, **kwargs):
        from random import choice
        from string import ascii_lowercase, ascii_uppercase, digits

        from django.contrib.auth.hashers import make_password
        from django.core.exceptions import ValidationError

        create = {}
        if not kwargs.get('label', False):
            raise ValidationError('A unique label is required for key')
        for key, value in kwargs.items():
            if key in ('key', 'created_at', 'updated_at'):
                continue
            create[key] = value
        code = ''.join(
            choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(46)
        )
        key_identifier = ''.join(
            choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6)
        )
        create['key'] = f'{make_password(code)}'
        create['key_identifier'] = key_identifier
        self.api_key = self.create(**create)
        return (f'API Key: {key_identifier}.{code}')

    def create_key_only(self, *args, **kwargs):
        key_string = self.create_key(*args, **kwargs)
        match = search(r'^API\sKey:\s(.+)', key_string)
        if match is not None:
            return match.group(1)
        return match

    def get_identifier(self, key: str):
        pattern = r'(.+)\.'
        match = search(pattern, key)
        if match is None:
            return False
        return match.group(1)

    def get_key(self, key: str):
        pattern = r'\.(.+)'
        match = search(pattern, key)
        if match is None:
            return False
        return match.group(1)

    def validate_key(self, key: str):
        identifier = self.get_identifier(key)
        if identifier:
            today = datetime.now()
            keys = APIKey.objects.filter(
                models.Q(expiry=None) | models.Q(expiry__gt=today),
                key_identifier=identifier, is_active=True
            )
            if any(tuple(map(lambda x: check_password(self.get_key(key), x.key), keys))):
                return True
        return False

    def deactivate_key(self, key: str):
        identifier = self.get_identifier(key)
        if identifier:
            keys = APIKey.objects.filter(key_identifier=identifier)
            if keys.exists():
                for key_ob in keys:
                    if check_password(self.get_key(key), key_ob.key):
                        key_ob.is_active = False
                        key_ob.save()
                        return True
        return False


class APIKey(models.Model):
    key = models.CharField(max_length=150, unique=True)
    expiry = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        null=True, default=None
    )
    label = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    key_identifier = models.CharField(max_length=10, unique=True)

    objects = APIKeyManager()

    def __str__(self) -> str:
        return f'{self.key}'

    class Meta:
        db_table = 'api-key'
        verbose_name = 'API Key'
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields) -> AbstractBaseUser:
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields) -> AbstractBaseUser:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class UserTypeChoices(models.IntegerChoices):
        USER = 1, 'User'
        ADMIN = 2, 'Admin'
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(unique=True)
    email = models.EmailField(unique=True)
    user_type = models.IntegerField(choices=UserTypeChoices.choices, default=1)

    REQUIRED_FIELDS = ('first_name',)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slug_generate('user')
        return super().save(*args, **kwargs)

    def __str__(self) -> str: return self.first_name
