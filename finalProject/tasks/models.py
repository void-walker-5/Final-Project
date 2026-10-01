from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


class Task(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2, "Title must be greater than 2 characters")
        ]
    )

    description = models.TextField()

    status = models.CharField(
        max_length=50
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title