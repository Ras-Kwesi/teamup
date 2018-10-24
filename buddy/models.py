from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Gym(models.Model):
    name = models.CharField(max_length=20)
    number = models.IntegerField(default=0)

class Chatroom(models.Model):
    name = models.CharField(max_length=20,unique=True)
    info = models.CharField(max_length=40,default = '')
    admin = models.ForeignKey(User,related_name='administrate')

    def save_chatroom(self):
        self.save()

    def remove_chatroom(self):
        self.delete()


    @classmethod
    def get_chatroom(cls,id):
        hood = Chatroom.objects.get(id=id)
        return hood


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=100, blank=True)
    profilepic = models.ImageField(upload_to='picture/',blank=True)
    contact = models.CharField(max_length=15,blank=True)
    mygym = models.ForeignKey(Gym,related_name='mygym',blank=True)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    @receiver(post_save,sender=User)
    def create_user_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save,sender=User)
    def save_user_profile(sender,instance,**kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


class Run(models.Model):
    distance = models.IntegerField(default=0)
    info = models.TextField(max_length=80)
    time = models.TimeField(default=0,auto_now=False,auto_now_add=False)
    date = models.DateField(auto_now=False,auto_now_add=False,)
    profile = models.ForeignKey(User,related_name='run')


class WeightLifting(models.Model):
    benchpress = models.BooleanField(default=False)
    squats = models.BooleanField(default=False)
    deadlift = models.BooleanField(default=False)
    profile = models.BooleanField(default=False)




