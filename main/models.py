from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from root.utils.utils import slug_generate

# Create your models here.


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
