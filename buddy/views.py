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


    return render(request, 'profile.html', {'profile': profile})




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
    return render(request, 'update_profile.html', {
        "user_form": user_form,
        "profile_form": profile_form,
        'gym_name': gym_name
    })


@login_required(login_url='/accounts/login/')
def hood(request,hood_id):
    current_user = request.user
    hood_name = current_user.profile.hood
    # if current_user.profile.hood is None:
    #     return redirect('update')
    # else:
    hood = Post.get_hood_posts(id = hood_id)
    comments = Comment.objects.all()
    form = NewComment(instance=request.user)

    return render(request,'hood.html',{'hood':hood,'hood_name':hood_name,'comments':comments,'comment_form':form})

def join(request,id):
    current_user = request.user
    hood_name = current_user.profile.hood
    hood = Hood.objects.get(id=id)
    current_user.profile.hood = hood
    current_user.profile.save()

    return redirect('index')

def exit(request,id):
    current_user = request.user
    # hood_name = current_user.profile.hood
    # hood = Hood.objects.get(id=id)
    current_user.profile.hood = None
    current_user.profile.save()

    return redirect('index')


@login_required(login_url='/accounts/login/')
def newhood(request):
    current_user = request.user
    hood_name = current_user.profile.hood
    if request.method == 'POST':
        NewHoodForm = NewHood(request.POST)
        if NewHoodForm.is_valid():
            hoodform = NewHoodForm.save(commit=False)
            hoodform.admin = current_user
            current_user.profile.hoodpin = True
            hoodform.save()
            print('saved')

            # request.session.modified = True
            # current_user.profile.hood = hoodform.id
        # return redirect('profilehood',hoodform.name)
        return redirect('index')


    else:
        NewHoodForm = NewHood()
    return render(request, 'newhood.html', {"newHoodForm": NewHoodForm,
                                            'hood_name': hood_name})


def profilehood(request,name):
    current_user = request.user
    hood_name = current_user.profile.hood
    hoodform = Hood.objects.get(name = name)
    current_user.profile.hood = hoodform.id
    current_user.profile.hoodpin = True

    return redirect('index')