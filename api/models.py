from django.db import models

# Create your models here.


class Football(models.Model):
    club_name = models.CharField(max_length=100)
    country_name= models.CharField(max_length=100)
    leage=models.CharField(max_length=100)

    def __str__(self):
        return self.club_name

