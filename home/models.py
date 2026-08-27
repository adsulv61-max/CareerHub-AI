from django.db import models
from django.contrib.auth.models import User


# =====================================================
# CHAT HISTORY
# =====================================================

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


# =====================================================
# USER PROFILE
# =====================================================

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=200,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    education = models.CharField(
        max_length=300,
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


# =====================================================
# JOB APPLICATIONS
# =====================================================

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