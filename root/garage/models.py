from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class TopLeaderboard(models.Model):
    name = models.CharField(max_length=40)
    team = models.CharField(max_length=40)
    points = models.IntegerField()
    # image = models.ImageField(upload_to='images/', blank=True, null=True) # for local databases
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name
    
class ConstructorsLeaderboard(models.Model):
    name = models.CharField()
    points = models.IntegerField()
    # image = models.ImageField(upload_to='images/', blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
      
class Calendar(models.Model):
    circuit = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    # country_image = models.ImageField(upload_to='images/', blank=True, null=True)
    country_image = CloudinaryField('image', blank=True, null=True)
    # image = models.ImageField(upload_to='images/', blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)

    from_date = models.DateTimeField()
    to_date = models.DateTimeField()

    description = models.TextField(blank=True)

    STATUS_CHOICES = [
        ('none', 'None'),
        ('previous', 'Previous'),
        ('next', 'Next'),
        ('upcoming', 'Upcoming'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    participants = models.ManyToManyField(Driver, through='RaceResult', related_name='races')

    class Meta:
        ordering = ['from_date']

    def __str__(self):
        return f"{self.circuit}"

    def is_upcoming(self):
        return self.from_date > timezone.now()
    
    def get_podium(self):
        return self.raceresult_set.order_by('position').select_related('driver')[:3]
    
class RaceResult(models.Model):
    race = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Finished')
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('race', 'driver')

    def __str__(self):
        return f"{self.race} - {self.driver}"
    
    
class Chat_post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    FLAIR_CHOICES = [
        ('news', 'News'),
        ('question', 'Question'),
        ('meme', 'Meme'),
        ('analysis', 'Analysis'),
        ('prediction', 'Prediction'),
        ('discussion', 'Discussion'),
        ('race_reaction', 'Race Reaction'),
        ('qualifying', 'Qualifying'),
        ('practice', 'Practice'),
        ('strategy', 'Strategy'),
        ('technical', 'Technical'),
        ('penalty', 'Penalty'),
        ('fantasy', 'F1 Fantasy'),
        ('fan_art', 'Fan Art'),
        ('highlight', 'Highlight'),
        ('throwback', 'Throwback'),
        ('driver_ranking', 'Driver Ranking'),
        ('poll', 'Poll'),
        ('rumor', 'Rumor'),
        ('announcement', 'Announcement'),
    ]
    flair = models.CharField(max_length=25, choices=FLAIR_CHOICES)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='images/')
    image = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_upvotes(self):
        return self.votes.filter(value=1).count()

    def total_downvotes(self):
        return self.votes.filter(value=-1).count()

    def __str__(self):
        return f'{self.user.username} - {self.title[:15]}'
    
class Vote(models.Model):
    post = models.ForeignKey(Chat_post, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=((1, 'Upvote'), (-1, 'Downvote')))

    class Meta:
        unique_together = ('post', 'user')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='images/', default='media/image/default.jpg')
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Comments(models.Model):
    post = models.ForeignKey(Chat_post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:10]




    




