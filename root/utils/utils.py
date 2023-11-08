from datetime import datetime
from typing import Any

from django.utils.text import slugify


def slug_generate(key: str = 'slug') -> str:
    return slugify(f'{key}-{datetime.now().timestamp()}')


def success(data: Any = None) -> dict:
    response = {'status': True, 'message': 'success'}
    if data is not None:
        response['data'] = data
    return response


def fail(error: Any) -> dict:
    return {'status': False, 'message': 'fail', 'error': error}
