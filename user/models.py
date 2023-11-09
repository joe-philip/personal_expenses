from collections.abc import Iterable

from django.db import models

from root.utils.choices import GenderChoices
from root.utils.utils import slug_generate

# Create your models here.


class UserProfiles(models.Model):
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dob = models.DateField()
    user = models.OneToOneField('main.User', on_delete=models.CASCADE)
    gender = models.IntegerField(choices=GenderChoices.choices)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='user/profile_images', blank=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User profile'

    def __str__(self) -> str: return self.user.first_name

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if not self.slug:
            self.slug = slug_generate()
        return super().save(force_insert, force_update, using, update_fields)
