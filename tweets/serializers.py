from email.mime import image
from django.conf import settings
from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import Tweet, Comment, UploadVideo, CommentVideo


MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)
    #image = serializers.ImageField(blank=True,required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value

class CommentActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)
    #image = serializers.ImageField(blank=True, required=False)

    def validate_action(self,value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value


class TweetCreateSerializer(serializers.ModelSerializer):
    # user = PublicProfileSerializer(source='user.profile', read_only=True) # serializers.SerializerMethodField(read_only=True)
    # likes = serializers.SerializerMethodField(read_only=True)
    # image = serializers.SerializerMethodField()
    class Meta:
        model = Tweet
        fields = ['image','content', 'user']

 
    
    def get_likes(self, obj):
        return obj.likes.count()


    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image 
    
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value

class CommentCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True) # serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['user', 'id', 'content', 'likes','image',  'timestamp']


    def get_likes(self, obj):
        return obj.likes.count()

#     # def get_image(self, obj):
#     #     try:
#     #         image = obj.image.url
#     #     except:
#     #         image = None
#     #     return image 

#     def validate_content(self, value):
#         if len(value) > MAX_TWEET_LENGTH:
#             raise serializers.ValidationError("This tweet is too long")
#         return value

#     # def get_user(self, obj):
#     #     return obj.user.id




class CommentTweetSerializer(serializers.ModelSerializer):
    # user = PublicProfileSerializer(source='user.profile', read_only=True)
    # likes = serializers.SerializerMethodField(read_only=True)
    # image = serializers.SerializerMethodField()
    # parent = CommentCreateSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
                'user', 
                # 'id', 
                'content',
                'image',
                'tweet',
                # 'likes',
                # 'is_retweet',
                # 'parent',
                'timestamp']
    def get_likes(self,obj):
        return obj.likes.count()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image 


class TweetSerializer(serializers.ModelSerializer):
    # user = PublicProfileSerializer(source='user.profile', read_only=True)
    #tweets_comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField(read_only=True)
    #image = serializers.SerializerMethodField()
    parent = TweetCreateSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = [
                # 'user', 
                # 'id', 
                'content',
                'image',
                # 'likes',
                # 'is_retweet',
                # 'parent',
                'timestamp']
                #'tweets_comments']

    def get_likes(self, obj):
        return obj.likes.count()

# class Base64ImageField(serializers.ImageField):
#     def to_internal_value(self, data):
#         from django.core.files.base import ContentFile
#         import base64
#         import six
#         import uuid

#         # check if this is a base64 string
#         if isinstance(data, six.string_types):
#             # check if the base64 string is in the "data:" format
#             if 'data:' in data and ';base64,' in data:
#                 # Break out the header from the base64 content
#                 header, data = data.split(';base64,')
#             # Try to decode the file. REturn validation error if it fails.
#             try:
#                 decoded_file = base64.b64decode(data)
#             except TypeError:
#                 self.fail('Invalid image')
            
#             # Generate file name:
#             file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
#             # Get the file name extension:
#             file_extension =  self.get_file_extensions(file_name, decoded_file)
#             complete_file_name = "%s.%s" % (file_name, file_extension, )
#             data = ContentFile(decoded_file, name=complete_file_name)

#         return super(Base64ImageField, self).to_internal_value(data)
    
#     def get_file_extensions(self, file_name, decode_file):
#         import imghdr
#         extension =  imghdr.what(file_name, decode_file)
#         extension =  "jpg" if extension == "jpeg" else extension

#         return extension

class VideoSerializer(serializers.ModelSerializer):
    # image = Base64ImageField(
    #     max_length=None, use_url=True,
    # )

    class Meta:
        model = UploadVideo
        fields = [
            # 'user', 
            'videoname', 
            'video',
            # 'image',
            # 'about',
            ]

class CommentVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentVideo
        fields = [
            'user', 
            'uploadedvideo', 
            'comment',
            ]

    # def get_comments(self, tweet_id):
    #     comment_query  = Comment.objects.filter(
    #             id=tweet_id)
    #     tweets_comments = CommentSerializer(comment_query, many=True)
    #     return tweets_comments

    # def get_comments_count(self,obj):
    #     return obj.tweets_comments.count()



    # def get_image(self, obj):
    #     try:
    #         image = obj.image.url
    #     except:
    #         image = None
    #     return image 
        
