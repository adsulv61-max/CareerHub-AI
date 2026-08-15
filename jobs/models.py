from django.db import models
from django.contrib.auth.models import User


# =========================================================
# JOB
# =========================================================

class Job(models.Model):

    title = models.CharField(
        max_length=200
    )

    company = models.CharField(
        max_length=200
    )

    location = models.CharField(
        max_length=100
    )

    salary = models.CharField(
        max_length=100,
        blank=True
    )

    job_type = models.CharField(
        max_length=50
    )

    description = models.TextField()

    skills = models.CharField(
        max_length=300
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================================================
# JOB APPLICATION
# =========================================================

class JobApplication(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    cover_letter = models.TextField(
        blank=True
    )

    # Application Status
    status = models.CharField(
        max_length=30,
        default="Submitted"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


# =========================================================
# CONTACT MESSAGE
# =========================================================

class ContactMessage(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name