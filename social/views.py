from django.shortcuts import render
from social.serializers import UserSerializer,PostSerializer,CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from social.models import Posts,Comments
from rest_framework import authentication,permissions
from rest_framework.decorators import action
# Create your views here.



class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class PostView(ModelViewSet):
    serializer_class=PostSerializer
    queryset=Posts.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


    @action(methods=["GET"],detail=False)
    def my_posts(self,request,*args,**kw):
        qs=request.user.posts_set.all()
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["POST"],detail=True)
    def add_comment(self,request,*args,**kw):
        id=kw.get("pk")
        pos=Posts.objects.get(id=id)
        usr=request.user
        serializer=CommentSerializer(data=request.data,context={"post":pos,"user":usr})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["GET"],detail=True)
    def list_comment(self,request,*args,**kw):
        id=kw.get("pk")
        pos=Posts.objects.get(id=id)
        po=pos.comments_set.all()
        serializer=CommentSerializer(po,many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"],detail=True)
    def liked_by(self,request,*args,**kw):
        pos=self.get_object()
        usr=request.user
        pos.liked_by.add(usr)
        return Response(data="liked")

