from django.db import models
from django.forms import IntegerField
from django.contrib.auth.models import User


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    year_released = models.DateField()
    length = models.IntegerField(default=0)
    genre = models.CharField(max_length=30)
    thumbnail = models.ImageField(upload_to='thumbnails/', verbose_name='Movie Poster')

    def __str__(self):
        return self.name

class Session(models.Model):
     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
     date = models.DateField()
     start_time = models.TimeField()
     end_time = models.TimeField()
     audience_number = models.IntegerField(default=1)
     is_active = models.BooleanField(default=True)

     def __str__(self):
         return f"Session {self.id} | {self.movie.name}: {self.start_time} - {self.end_time} | Audience: {self.audience_number}"

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    review_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')