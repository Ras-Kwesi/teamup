from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Gym(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=100)
    owner = models.ForeignKey(User,related_name='owner')


class Chatroom(models.Model):
    name = models.CharField(max_length=20,unique=True)
    info = models.TextField(max_length=100)
    admin = models.ForeignKey(User,related_name='administrate')

    def save_chatroom(self):
        self.save()

    def remove_chatroom(self):
        self.delete()

    @classmethod
    def get_chatroom(cls,id):
        hood = Chatroom.objects.get(id=id)
        return hood


# class Member(models.Model):
#     user = models.ForeignKey(User,related_name='member')
#     chatroom = models.ForeignKey(Chatroom,related_name='chatroom')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=100, blank=True)
    profilepic = models.ImageField(upload_to='picture/',blank=True)
    contact = models.CharField(max_length=15,blank=True)
    mygym = models.ForeignKey(Gym,related_name='mygym',blank=True,null=True)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    chatroom = models.ManyToManyField(Chatroom)

    @receiver(post_save,sender=User)
    def create_user_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save,sender=User)
    def save_user_profile(sender,instance,**kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


    @classmethod
    def addchatroom(cls,user,newroom):
        room, created = cls.objects.get_or_create(
            user = user
        )
        room.chatroom.add(newroom)

    @classmethod
    def removechatroom(cls, user, newroom):
        room, created = cls.objects.get_or_create(
            user=user
        )
        room.chatroom.remove(newroom)


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User,related_name="befriend",null=True)

    @classmethod
    def addfriend(cls,current_user,other_user):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(other_user)

    @classmethod
    def removefriend(cls,current_user,other_user):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(other_user)

    # @classmethod
    # def get_friends(cls,current_user):
    #     friend, s =


class Post(models.Model):
    title = models.CharField(max_length=30)
    post = models.TextField(max_length=100)
    chatroom = models.ForeignKey(Chatroom,related_name='posts',null=True)
    gym = models.ForeignKey(Gym,related_name='gym',null=True)
    poster = models.ForeignKey(User,on_delete=models.CASCADE)


    def save_post(self):
        self.save()

    def remove_post(self):
        self.delete()

    @classmethod
    def get_hood_posts(cls,id):
        posts = Post.objects.filter(id = id)
        return posts

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    commentator = models.ForeignKey(User)
    comment_post = models.ForeignKey(Post,related_name='comment',null=True)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()


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
    weight = models.IntegerField(default=0)
    profile = models.BooleanField(default=False)




