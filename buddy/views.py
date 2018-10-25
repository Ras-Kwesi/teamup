from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import *
from .forms import *

# Create your views here.
def index(request):
    current_user = request.user
    # if current_user.profile.hood is None:
        # hoods = Hood.objects.all()
        # return redirect('communities')

    # else:
        # return redirect('/hood/',hood_id =hood_id)


    # posts = Post.objects.all()


    return render(request,'index.html',{})



@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user

    profile = Profile.objects.get(user=current_user)
    print(profile)
    posts = Post.objects.filter(poster = current_user)
    chatrooms = current_user.profile.chatroom.all()
    print(chatrooms)
    # profile = Profile.objects.filter(user=request.user.id)

    return render(request, 'profile/profile.html', {'profile': profile,'posts':posts,'chatrooms':chatrooms})


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
def chatroom(request,room_id):
    current_user = request.user
    form = ChatPostForm()

    chatroom = get_object_or_404(Chatroom,pk=room_id)
    chatrooms = request.user.profile.chatroom.all()
    print(chatroom)
    posts = Post.objects.filter(chatroom=chatroom)
    if chatroom in chatrooms:
        r = chatroom
        return render(request, 'chatroom.html', {'chatroom': r,'form':form})

    # for room in chatrooms:
    #     r = None
    #     if room == chatroom.id:
    #         r = room
    #         print(chatroom.id)
    #     return r
    #     print(r)

    #     return redirect('update')
    # else:
    # hood = Post.get_hood_posts(id = hood_id)
    posts = Post.objects.filter(chatroom = chatroom)
    # form = PostForm()

    # return render(request,'chatroom.html',{'chatroom':r})


# def post(request, id):
#     chatroom = Chatroom.objects.get(id=id)
#     print(id)
#     if request.method == 'POST':
#         post = PostForm(request.POST)
#         if post.is_valid():
#             posting = post.save(commit=False)
#             posting.poster = request.user
#             posting.chatroom = chatroom
#             posting.save()
#             return redirect('index')
#     return redirect('index')

def post(request, id):
    chatroom = Chatroom.objects.get(id=id)
    print(id)
    # new_post = Post()
    if request.method == 'POST':
        newpost = ChatPostForm(request.POST,request.FILES)
        if newpost.is_valid():
            newpost.save(commit=False)
            newpost.poster = request.user
            newpost.chatroom = chatroom
            newpost.save()
        return redirect('index')







def joingym(request,id):
    current_user = request.user
    # hood_name = current_user.profile.hood
    gym = Gym.objects.get(id=id)
    current_user.profile.mygym = gym
    current_user.profile.save()

    return redirect('index')


def comment(request,id):
    post = Post.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        comm=NewComment(request.POST)
        if comm.is_valid():
            comment=comm.save(commit=False)
            comment.commentator = request.user
            comment.comment_post = post
            comment.save()
            return redirect('index')
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

def chatrooms(request):
    current_user = request.user
    chatrooms = Chatroom.objects.all()

    return render(request,'chatrooms.html',{'chatrooms':chatrooms})


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
        # return redirect('profilehood' + hoodform.name)
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
            gymform.owner = current_user
            gymform.save()
            print('saved')

            # request.session.modified = True
            # current_user.profile.hood = hoodform.id
        # return redirect('profilehood',hoodform.name)
        return redirect('index')


    else:
        NewGymForm = RegGym()
    return render(request,'forms/newgym.html', {"newGymForm": NewGymForm})



def change_friends(request,operation,pk):
    new_friend = User.objects.get(pk = pk)
    if operation == 'addfriend':
        Friend.addfriend(request.user,new_friend)
    elif operation == 'removefriend':
        Friend.removefriend(request.user,new_friend)



def joinchat(request,id):
    current_user = request.user
    chat = Chatroom.objects.get(id=id)
    current_user.profile.addchatroom(current_user,chat)
    current_user.profile.save()

    return redirect('index')

def forms(request):
    NewGymForm = RegGym()
    NewChatForm = ChatForm()

    return render(request,'forms/forms.html',{'newGymForm':NewGymForm,'newChatForm':NewChatForm})