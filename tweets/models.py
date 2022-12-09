import random
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Q
# from django.db.models import Count
# from django.contrib.humanize.templatetags.humanize import naturaltime

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True) # [x.user.id for x in profiles]
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-timestamp")

class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)




class Tweet(models.Model):
    # Maps to SQL data
    id = models.AutoField(primary_key=True)
    # parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets", null=True) # many users can many tweets
    # likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    #comments = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="Baseballcomments")
    
    # def FORMAT(self):
      
    #     return naturaltime(self.timestamp)

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['timestamp'] = naturaltime(instance.timestamp)
        
    #     return representation

    # @property
    # def timesince(self):
    #     return timesince.timesince(self.timestamp)

    objects = TweetManager()
    # def __str__(self):
    #     return self.content
    
    class Meta:
        ordering = ['-id']
    
    @property
    def is_retweet(self):
        return self.parent != None
    
    def serialize(self):
        '''
        Feel free to delete!
        '''
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }


    # def FORMAT(self):
    #    from django.utils.timesince import timesince
    #    return timesince(self.timestamp)
       
    # @property
    # def comments(self):
    #     instance = self
    #     qs = Comment.objects.filter_by_instance(instance)
    #     return qs

    # @property
    # def get_content_type(self):
    #     instance = self
    #     content_type = ContentType.objects.get_for_model(instance.__class__)
    #     return content_type



class Comment(models.Model):
    #id = models.AutoField(primary_key=True)
    # parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    tweet = models.ForeignKey(Tweet,  on_delete=models.CASCADE, null=True, related_name="tweets_comments")
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="comments")
    likes = models.ManyToManyField(User, related_name='comment_user', blank=True, through=CommentLike)
    content=models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    total_comments = models.ForeignKey('self',related_name='comment_count',blank=True,null=True,on_delete = models.CASCADE)

    objects = TweetManager()


    
 #   def __str__(self):
  #      return 'comment on {} by {}'.format(self.post.title,self.user.username)

    class Meta:
        ordering = ['-id']
    
    @property
    def is_retweet(self):
        return self.parent != None
    
    def serialize(self):
        '''
        Feel free to delete!
        '''
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }




    class Meta:
        ordering = ['-id']
    
    @property
    def is_retweet(self):
        return self.parent != None
    from django.db import models

class UploadVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='', null=True)
    videoname = models.CharField(max_length=50, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, blank=True, null=True)
    imagename = models.CharField(max_length=25, null=True)
    about = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.videoname

    # def image_img(self):
    #     if self.image:
    #         return u'<img src="%s" width=50 height=50 />' % self.image.url
    #     else:
    #         return '(Sin imagen)'

class CommentVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    uploadedvideo = models.ForeignKey(UploadVideo, on_delete=models.CASCADE, related_name="uploadedvideo")
    comment = models.CharField(max_length=275, null=False)


# Create your models here.
