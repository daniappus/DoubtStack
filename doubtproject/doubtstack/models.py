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
