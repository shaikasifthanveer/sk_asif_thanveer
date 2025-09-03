from django.shortcuts import render,redirect
from django.http import HttpResponse
from CgpaApp.forms import Reg
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from CgpaProject import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request,'home.html',{})

def register(request):
    if request.method=="POST":
        form=Reg(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("<h2>Registration Successfull</h2>")
    form=Reg()
    return render(request,'register.html',{'info':form})

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('signin')
    else:
        form = CreateUserForm()
    return render(request, 'signup.html', {'form': form})

def login_views(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('cgpa')
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'signin.html',{})

def mail(request):
    if request.method=="POST":
        rcr=request.POST['sat']
        sb=request.POST['sbj']
        m=request.POST['msg']
        t=settings.EMAIL_HOST_USER
        res=send_mail(sb,m,t,[rcr])
        if res==1:
            messages.success(request, "Mail Sent")
        else:
            messages.error(request, "Mail not sent")
        return redirect('mail')
    
    return render(request,'mail.html',{})

GRADE_MAP = {
    'O': 10,
    'A': 9,
    'B': 8,
    'C': 7,
    'D': 6,
    'E': 5,
    'F': 0
}

def cgpa_cal(request):
    semesters = list(range(1, 9))
    grade_choices = GRADE_MAP.items()
    values = {}
    overall_cgpa = None

    if request.method == 'POST':
        selected_sems = request.POST.getlist('semesters')
        values['selected_sems'] = selected_sems
        sem_data = {}

        total_credits = 0
        total_points = 0

        for sem in selected_sems:
            num_subjects = int(request.POST.get(f'subject_count_{sem}', '0'))
            subjects = []

            for i in range(1, num_subjects + 1):
                grade = request.POST.get(f'grade_{sem}_{i}', '')
                credit = request.POST.get(f'credit_{sem}_{i}', '')
                if credit.isdigit():
                    credit_int = int(credit)
                    subjects.append({'grade': grade, 'credit': credit})
                    if grade in GRADE_MAP:
                        total_credits += credit_int
                        total_points += GRADE_MAP[grade] * credit_int
                else:
                    subjects.append({'grade': grade, 'credit': ''})

            sem_data[str(sem)] = {
                'num_subjects': num_subjects,
                'subjects': subjects
            }

        values['sem_data'] = sem_data

        if total_credits > 0:
            overall_cgpa = round(total_points / total_credits, 2)

    return render(request, 'cgpa.html', {
        'semesters': semesters,
        'grade_choices': grade_choices,
        'values': values,
        'overall_cgpa': overall_cgpa
    })

