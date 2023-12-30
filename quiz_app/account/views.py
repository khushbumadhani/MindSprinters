from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import profile
from quiz.models import QuizSubmission
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def submit(request):
      if request.user.is_authenticated:
          return redirect('user_profile',request.user.username)
      if request.method=='POST':
            username=request.POST['username']
            user_email=request.POST['email']
            password=request.POST['password']
            password2=request.POST['password2']

            if password== password2:
                  if User.objects.filter(email=user_email).exists():
                        messages.info(request,"Email-id already used.Try to login")
                        return render(request,'register.html')
                  elif User.objects.filter(username=username).exists():
                        messages.info(request,"Username already taken")
                        return render(request,'register.html')
                  else:
                        #create user
                        user=User.objects.create_user(username=username,email=user_email,password=password)
                        user.save()
                        #login user and direct to profile page
                        user_login=auth.authenticate(username=username,password=password)
                        auth.login(request,user_login)

                        #profile page for loged user
                        user_model=User.objects.get(username=username)
                        new_profile=profile.objects.create(user=user_model)
                        new_profile.save()
                        return redirect('user_profile',user_model.username)

            else:
                  messages.info(request,"password not matching")
                  return redirect('submit')
            
      return render(request,"register.html")



def login(request):
      if request.user.is_authenticated:
          return redirect('user_profile',request.user.username)
      if request.method=='POST':
            username=request.POST["username"]
            password=request.POST["password"]



            user=auth.authenticate(username=username,password=password)
            if user is not None:
                  auth.login(request,user)
                  return redirect('user_profile',username)
            
            else:
                  messages.info(request,"credentials invalid")

      return render(request,"login.html")


@login_required(login_url='login')
def user_profiles(request,username):
      user_object2=User.objects.get(username=username)
      user_profile2=profile.objects.get(user=user_object2)

      user_object=User.objects.get(username=request.user)
      user_profile=profile.objects.get(user=user_object)

      submissions=QuizSubmission.objects.filter(user=user_object2)

      context= {"user_profile": user_profile,"user_profile2": user_profile2,"submissions":submissions}
      return render(request,"profile.html",context)


@login_required(login_url='login')
def logout(request):
      auth.logout(request)
      return redirect('home')


@login_required(login_url='login')
def edit(request):

      user_object=User.objects.get(username=request.user)
      user_profile=profile.objects.get(user=user_object)

      if request.method=="POST":
            if request.FILES.get('profile_img')!=None:
                  user_profile.profile_img=request.FILES.get('profile_img')
                  user_profile.save()

            if request.POST.get('email')!=None:
                  u=User.objects.filter(email=request.POST.get('email')).first()

                  if u==None:
                        user_object.email=request.POST.get('email')
                        user_object.save()
                  else:
                        if u!=user_object:
                              messages.info(request,"Email Already used,choose a different one")
                              return redirect('edit')
                        
            if request.POST.get('username')!=None:
                  u=User.objects.filter(username=request.POST.get('username')).first()

                  if u==None:
                        user_object.username=request.POST.get('username')
                        user_object.save()
                  else:
                        if u!=user_object:
                              messages.info(request,"username Already used,choose a different one")
                              return redirect('edit')
            
            user_object.first_name=request.POST.get('first_name')
            user_object.last_name=request.POST.get('last_name')
            user_object.save()

            user_profile.location=request.POST.get('location')
            user_profile.gender=request.POST.get('gender')
            user_profile.bio=request.POST.get('bio')
            user_profile.save()
            return redirect('user_profile',user_object.username)
                 
      
      context={"user_profile": user_profile}
      return render(request,'profile_edit.html',context)

@login_required(login_url='login')
def delete(request):

      user_object=User.objects.get(username=request.user)
      user_profile=profile.objects.get(user=user_object)
      if request.method=="POST":
            user_profile.delete()
            user_object.delete()
            return redirect('logout') 

      context={"user_profile":user_profile}
      return render(request,'confirm.html',context)

