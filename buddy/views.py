from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import *
from .forms import *

# Create your views here.
@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user

    profile = Profile.objects.get(user=current_user)
    print(profile)
    # profile = Profile.objects.filter(user=request.user.id)


    return render(request, 'profile/profile.html', {'profile': profile})




@login_required(login_url='/accounts/login/')
@transaction.atomic
def update(request):
    # current_user = User.objects.get(pk=user_id)
    current_user=request.user
    gym_name = current_user.profile.mygym
    if request.method == 'POST':
        user_form = EditUser(request.POST, request.FILES,instance=request.user)
        profile_form = EditProfile(request.POST, request.FILES,instance=current_user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
        return redirect('profile')

    else:
        user_form = EditUser(instance=request.user)
        profile_form = EditProfile(instance=current_user.profile)
    return render(request, 'profile/update_profile.html', {
        "user_form": user_form,
        "profile_form": profile_form,
        'gym_name': gym_name
    })


@login_required(login_url='/accounts/login/')
def chatroom(request,hood_id):
    current_user = request.user
    gym_name = current_user.profile.hood
    # if current_user.profile.hood is None:
    #     return redirect('update')
    # else:
    hood = Post.get_hood_posts(id = hood_id)
    comments = Comment.objects.all()
    form = PostForm()

    return render(request,'hood.html',{'hood':hood,'gym_name':gym_name,'comments':comments,'comment_form':form})

def post(request, id):
    chatroom = Chatroom.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        post = PostForm(request.POST)
        if post.is_valid():
            posting = post.save(commit=False)
            posting.poster = request.user
            posting.chatroom = chatroom
            posting.save()
            return redirect('index')
    return redirect('index')


def joinchat(request,id):
    current_user = request.user
    chat = Chatroom.objects.get(id=id)

    current_user.profile.save()

    return redirect('index')


def joingym(request,id):
    current_user = request.user
    hood_name = current_user.profile.hood
    chat = Chatroom.objects.get(id=id)
    current_user.profile. = hood
    current_user.profile.save()

    return redirect('index')



def exitgym(request,id):
    current_user = request.user
    # hood_name = current_user.profile.hood
    # hood = Hood.objects.get(id=id)
    current_user.profile.mygym = None
    current_user.profile.save()

    return redirect('index')


def exitchatroom(request,id):
    current_user = request.user
    # hood_name = current_user.profile.hood
    # hood = Hood.objects.get(id=id)
    current_user.profile.chatroom = None
    current_user.profile.save()

    return redirect('index')


@login_required(login_url='/accounts/login/')
def newchatroom(request):
    current_user = request.user
    if request.method == 'POST':
        NewChatForm = ChatForm(request.POST)
        if NewChatForm.is_valid():
            chatform = NewChatForm.save(commit=False)
            chatform.admin = current_user
            chatform.save()
            print('saved')

            # request.session.modified = True
            # current_user.profile.hood = hoodform.id
        # return redirect('profilehood',hoodform.name)
        return redirect('index')


    else:
        NewChatForm = ChatForm()
    return render(request, 'forms/newchat.html', {"newChatForm": NewChatForm})


def profilechatrooms(request):
    current_user = request.user
    chatrooms = current_user.profile.chatroom.all()

    return redirect('index')


@login_required(login_url='/accounts/login/')
def newgym(request):
    current_user = request.user
    if request.method == 'POST':
        NewGymForm = RegGym(request.POST)
        if NewGymForm.is_valid():
            gymform = NewGymForm.save(commit=False)
            gymform.admin = current_user
            gymform.save()
            print('saved')

            # request.session.modified = True
            # current_user.profile.hood = hoodform.id
        # return redirect('profilehood',hoodform.name)
        return redirect('index')


    else:
        NewGymForm = RegGym()
    return render(request, 'newhood.html', {"newGymForm": NewGymForm})
