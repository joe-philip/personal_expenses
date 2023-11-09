from django.db import models

from main.fields import CommonFields
from root.utils.choices import GenderChoices

# Create your models here.


class UserProfiles(CommonFields):
    dob = models.DateField()
    user = models.OneToOneField('main.User', on_delete=models.CASCADE)
    gender = models.IntegerField(choices=GenderChoices.choices)
    bio = models.TextField(blank=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User profile'

    def __str__(self) -> str: return self.user.first_name
