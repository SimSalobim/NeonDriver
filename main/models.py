from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.name}"

class Car(models.Model):
    name = models.CharField(max_length=100, unique=True)
    engine = models.CharField(max_length=100, blank=True)
    armor = models.CharField(max_length=100, blank=True)
    speed = models.CharField(max_length=50, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_cars', blank=True)

    def user_has_liked(self, user):
        return self.likes.filter(id=user.id).exists() if user.is_authenticated else False

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.name