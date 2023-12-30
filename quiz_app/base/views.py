import datetime
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from account.models import profile
from quiz.models import UserRank,Quiz,QuizSubmission,Question
from django.contrib.auth.decorators import login_required,user_passes_test
import math
from .models import Message
from django.db.models import Q
from django.contrib import messages

# Create your views here.

# def welcome(request):
#     return render(request,'home.html')

def home(request):
    leaderboard_users=UserRank.objects.order_by('rank')[:4]
    if request.user.is_authenticated:
        user_object=User.objects.get(username=request.user)
        user_profile=profile.objects.get(user=user_object)
        context={"user_profile":user_profile,"leaderboard_users":leaderboard_users}
    else:
        context={"leaderboard_users":leaderboard_users}
    return render(request,'home.html',context)

@login_required(login_url='login')
def leader_view(request):
    leaderboard_users=UserRank.objects.order_by('rank')

    user_object=User.objects.get(username=request.user)
    user_profile=profile.objects.get(user=user_object)

    context={"user_profile":user_profile,"leaderboard_users":leaderboard_users}
    return render(request,"leaderboard.html",context)

def is_superuser(user):
    return user.is_superuser



@login_required(login_url='login')
@user_passes_test(is_superuser)
def dashboard_view(request):
    user_object=User.objects.get(username=request.user)
    user_profile=profile.objects.get(user=user_object)

    total_users=User.objects.all().count()
    
    total_quizzes=Quiz.objects.all().count()
    
    total_quiz_submit=QuizSubmission.objects.all().count()
    
    total_questions=Question.objects.all().count()



    today_users = User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_objs = Quiz.objects.filter(created_at__date=datetime.date.today())
    today_quizzes = Quiz.objects.filter(created_at__date=datetime.date.today()).count()
    today_quiz_submit = QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()
    today_questions = 0
    for quiz in today_quizzes_objs:
        today_questions += quiz.question_set.count()


    gain_users = gain_percentage(total_users, today_users)
    gain_quizzes = gain_percentage(total_quizzes, today_quizzes)
    gain_quiz_submit = gain_percentage(total_quiz_submit, today_quiz_submit)
    gain_questions = gain_percentage(total_questions, today_questions)

    messages = Message.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')
    
    context={"user_profile":user_profile,
             "total_users":total_users,
             "total_quizzes":total_quizzes,
             "total_quiz_submit":total_quiz_submit,
             "total_questions":total_questions,
             "today_users":today_users,
               "today_quizzes":today_quizzes,
               "today_quiz_submit":today_quiz_submit,
               "today_questions":today_questions,
               "gain_users": gain_users,
               "gain_quizzes": gain_quizzes,
               "gain_quiz_submit": gain_quiz_submit,
               "gain_questions": gain_questions,
               "messages": messages,
             }


   
    return render(request,"dashboard.html",context)

def gain_percentage(total, today):
    if total > 0 and today > 0:
        gain = math.floor((today *100)/total)
        return gain
    
def about_view(request):
    if request.user.is_authenticated:
        user_object=User.objects.get(username=request.user)
        user_profile=profile.objects.get(user=user_object)
        context={"user_profile":user_profile}
    else:
        context={}
    
    return render(request,"about.html",context)

def blogs_view(request):
    if request.user.is_authenticated:
        user_object=User.objects.get(username=request.user)
        user_profile=profile.objects.get(user=user_object)
        context={"user_profile":user_profile}
    else:
        context={}
    
    return render(request,"blogs.html",context)

@login_required(login_url='login')
def blog_view(request,blog_id):
    
    user_object=User.objects.get(username=request.user)
    user_profile=profile.objects.get(user=user_object)

    context={"user_profile":user_profile}
    
    
    return render(request,"blog.html",context)


@login_required(login_url='login')
def contact_view(request):
    user_object=User.objects.get(username=request.user)
    user_profile=profile.objects.get(user=user_object)

    if request.method=='POST':
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        if subject is not None and message is not None:
            form =Message.objects.create(user=request.user,subject=subject,message=message)
            form.save()
            messages.success(request,"we got your message. we will resolve your query")
            return redirect("user_profile",request.user.username)
        else:
            return redirect('contact')

    context={"user_profile":user_profile}
    
    
    return render(request,"contact.html",context)

def term_conditions_view(request):
    if request.user.is_authenticated:
        user_object=User.objects.get(username=request.user)
        user_profile=profile.objects.get(user=user_object)
        context={"user_profile":user_profile}
    else:
        context={}
    
    return render(request,"term-conditions.html",context)

@login_required(login_url='login')
def downloads_view(request):
    user_object=User.objects.get(username=request.user)
    user_profile=profile.objects.get(user=user_object)

    context={"user_profile":user_profile}
    
    
    return render(request,"downloads.html",context)

@user_passes_test(is_superuser)
@login_required(login_url='login')
def message_view(request, id):

    user_object = User.objects.get(username=request.user)
    user_profile = profile.objects.get(user=user_object)

    message = Message.objects.filter(id=int(id)).first()
    if not message.is_read:
        message.is_read = True
        message.save()

    context = {"user_profile": user_profile, "message": message}
    return render(request, "message.html", context)


def search_view(request):

    query=request.GET.get('q')
    if query:
        users=User.objects.filter(
            Q(username__icontains=query)|Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).order_by('-date_joined')
        
        
    else:
        users=[]

    if request.user.is_authenticated:
        user_object=User.objects.get(username=request.user)
        user_profile=profile.objects.get(user=user_object)
        context={"user_profile":user_profile,"query":query,"users":users}
    else:
        context={"query":query,"users":users}
    return render(request,"search-user.html",context)