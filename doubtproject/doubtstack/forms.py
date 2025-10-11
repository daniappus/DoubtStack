from django import forms

# Step 1: Enter register/staff number
class RegisterNumberForm(forms.Form):
    reg_no = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-gray-200',
            'placeholder': 'Enter your register/staff number'
        })
    )

# Step 2: OTP verification
class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 text-center text-xl bg-gray-900 border border-gray-700 rounded-lg text-gray-200',
            'placeholder': 'Enter OTP'
        })
    )

# Step 3: Set password
class PasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-gray-200',
            'placeholder': 'Enter password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-gray-200',
            'placeholder': 'Confirm password'
        })
    )


from django import forms
from .models import Doubt, Subject

class SubmitDoubtForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['subject', 'topic', 'text', 'anonymous']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Type your doubt...', 'rows': 4, 'class': 'w-full p-2 rounded-md bg-gray-800 text-gray-200'}),
            'topic': forms.TextInput(attrs={'placeholder': 'Topic (optional)', 'class': 'w-full p-2 rounded-md bg-gray-800 text-gray-200'}),
            'subject': forms.Select(attrs={'class': 'w-full p-2 rounded-md bg-gray-800 text-gray-200'}),
            'anonymous': forms.CheckboxInput(attrs={'class': 'h-4 w-4 accent-purple-500'}),
        }

from django import forms
from .models import Reply

class StudentReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_text', 'file_url', 'anonymous']
        widgets = {
            'reply_text': forms.Textarea(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Type your reply here...',
            }),
            'file_url': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-700 border border-gray-300 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'anonymous': forms.CheckboxInput(attrs={
                'class': 'mr-2 rounded text-blue-600 focus:ring-blue-500',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        reply_text = cleaned_data.get('reply_text')
        file_url = cleaned_data.get('file_url')

        if not reply_text and not file_url:
            raise forms.ValidationError("⚠️ Please provide either a message or attach a file.")

        return cleaned_data
    

# forms.py
from django import forms
from .models import Reply

class TeacherReplyForm(forms.ModelForm):
    mark_resolved = forms.BooleanField(
        required=False,
        label="Mark this doubt as resolved",
        widget=forms.CheckboxInput(attrs={
            'class': 'mr-2 rounded text-green-600 focus:ring-green-500',
        })
    )

    class Meta:
        model = Reply
        fields = ['reply_text', 'file_url']
        widgets = {
            'reply_text': forms.Textarea(attrs={
                'class': 'w-full p-3 rounded-lg border border-gray-700 bg-gray-800 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Type your reply here...',
            }),
            'file_url': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-300 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        reply_text = cleaned_data.get('reply_text')
        file_url = cleaned_data.get('file_url')

        if not reply_text and not file_url:
            raise forms.ValidationError("⚠️ Please provide either a message or attach a file.")
        return cleaned_data



