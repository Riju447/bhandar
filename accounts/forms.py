from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm


class SignUpForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        max_length=150,
        required=True,
    )

    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Password confirmation',
        strip=False,
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is not None:
            return username.strip()
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'A user with that email already exists.'
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")

        return password2

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')

        if password:
            try:
                validate_password(
                    password,
                    user=User(
                        username=cleaned_data.get('username') or ''
                    )
                )
            except forms.ValidationError as error:
                self.add_error('password1', error)

        return cleaned_data

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )

        user.set_password(self.cleaned_data['password1'])

        if commit:
            # OTP version
            # user.is_active = False

            # Without OTP
            user.is_active = True
            user.save()

        return user


class CustomAuthenticationForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )

            if self.user_cache is None:

                # OTP check (disabled)
                #
                # try:
                #     user = User.objects.get(username=username)
                # except User.DoesNotExist:
                #     user = None
                #
                # if user is not None and not user.is_active:
                #     raise forms.ValidationError(
                #         'Your account is not active yet. '
                #         'Please verify your OTP first.'
                #     )

                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={
                        'username': self.username_field.verbose_name,
                    },
                )

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomPasswordChangeForm(PasswordChangeForm):
    pass


class CustomPasswordResetForm(PasswordResetForm):
    pass


class CustomSetPasswordForm(SetPasswordForm):
    pass


class ProfileForm(ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Required. 150 characters or fewer.',
        validators=[],
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is not None:
            return username.strip()
        return username


class UserManagementForm(ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Required. 150 characters or fewer.',
        validators=[],
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is not None:
            return username.strip()
        return username


# =====================================================
# OTP Form (Disabled)
# =====================================================

# class VerifyOTPForm(forms.Form):
#     otp = forms.CharField(
#         max_length=6,
#         min_length=6,
#         label='Verification code'
#     )