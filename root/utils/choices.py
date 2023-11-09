from django.db.models import IntegerChoices


class GenderChoices(IntegerChoices):
    MALE = 1, 'Male'
    FEMALE = 2, 'Female'
    TRANSGENDER = 3, 'Transgender'
