from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return u"{}".format(self.name)


class Movie(models.Model):
    """Create movie model"""
    image = models.ImageField(upload_to='static/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    cast = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveSmallIntegerField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    release_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    age_restriction = models.CharField(max_length=2, null=True, blank=True)
    
    # def save(self, *args, **kwargs):
    #     if self.image:
    #         self.image = get_thumbnail(self.image, '500x600', quality=99, format='JPEG')
    #     super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return u"{}".format(self.title)


class Cinema(models.Model):
    image = models.ImageField(upload_to='static/', blank=True, null=True)  
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return u"{}".format(self.name)

class Showtimes(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    cinema = models.ForeignKey(Cinema, on_delete=None, null = True)
    movie = models.ForeignKey(Movie, on_delete=None, null = True)
    remaining_cap = models.IntegerField(default=0)
    active = models.BooleanField(default = True)
    def __str__(self):
        return u"{}-{} {} : {}".format(self.start, self.end, self.cinema, self.movie)

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    showtime = models.ForeignKey(Showtimes, on_delete=None)
    seats = models.IntegerField()
