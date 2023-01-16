from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from social_web.views import SignInView,SignUpView,IndexView,add_comment,post_like_view,signout_view,AddProfileView,ViewmyProfileView,ProfileView,post_delete,EditprofileView,add_follower,ListPeopleView,comment_like_view

urlpatterns = [
    path("register",SignUpView.as_view(),name="signup"),
    path("login",SignInView.as_view(),name="signin"),
    path("index",IndexView.as_view(),name="index"),
    path("posts/<int:id>/comments/add",add_comment,name="add-comment"),
    path("posts/<int:id>/likes/add",post_like_view,name="add-like"),
    path("comments/<int:id>/likes/add",comment_like_view,name="add-likes"),
    path("logout",signout_view,name="sign-out"),
    path("postprofile",ProfileView.as_view(),name="myprofilepost"),
    path("profile",AddProfileView.as_view(),name="profile"),
    path("myprofile",ViewmyProfileView.as_view(),name="myprofile"),
    path("post/<int:id>/remove",post_delete,name="post-delete"),
    path("users/profile/<int:id>/change",EditprofileView.as_view(),name="edit-profile"),
    path("user/<int:id>/follower/add",add_follower, name="add-follower"),
    path("people/", ListPeopleView.as_view(),name="people"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)