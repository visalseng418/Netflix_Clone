from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.`
class Movie(models.Model):

    GENRE = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('science_fiction', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
    ]

    uu_id = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=250)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices = GENRE)
    lenght = models.PositiveIntegerField()
    image_card = models.ImageField(upload_to = 'movie_images/')
    image_cover = models.ImageField(upload_to= 'movie_images/')
    video = models.FileField(upload_to= 'movie-videos/')
    movie_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class MovieList(models.Model):
    owner = models.ForeignKey(User,on_delete= models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete= models.CASCADE)
