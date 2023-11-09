from collections.abc import Iterable

from django.db import models

from root.utils.utils import slug_generate


class CommonFields(models.Model):
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if not self.slug:
            self.slug = slug_generate()
        return super().save(force_insert, force_update, using, update_fields)
