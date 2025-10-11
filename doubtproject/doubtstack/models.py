from django.db import models
from django.contrib.auth.hashers import make_password
import random

class LoginDB(models.Model):
    adm_no = models.IntegerField(primary_key=True)
    stu_name = models.CharField(max_length=100)
    stu_email = models.EmailField(max_length=100)
    stu_branch = models.CharField(max_length=100)
    stu_sem = models.IntegerField(default=1)
    stu_start_year = models.CharField(max_length=100)
    stu_end_year = models.CharField(max_length=100)
    stu_dob = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.stu_name} ({self.adm_no})"


# Existing college database (teacher)
class LoginDB2(models.Model):
    tchr_no = models.IntegerField(primary_key=True)
    tchr_name = models.CharField(max_length=100)
    tchr_email = models.EmailField(max_length=100)
    tchr_dept = models.CharField(max_length=100)
    tchr_role = models.CharField(max_length=100)
    tchr_join_year = models.IntegerField()
    tchr_dob = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.tchr_name} ({self.tchr_no})"
    

# System student table
class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=30)
    semester = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# System teacher table
class Teacher(models.Model):
    teacher_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=30)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# OTP verification table
class OTPVerification(models.Model):
    reg_no = models.IntegerField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        return self.otp

    def __str__(self):
        return f"{self.reg_no} - {self.otp}"


import uuid
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, null=True)
    teacher_id = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='subjects')
    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name


class Doubt(models.Model):
    STATUS_CHOICES = [
        ('unresolved', 'Unresolved'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
    ]

    id = models.AutoField(primary_key=True)
    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='submitted_doubts')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    anonymous = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unresolved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Doubt {self.reference} by {self.student}"
    
    def total_votes(self):
        return self.votes.count()

    # ✅ Helper: check if a given student already voted
    def has_voted(self, student_id):
        return self.votes.filter(student__student_id=student_id).exists()


class Vote(models.Model):
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name='votes')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='doubt_votes')

    class Meta:
        unique_together = ('doubt', 'student')

    def __str__(self):
        return f"Vote by {self.student} on {self.doubt.reference}"
    
class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name='replies')
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)
    reply_text = models.CharField(max_length=1000, null=True, blank=True)
    file_url = models.FileField(upload_to='replies/', null=True, blank=True)
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reply_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
            ('file', 'File'),
            ('audio', 'Audio'),
            ('video', 'Video'),
            ('whiteboard', 'Whiteboard')
        ],
        default='text'
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        sender = self.teacher if self.teacher else self.student
        return f"Reply by {sender} on Doubt {self.doubt.id}"

