from datetime import datetime

from django.utils.text import slugify


def slug_generate(key: str = 'slug') -> str:
    return slugify(f'{key}-{datetime.now().timestamp()}')
