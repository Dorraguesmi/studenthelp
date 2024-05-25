from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    OFFER = 0
    REQUEST = 1
    TYPE_CHOICES = [
        (OFFER, 'Offer'),
        (REQUEST, 'Request'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Housing(Post):
    address = models.CharField(max_length=255)
    descript = models.CharField(max_length=255, default="default_descript")
    contact = models.CharField(max_length=255, default="default_contact")
class TransportManager(models.Manager):
    def all_transports(self):
        return self.all()
class Transport(Post):
    depart = models.CharField(max_length=255, default="default_depart")
    destination = models.CharField(max_length=255)
    departuretime = models.CharField(max_length=255, default="default_departtime")
    nbseats = models.IntegerField(default=0)
    contact = models.CharField(max_length=255, default="default_contact")
    objects = TransportManager()



class Event(Post):
    CULTURAL = 0
    SCIENTIFIC = 1
    EVENT_TYPE_CHOICES = [
        (CULTURAL, 'Cultural'),
        (SCIENTIFIC, 'Scientific'),
    ]

    event_type = models.IntegerField(choices=EVENT_TYPE_CHOICES)
    date = models.DateField()

class Internship(Post):
    INTERNSHIP_TYPE_CHOICES = [
        (1, 'Worker'),
        (2, 'Technician'),
        (3, 'PFE'),  
    ]

    internship_type = models.IntegerField(choices=INTERNSHIP_TYPE_CHOICES)
    company = models.CharField(max_length=255)
    duration = models.IntegerField(default=1)
    object = models.CharField(max_length=255, default="default_object")
    contact = models.CharField(max_length=255, default="default_contact")

class Recommendation(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation by {self.creator}"
