from django.shortcuts import render,redirect
from social_web.forms import LoginForm,UserRegistrationForm,PostsForm,ProfileForm
from django.views.generic import CreateView,FormView,TemplateView,ListView,UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from social.models import Posts,Comments,Userprofile,Friends
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

decs=[signin_required,never_cache]

# Create your views here.
class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")

class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self,request,*args,**kwargs):
       form=LoginForm(request.POST)
       if form.is_valid():
           uname=form.cleaned_data.get("username")
           pwd=form.cleaned_data.get("password")
           usr=authenticate(request,username=uname,password=pwd)
           if usr:
            login(request,usr)
            return redirect("index")
           else:
            return render(request,self.template_name,{"form":"form"})

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostsForm
    success_url=reverse_lazy("index")
    model=Posts
    context_object_name="posts"


    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"your post added successfully")
        return super().form_valid(form)

    def get_queryset(self):
       return Posts.objects.exclude(user=self.request.user).order_by("-created_date")

decs
def add_comment(request,*args,**kwargs):
    id=kwargs.get("id")
    pos=Posts.objects.get(id=id)
    comment=request.POST.get("comment")
    Comments.objects.create(post=pos,comment=comment,user=request.user)
    messages.success(request,"your comment posted successfully")
    return redirect("index")

decs
def post_like_view(request,*args,**kwargs):
    id=kwargs.get("id")
    pos=Posts.objects.get(id=id)
    pos.liked_by.add(request.user)
    return redirect("index")


decs
def comment_like_view(request,*args,**kwargs):
    id=kwargs.get("id")
    com=Comments.objects.get(id=id)
    com.liked_by.add(request.user)
    return redirect("index")


def signout_view(request,*args,**kw):
    logout(request)
    return redirect("signin")


class ProfileView(CreateView,ListView):
    template_name="myprofilepost.html"
    form_class=PostsForm
    model=Posts
    success_url=reverse_lazy("index")
    context_object_name="posts"
    queryset=Posts.objects.all()

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user).order_by("-created_date")


class AddProfileView(CreateView):
    template_name="profile.html"
    form_class=ProfileForm
    success_url=reverse_lazy("index")
    
    # queryset=Posts.objects.all()

    # def get_queryset(self):
    #     return Posts.objects.filter(user=self.request.user).order_by("-created_date")
    

    def post(self, request,*args,**kw):
        
        form=ProfileForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect("index")
        else:
            return render(request,"profile.html",{"form":form})


class ViewmyProfileView(TemplateView):
    template_name="profileview.html"


decs
def post_delete(request,*args,**kw):
    id=kw.get("id")
    Posts.objects.get(id=id).delete()

    return redirect("index")

class EditprofileView(UpdateView):
    template_name="edit.html"
    form_class=ProfileForm
    model=Userprofile
    pk_url_kwarg="id"
    success_url=reverse_lazy("listpost")


class ListPeopleView(ListView):
    template_name="peoples.html"
    model=User
    context_object_name = 'people'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        context["posts"] = Posts.objects.all().order_by('-created_date')
        return context
    

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)


def add_follower(request, *args, **kwargs):
    id = kwargs.get('id')
    usr = User.objects.get(id=id)
    if not Friends.objects.filter(user=usr, follower=request.user):
        Friends.objects.create(user=usr, follower=request.user)
    else:
        Friends.objects.get(user=usr, follower=request.user).delete()
    return redirect("people")

