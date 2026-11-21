from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{12}$",
    message="Enter a valid phone number: exacly 12 digits",
)

class Candidate(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=12, validators=[phone_validator] ,blank=True)


    class Meta:
        db_table = 'candidate'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} <{self.email}>"
