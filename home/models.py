from django.db import models
from django.contrib.auth.models import User


class ChatHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    question = models.TextField()

    answer = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.question


class Application(models.Model):

    STATUS_CHOICES = [
        ("Submitted", "Submitted"),
        ("Under Review", "Under Review"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job_title = models.CharField(
        max_length=200
    )

    company = models.CharField(
        max_length=200
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Submitted"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.job_title} - {self.company}"