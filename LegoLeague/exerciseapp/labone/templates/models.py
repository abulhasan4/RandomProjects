from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
#... any other imports

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField('Username', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CARDIO = 'Cardio'
    STRENGTH_TRAINING = 'Strength Training'
    FLEXIBILITY = 'Flexibility'
    YOGA = 'Yoga'
    PILATES = 'Pilates'
    HIIT = 'HIIT'
    CROSSFIT = 'CrossFit'
    SWIMMING = 'Swimming'
    CYCLING = 'Cycling'
    RUNNING = 'Running'
    WALKING = 'Walking'
    OTHER = 'Other'
    EXERCISE_TYPE_CHOICES = [
        (CARDIO, 'Cardio'),
        (STRENGTH_TRAINING, 'Strength Training'),
        (FLEXIBILITY, 'Flexibility'),
        (YOGA, 'Yoga'),
        (PILATES, 'Pilates'),
        (HIIT, 'HIIT'),
        (CROSSFIT, 'CrossFit'),
        (SWIMMING, 'Swimming'),
        (CYCLING, 'Cycling'),
        (RUNNING, 'Running'),
        (WALKING, 'Walking'),
        (OTHER, 'Other'),
    ]
    exercise_type = models.CharField(max_length=50, choices=EXERCISE_TYPE_CHOICES)
    DURATION_CHOICES = [
        ('0:15:00', '15 minutes'),
        ('0:30:00', '30 minutes'),
        ('0:45:00', '45 minutes'),
        ('1:00:00', '1 hour'),
        ('1:15:00', '1 hour 15 minutes'),
        ('1:30:00', '1 hour 30 minutes'),
        ('1:45:00', '1 hour 45 minutes'),
        ('2:00:00', '2 hours'),
        ('2:15:00', '2 hours 15 minutes'),
        ('2:30:00', '2 hours 30 minutes'),
        ('2:45:00', '2 hours 45 minutes'),
        ('3:00:00', '3 hours'),
    ]
    duration = models.CharField(max_length=8, choices=DURATION_CHOICES)
    LOW = 'Low'
    MODERATE = 'Moderate'
    HIGH = 'High'
    INTENSITY_CHOICES = [
        (LOW, 'Low'),
        (MODERATE, 'Moderate'),
        (HIGH, 'High'),
    ]
    intensity = models.CharField(max_length=20, choices=INTENSITY_CHOICES)
    description = models.TextField()

    def __str__(self):
        return f"{self.user}'s {self.exercise_type} - Duration: {self.get_duration_display()}, Intensity: {self.intensity}, Description: {self.description}"

