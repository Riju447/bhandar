from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

# OTP imports (disabled)
# from django.conf import settings
# from django.core.mail import send_mail
# from .models import EmailOTP

from .forms import (
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    ProfileForm,
    SignUpForm,
    UserManagementForm,
    # VerifyOTPForm,
)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        # OTP code (disabled)
        #
        # user = form.save(commit=False)
        # user.is_active = False
        # user.save()
        #
        # otp_obj, _ = EmailOTP.objects.get_or_create(user=user)
        # otp_code = otp_obj.generate_code()
        # self.request.session['pending_verification_user_id'] = user.pk
        #
        # send_mail(
        #     'Verify your account',
        #     f'Your verification code is: {otp_code}',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [user.email],
        #     fail_silently=False,
        # )
        #
        # messages.success(
        #     self.request,
        #     'Account created. Please verify your email using the OTP sent to you.'
        # )
        # return redirect('accounts:verify_otp')

        # New signup flow (OTP removed)
        user = form.save()

        messages.success(
            self.request,
            'Account created successfully. Please log in.'
        )

        return redirect('accounts:login')


# OTP verification view (disabled)
#
# class VerifyOTPView(View):
#     template_name = 'accounts/verify_otp.html'
#
#     def get(self, request):
#         form = VerifyOTPForm()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = VerifyOTPForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['otp']
#             user_id = request.session.get('pending_verification_user_id')
#
#             if not user_id:
#                 messages.error(request, 'No verification request found.')
#                 return redirect('accounts:signup')
#
#             try:
#                 user = User.objects.get(pk=user_id)
#                 otp_obj = EmailOTP.objects.get(user=user)
#             except (User.DoesNotExist, EmailOTP.DoesNotExist):
#                 messages.error(request, 'No verification request found.')
#                 request.session.pop('pending_verification_user_id', None)
#                 return redirect('accounts:signup')
#
#             if otp_obj.code != code:
#                 messages.error(request, 'Invalid verification code.')
#                 return render(request, self.template_name, {'form': form})
#
#             user.is_active = True
#             user.save(update_fields=['is_active'])
#             otp_obj.delete()
#             request.session.pop('pending_verification_user_id', None)
#             user.backend = 'django.contrib.auth.backends.ModelBackend'
#             login(request, user)
#
#             messages.success(request, 'Account verified successfully.')
#             return redirect('dashboard:home')
#
#         return render(request, self.template_name, {'form': form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        return render(request, 'accounts/profile.html', {'form': form})


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('accounts:profile')


class PasswordResetRequestView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserManagementForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.is_superuser


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserManagementForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.is_superuser


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.is_superuser


@login_required
def toggle_user_status(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to do this.')
        return redirect('dashboard:home')

    user = User.objects.get(pk=pk)
    user.is_active = not user.is_active
    user.save()

    messages.success(request, 'User status updated successfully.')
    return redirect('accounts:user_list')