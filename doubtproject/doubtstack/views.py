from django.shortcuts import render, redirect

def home(request):
    return render(request, 'index/home.html')


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegisterNumberForm, OTPForm, PasswordForm
from .models import Student, Teacher, OTPVerification
from .models import LoginDB, LoginDB2  # your college databases
import datetime

# Landing page
def index(request):
    number_form = RegisterNumberForm()
    return render(request, 'index/landing.html', {'number_form': number_form})

def student_dashboard(request):
    return render(request, 'student/studenthome.html')

def teacher_dashboard(request):
    return render(request, 'teacher/teacherhome.html')

# Step 1: Verify register number
def verify_number(request):
    if request.method == "POST":
        reg_no = request.POST.get('reg_no')
        # 1. Check if user exists in system
        if Student.objects.filter(student_id=reg_no).exists():
            return redirect('student_password', reg_no=reg_no)
        elif Teacher.objects.filter(teacher_id=reg_no).exists():
            return redirect('teacher_password', reg_no=reg_no)
        # 2. If not, check college DB
        student_college = LoginDB.objects.filter(adm_no=reg_no).first()
        teacher_college = LoginDB2.objects.filter(tchr_no=reg_no).first()
        if student_college or teacher_college:
            request.session['reg_no'] = reg_no
            return redirect('permission')
        messages.error(request, "Register/Staff number not found.")
        return redirect('index')
    return redirect('index')

# Step 2: Ask permission to create account
def permission(request):
    reg_no = request.session.get('reg_no')
    if request.method == "POST":
        if request.POST.get('permission') == 'yes':
            # Generate OTP
            student_college = LoginDB.objects.filter(adm_no=reg_no).first()
            teacher_college = LoginDB2.objects.filter(tchr_no=reg_no).first()
            email = student_college.stu_email if student_college else teacher_college.tchr_email
            otp_obj = OTPVerification(reg_no=reg_no)
            otp = otp_obj.generate_otp()
            otp_obj.save()
            send_mail(
                'DoubtStack OTP Verification',
                f'Your OTP is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )
            return redirect('verify_otp')
        else:
            messages.info(request, "Account creation cancelled.")
            return redirect('index')
    return render(request, 'index/permission.html', {'reg_no': reg_no})

# Step 3: OTP verification
def verify_otp(request):
    reg_no = request.session.get('reg_no')
    otp_form = OTPForm()  # Create a form instance

    if request.method == "POST":
        otp_form = OTPForm(request.POST)
        if otp_form.is_valid():
            otp_input = otp_form.cleaned_data['otp']
            otp_obj = OTPVerification.objects.filter(reg_no=reg_no).last()
            if otp_obj and otp_obj.otp == otp_input:
                otp_obj.delete()
                return redirect('set_password')
            else:
                messages.error(request, "Invalid OTP")
                return redirect('verify_otp')

    return render(request, 'index/verify_otp.html', {'reg_no': reg_no, 'otp_form': otp_form})

# Step 4: Set password and create profile
def set_password(request):
    reg_no = request.session.get('reg_no')
    password_form = PasswordForm()  # create form instance

    if request.method == "POST":
        password_form = PasswordForm(request.POST)
        if password_form.is_valid():
            password = password_form.cleaned_data['password']
            confirm_password = password_form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('set_password')

            # Fetch details from college DB
            student_college = LoginDB.objects.filter(adm_no=reg_no).first()
            teacher_college = LoginDB2.objects.filter(tchr_no=reg_no).first()

            if student_college:
                Student.objects.create(
                    student_id=student_college.adm_no,
                    username=str(student_college.adm_no),
                    password=make_password(password),
                    name=student_college.stu_name,
                    department=student_college.stu_branch,
                    semester=calculate_sem(student_college.stu_start_year, student_college.stu_end_year)
                )
                return redirect('index')

            elif teacher_college:
                Teacher.objects.create(
                    teacher_id=teacher_college.tchr_no,
                    username=str(teacher_college.tchr_no),
                    password=make_password(password),
                    name=teacher_college.tchr_name,
                    department=teacher_college.tchr_dept,
                    role=teacher_college.tchr_role
                )
                return redirect('index')

    return render(request, 'index/set_password.html', {'password_form': password_form, 'reg_no': reg_no})

# Helper: Calculate semester
import datetime

def calculate_sem(start_year, end_year=None):
    """
    Calculate the current semester for MCA (4 semesters) based on start_year.
    Semesters:
      Sep-Feb   -> 1
      Feb-Jun   -> 2
      Jun-Dec   -> 3
      Dec-May   -> 4
    """
    today = datetime.date.today()
    start_year = int(start_year)
    
    # Determine months
    month = today.month
    year_diff = today.year - start_year

    # Base semester according to year_diff
    # Each academic year has 2 semesters
    base_sem = year_diff * 2

    # Adjust according to current month
    if 9 <= month <= 2 or month == 1 or month == 2:   # Sep-Feb
        sem_offset = 1
    elif 2 < month <= 6:  # Mar-Jun
        sem_offset = 2
    elif 6 < month <= 12:  # Jul-Dec
        sem_offset = 3
    else:
        sem_offset = 4

    semester = base_sem + sem_offset

    # Cap at 4 semesters for MCA
    if semester > 4:
        semester = 4
    elif semester < 1:
        semester = 1

    return semester


# Password login for existing users
def student_password(request, reg_no):
    if request.method == "POST":
        password = request.POST.get('password')
        student = Student.objects.get(student_id=reg_no)
        if check_password(password, student.password):
            # login session
            request.session['user_id'] = student.student_id
            request.session['user_type'] = 'student'
            return redirect('student_dashboard')
        messages.error(request, "Invalid password")
    return render(request, 'index/password_login.html', {'reg_no': reg_no, 'user_type': 'student'})

def teacher_password(request, reg_no):
    if request.method == "POST":
        password = request.POST.get('password')
        teacher = Teacher.objects.get(teacher_id=reg_no)
        if check_password(password, teacher.password):
            request.session['user_id'] = teacher.teacher_id
            request.session['user_type'] = 'teacher'
            return redirect('teacher_dashboard')
        messages.error(request, "Invalid password")
    return render(request, 'index/password_login.html', {'reg_no': reg_no, 'user_type': 'teacher'})



