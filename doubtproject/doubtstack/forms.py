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
