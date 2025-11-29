from django.db import models
import uuid

import secrets

class Client(models.Model):
    name = models.CharField(max_length=255)
    base_url = models.URLField(help_text="Base URL of the client application (e.g., http://localhost:8000)", default="http://localhost")
    client_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    client_secret = models.CharField(max_length=255, default=secrets.token_urlsafe, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.client_secret:
            self.client_secret = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Pole(models.Model):
    name = models.CharField(max_length=255)
    fhir_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Sector(models.Model):
    name = models.CharField(max_length=255)
    fhir_id = models.CharField(max_length=255, unique=True)
    pole = models.ForeignKey(Pole, on_delete=models.CASCADE, related_name='sectors')

    def __str__(self):
        return self.name

class Bed(models.Model):
    name = models.CharField(max_length=255)
    fhir_id = models.CharField(max_length=255, unique=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='beds')

    def __str__(self):
        return f"{self.name} ({self.sector.name})"

class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    fhir_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Encounter(models.Model):
    STATUS_CHOICES = [
        ('in-progress', 'In Progress'),
        ('finished', 'Finished'),
        ('planned', 'Planned'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='encounters')
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in-progress')
    fhir_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    def __str__(self):
        return f"Encounter {self.fhir_id} - {self.patient}"

class Observation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='observations')
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='observations')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    fhir_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    def __str__(self):
        return f"Observation for {self.patient} at {self.date}"
