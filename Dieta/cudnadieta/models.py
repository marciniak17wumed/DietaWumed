from django.db import models
from django.contrib.auth.models import User

class CalorieEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wiek = models.IntegerField(default=30)
    wzrost = models.FloatField(default=170)
    waga = models.FloatField(default=70)
    PLEC_CHOICES = [
        ('M', 'Mężczyzna'),
        ('K', 'Kobieta'),
    ]
    plec = models.CharField(max_length=1, choices=PLEC_CHOICES, default='M')
    AKTYWNOSC_CHOICES = [
        ('niska', 'Niska'),
        ('umiarkowana', 'Umiarkowana'),
        ('wysoka', 'Wysoka'),
    ]
    aktywnosc = models.CharField(max_length=20, choices=AKTYWNOSC_CHOICES, default='niska')
    CEL_CHOICES = [
        ('schudnac', 'Schudnąć'),
        ('utrzymanie_masy', 'Utrzymać wagę'),
        ('przytyc', 'Przytyć'),
    ]
    cel = models.CharField(max_length=20, choices=CEL_CHOICES, default='utrzymanie')
