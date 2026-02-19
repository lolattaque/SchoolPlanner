from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    IMPORTANCE_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    STAGE_CHOICES = (
        ('HS', 'High School'),
        ('UNI', 'University'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    importance = models.CharField(max_length=6, choices=IMPORTANCE_CHOICES)
    completed = models.BooleanField(default=False)
    stage = models.CharField(max_length=3, choices=STAGE_CHOICES)

    def __str__(self):
        return self.title

class Profile(models.Model):
    STAGE_CHOICES = (
        ('HS', 'High School'),
        ('UNI', 'University'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage = models.CharField(max_length=3, choices=STAGE_CHOICES, default='HS')
    interests = models.TextField(blank=True)
    target_program = models.CharField(max_length=255, blank=True, help_text="e.g. Computer Science at Waterloo")

    def __str__(self):
        return f"{self.user.username} Profile"