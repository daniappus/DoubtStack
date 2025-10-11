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

# def student_dashboard(request):
#     return render(request, 'student/studenthome.html')

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
            request.session['student_id'] = student.student_id
            request.session['user_type'] = 'student'
            return redirect('student_dashboard')
        messages.error(request, "Invalid password")
    return render(request, 'index/password_login.html', {'reg_no': reg_no, 'user_type': 'student'})

def teacher_password(request, reg_no):
    if request.method == "POST":
        password = request.POST.get('password')
        teacher = Teacher.objects.get(teacher_id=reg_no)
        if check_password(password, teacher.password):
            request.session['teacher_id'] = teacher.teacher_id
            request.session['user_type'] = 'teacher'
            return redirect('teacher_dashboard')
        messages.error(request, "Invalid password")
    return render(request, 'index/password_login.html', {'reg_no': reg_no, 'user_type': 'teacher'})



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SubmitDoubtForm
from .models import Doubt, Subject, Student

def student_dashboard(request):
    # Get student_id from session
    st_id = request.session.get('student_id')
    if not st_id:
        return redirect('home')  # redirect to login if session is missing

    student = Student.objects.get(student_id=st_id)

    if request.method == 'POST':
        form = SubmitDoubtForm(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.student = student
            doubt.save()
            messages.success(request, 'Doubt submitted successfully!')
            return redirect('student_dashboard')
    else:
        form = SubmitDoubtForm()

    doubts = Doubt.objects.filter(student=student)
    subjects = Subject.objects.all()

    return render(request, 'student/studenthome.html', {
        'form': form,
        'doubts': doubts,
        'subjects': subjects
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.contrib import messages
from .models import Doubt, Subject, Vote, Student


# 🔹 View all doubts with filters and upvote count
def view_all_doubts(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please log in to view doubts.")
        return redirect('index')  # Change to your actual login URL name

    student = get_object_or_404(Student, student_id=student_id)

    # Base queryset with select_related to reduce DB hits
    doubts = (
        Doubt.objects.select_related('student', 'subject')
        .annotate(total_votes=Count('votes'))
        .order_by('-created_at')
    )

    # 🔹 Filters (optional via GET params)
    subject_id = request.GET.get('subject')
    status = request.GET.get('status')
    topic = request.GET.get('topic')

    if subject_id:
        doubts = doubts.filter(subject_id=subject_id)
    if status:
        doubts = doubts.filter(status=status)
    if topic:
        doubts = doubts.filter(topic__icontains=topic)

    subjects = Subject.objects.all()  # For dropdown filters

    # Pass context to template
    context = {
        'student': student,
        'doubts': doubts,
        'subjects': subjects,
    }

    return render(request, 'student/student_doubts.html', context)


# 🔹 Handle upvote logic
def upvote_doubt(request, doubt_id):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please log in to upvote.")
        return redirect('index')

    student = get_object_or_404(Student, student_id=student_id)
    doubt = get_object_or_404(Doubt, id=doubt_id)

    # Check if student already voted
    if Vote.objects.filter(doubt=doubt, student=student).exists():
        messages.warning(request, "You already upvoted this doubt.")
    else:
        Vote.objects.create(doubt=doubt, student=student)
        messages.success(request, "Upvoted successfully!")

    return redirect('view_all_doubts')


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Doubt, Reply, Student
from .forms import StudentReplyForm

def student_reply_chat(request, doubt_id):
    # 🧍‍♂️ Get logged-in student
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('index')

    student = get_object_or_404(Student, pk=student_id)
    doubt = get_object_or_404(Doubt, pk=doubt_id)
    replies = Reply.objects.filter(doubt=doubt).order_by('created_at')
    upvote_count = doubt.votes.count() if hasattr(doubt, 'votes') else 0

    # Check if it's an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # 📤 POST (sending a new reply)
    if request.method == 'POST':
        form = StudentReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.student = student
            reply.teacher = None
            reply.doubt = doubt
            
            # Determine reply_type based on file
            if reply.file_url:
                file_name = reply.file_url.name.lower()
                if file_name.endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    reply.reply_type = 'audio'
                elif file_name.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                    reply.reply_type = 'video'
                elif file_name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                    reply.reply_type = 'image'
                elif file_name.endswith(('.pdf',)):
                    reply.reply_type = 'pdf'
                elif file_name.endswith(('.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx')):
                    reply.reply_type = 'doc'
                else:
                    reply.reply_type = 'file'
            else:
                reply.reply_type = 'text'
            
            reply.save()
            
            # Always return JSON for POST requests in this view
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # 📥 GET AJAX fetch
    if is_ajax:
        reply_data = []
        for r in replies:
            # For student view, show "Anonymous" instead of actual name for anonymous posts
            if r.anonymous and r.student and not r.teacher:
                sender_name = "Anonymous"
            else:
                sender_name = (
                    'You'
                    if r.student and r.student.student_id == student_id
                    else (
                        r.teacher.name if r.teacher
                        else r.student.name if r.student
                        else 'Unknown'
                    )
                )
            
            reply_data.append({
                'id': r.reply_id,
                'text': r.reply_text,
                'file_url': r.file_url.url if r.file_url else None,
                'file_name': r.file_url.name if r.file_url else None,
                'reply_type': r.reply_type,
                'anonymous': r.anonymous,
                'sender': sender_name,
                'is_teacher': bool(r.teacher),
                'timestamp': r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'is_self': r.student and r.student.student_id == student_id,
            })
        return JsonResponse({'replies': reply_data})

    # 🖼️ Normal page render (only for non-AJAX GET requests)
    form = StudentReplyForm()
    context = {
        'doubt': doubt,
        'replies': replies,
        'form': form,
        'student_id': student_id,
        'upvote_count': upvote_count,
    }
    return render(request, 'student/doubt_chat.html', context)


from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Teacher, Subject, Doubt, Vote

def teacher_view_doubts(request):
    """
    Teacher dashboard: shows doubts for the teacher's assigned subjects.
    HOD (role == 'HOD') can view all doubts.
    Supports GET filters:
      - subject_id
      - status (unresolved/resolved/escalated)
      - sort (latest | votes)
    """
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('index')

    try:
        teacher = Teacher.objects.get(teacher_id=teacher_id)
    except Teacher.DoesNotExist:
        request.session.flush()
        return redirect('teacher_login')

    # Check if teacher is HOD
    is_hod = bool(teacher.role and teacher.role.strip().upper() == 'HOD')

    # Base queryset
    if is_hod:
        doubts_qs = Doubt.objects.all()
        subjects_qs = Subject.objects.all()
    else:
        subjects_qs = teacher.subjects.all()
        doubts_qs = Doubt.objects.filter(subject__in=subjects_qs)

    # Filters
    subject_id = request.GET.get('subject_id')
    status = request.GET.get('status')
    sort = request.GET.get('sort')

    if subject_id:
        try:
            sid = int(subject_id)
            if is_hod or subjects_qs.filter(id=sid).exists():
                doubts_qs = doubts_qs.filter(subject_id=sid)
            else:
                doubts_qs = doubts_qs.none()
        except ValueError:
            pass

    if status in [choice[0] for choice in Doubt.STATUS_CHOICES]:
        doubts_qs = doubts_qs.filter(status=status)

    # ✅ Annotate actual upvote count using Vote model
    doubts_qs = (
        doubts_qs.select_related('student', 'subject')
                 .annotate(votes_count=Count('votes', distinct=True))
    )

    # Sorting
    if sort == 'votes':
        doubts_qs = doubts_qs.order_by('-votes_count', '-created_at')
    else:
        doubts_qs = doubts_qs.order_by('-created_at')

    context = {
        'teacher': teacher,
        'subjects': subjects_qs,
        'doubts': doubts_qs,
        'is_hod': is_hod,
        'request': request,
    }
    return render(request, 'teacher/doubts.html', context)

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.conf import settings
from django.contrib import messages

from .models import Doubt, Reply, Teacher
from .forms import TeacherReplyForm


def teacher_reply_chat(request, doubt_id):
    """
    View a single doubt's chat (teacher side). Teachers can reply (text/file),
    optionally mark the doubt as resolved. Permission: only assigned teachers or HOD.
    Uses TeacherReplyForm for validation and file handling.
    """
    # session-based auth
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        messages.error(request, "Please sign in as a teacher to continue.")
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    doubt = get_object_or_404(Doubt, pk=doubt_id)

    # role check (normalize)
    is_hod = bool(teacher.role and teacher.role.strip().upper() == 'HOD')

    # permission: either HOD or the teacher assigned to the doubt's subject
    # Note: in your Subject model the FK is named `teacher_id`
    if not is_hod and doubt.subject.teacher_id != teacher:
        return HttpResponseForbidden("You are not authorized to access this doubt.")

    # fetch replies (ordered by created_at ascending thanks to model Meta)
    replies = doubt.replies.select_related('teacher', 'student').all()

    # upvotes for display
    try:
        upvotes = doubt.votes.count()
    except Exception:
        upvotes = 0

    # handle form submission
    if request.method == 'POST':
        form = TeacherReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.doubt = doubt
            reply.teacher = teacher

            # infer reply_type if not provided by form
            # (TeacherReplyForm doesn't include reply_type field in the suggested version)
            uploaded_file = getattr(reply, 'file_url', None) or request.FILES.get('file_url') or request.FILES.get('file')
            if uploaded_file:
                fname = uploaded_file.name.lower()
                if fname.endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    reply.reply_type = 'audio'
                elif fname.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                    reply.reply_type = 'video'
                elif fname.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                    reply.reply_type = 'image'
                elif fname.endswith(('.pdf',)):
                    reply.reply_type = 'pdf'
                elif fname.endswith(('.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx')):
                    reply.reply_type = 'doc'
                else:
                    reply.reply_type = 'file'
            else:
                # text-only
                reply.reply_type = 'text'

            # save reply
            reply.save()

            # If the form included a 'mark_resolved' custom field, read it from cleaned_data.
            mark_resolved = form.cleaned_data.get('mark_resolved') if hasattr(form, 'cleaned_data') else False
            if mark_resolved:
                doubt.status = 'resolved'
                doubt.save(update_fields=['status'])

            messages.success(request, "Reply posted successfully.")
            return redirect('teacher_reply_chat', doubt_id=doubt.id)
        else:
            # form invalid
            messages.error(request, "Please fix the errors below.")
    else:
        form = TeacherReplyForm()

    context = {
        'teacher': teacher,
        'doubt': doubt,
        'replies': replies,
        'form': form,
        'is_hod': is_hod,
        'upvotes': upvotes,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'teacher/teacher_chat.html', context)

