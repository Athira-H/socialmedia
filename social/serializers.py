from rest_framework import serializers
from django.contrib.auth.models import User
from social.models import Posts,Comments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id",
            "username",
            "email",
           "password"
        ]
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    post=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)

    class Meta:
        model=Comments
        fields=[
            "post",
            "comment",
            "user",
            "created_date"
        ]
    def create(self,validated_data):
        pos=self.context.get("post")
        usr=self.context.get("user")
        return pos.comments_set.create(user=usr,**validated_data)

class PostSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    post_comments=CommentSerializer(read_only=True,many=True)
    # likecount=serializers.CharField(read_only=True)

    class Meta:
        model=Posts
        fields=[
            "id",
            "title",
            "image",
            "user",
            "post_comments"
            # "likecount"
        ]



