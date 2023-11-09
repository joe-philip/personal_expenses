import re

from django.conf import settings
from django.core.exceptions import ValidationError


class PasswordRegexValidation:
    def __init__(self, patterns=None) -> None:
        if patterns is None:
            patterns = getattr(settings, 'PASSWORD_REGEX_PATTERNS', None)
        self.patterns = patterns
        self.errors = []

    def validate(self, password, user=None):
        def check(password, pattern):
            if re.search(pattern.get('pattern'), password) is None:
                if not pattern.get('message') in self.errors:
                    self.errors.append(pattern.get('message'))
        if self.patterns is None:
            raise ValidationError(
                'Unable to validate password no validation patterns found'
            )
        tuple(map(lambda x: check(password, x), self.patterns))
        if self.errors:
            # print(self.errors)
            raise ValidationError(self.errors)


class PasswordSpecialCharacterValidation:
    def __init__(self, allowed_characters=None) -> None:
        if allowed_characters is None:
            allowed_characters = getattr(
                settings, 'PASSWORD_ALLOWED_SPECIAL_CHARACTERS', ''
            )
        self.characters = allowed_characters

    def validate(self, password, user=None):
        if self.characters is None:
            raise ValidationError('Special_characters not found')
        if not any(i in password for i in self.characters):
            raise ValidationError('Atleast one special character is required')
