import uuid
from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_id = models.BigIntegerField(unique=True, db_index=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=32, null=True, blank=True, verbose_name="Username")
    first_name = models.CharField(max_length=150, verbose_name="First name")
    last_name = models.CharField(max_length=150, null=True,blank=True, verbose_name="Last name")
    language_code = models.CharField(max_length=10, null=True,blank=True, verbose_name="Language code")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} (@{self.username})"
