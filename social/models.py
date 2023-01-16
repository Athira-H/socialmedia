from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.
class Posts(models.Model):
    title=models.CharField(max_length=250)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name="likes")
    
    @property
    def post_comments(self):
        # po=self.posts_set.all().annotate(u_count=Count('liked_by')).order_by('-u_count')
        return self.comments_set.all()
        # return po

    def __str__(self):
        return self.title
    
    @property
    def likecount(self):
        return self.liked_by.all().count()

class Comments(models.Model):
    comment=models.CharField(max_length=250)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(User,related_name="like")

    def __str__(self):
        return self.comment

    @property
    def likecount(self):
        return self.liked_by.all().count()


class Userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profile_pics",null=True)
    timelinepic=models.ImageField(upload_to="timelinepic",null=True)
    followings=models.ManyToManyField(User,related_name="followings")


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    date = models.DateTimeField(auto_now_add=True)