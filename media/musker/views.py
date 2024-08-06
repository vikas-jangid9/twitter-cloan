from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.models import User

def home(request):
    meeps = Meep.objects.all().order_by("-created_at")
    if request.user.is_authenticated:
        forms = MeepForm(request.POST or None)
        if forms.is_valid():
            meep = forms.save(commit=False)
            meep.user = request.user
            meep.save()
            messages.info(request, "Your Messages is posted...")
            return redirect('home')
        context = {'meeps':meeps, 'forms':forms}

    else:
        context = {'meeps':meeps}

    return render(request, 'musker/home.html', context)

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)

        context = { 'profiles':profiles }
        return render(request, 'musker/profile_list.html', context)
    
    else:
        messages.success(request, ("You must been logged In to see this page........"))
        return redirect('login')

def unfollow(request, pk):
    if request.user.is_authenticated:
        # get profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # unfollow the user
        request.user.profile.follows.remove(profile)

        request.user.profile.save()

        messages.success(request, (f"Unfollow the profile : { profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must been logged In to see this page........"))
        return redirect('login')
    
def follow(request, pk):
    if request.user.is_authenticated:
        # get profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # unfollow the user
        request.user.profile.follows.add(profile)

        request.user.profile.save()

        messages.success(request, (f"Follow the profile : { profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must been logged In to see this page........"))
        return redirect('login')


def followed(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)

            context = { 'profiles':profiles }
            return render(request, 'musker/followed.html', context)
        else:
            messages.success(request, ("That 's Not Your Profile page......."))
            return redirect('home')
    
    else:
        messages.success(request, ("You must been logged In to see this page........"))
        return redirect('login')
    

def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)

            context = { 'profiles':profiles }
            return render(request, 'musker/followers.html', context)
        else:
            messages.success(request, ("That 's Not Your Profile page......."))
            return redirect('home')
    
    else:
        messages.success(request, ("You must been logged In to see this page........"))
        return redirect('login')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")


        if request.method == "POST":
            #get current user
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
            #delete to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            #save the profile
            current_user_profile.save()

        context = {'profile':profile, 'meeps':meeps}
        return render(request, "musker/profile.html", context)
    
    else:
        messages.success(request, ("You must been logged In to see this page........"))
        return redirect('login')
    

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been Logged In!..."))
            return redirect('home')
        else:
            messages.success(request, ("You have enter wrong  something!..."))
            return redirect('login')
    else:
        return render(request, 'musker/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("Your account is logout...."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have register now")) 
            return redirect('home')
    return render(request, 'musker/register.html', {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user_id=request.user.id)
        form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("Your Profile Has Been Updated **"))
        return render(request, 'musker/update_user.html', {'form':form, 'profile_form':profile_form})
    else:
        messages.success(request, ("You must been logged In to see this page........"))
        return redirect('home')
    
def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)

        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must been logged In to see this page........"))
        return redirect('home')
    
def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, "musker/meep_page.html", {'meep':meep})
    else:
        messages.success(request, ("This page does not exist........"))
        return redirect('home')
    

def delete_meep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if request.user.username == meep.user.username:
            meep.delete()
            messages.success(request, ("That's post is deleted"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("You don't own that post"))
            return redirect('home')

    else:
        messages.success(request, ("You must been logged In...."))
        return redirect('login')
    

def edit_meep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if request.user.username == meep.user.username:
            form =MeepForm(request.POST or None, instance=meep)
            if request.method == 'POST':
                if form.is_valid():
                    meep = form.save(commit=False)
                    meep.user = request.user
                    meep.save()
                    messages.success(request, ("Your post has been edit"))
                    return redirect('home')
            else:    
                return render(request, 'musker/edit_meep.html', {'meep':meep, 'form':form} )
        else:
            messages.success(request, ("You don't own that post"))
            return redirect('home')

    else:
        messages.success(request, ("You must been logged In...."))
        return redirect('login')
    

def search(request):
    pass