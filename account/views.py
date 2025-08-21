from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

from .models import User
from blog.models import *
from .token import account_activation_token

# Create your views here.

User = get_user_model()

class RegisterView(View):
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        bio = request.POST.get("bio", "").strip()
        profile_pic = request.FILES.get("profilePic")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        errors = {}

        if not username:
            errors["username"] = "Username is required."
        elif User.objects.filter(username=username).exists():
            errors["username"] = "Username already taken."

        if not email:
            errors["email"] = "Email is required."
        elif User.objects.filter(email=email).exists():
            errors["email"] = "Email already registered."

        if password1 != password2:
            errors["password"] = "Passwords do not match."
        elif len(password1) < 6:
            errors["password"] = "Password must be at least 6 characters."

        if errors:
            return render(request, self.template_name, {
                "errors": errors,
                "form_data": request.POST
            })
        
        user = User.objects.create_user(
            email=email,
            password=password1,
            username=username,
            bio=bio
        )

        if profile_pic:
            user.profile_picture = profile_pic

        user.is_active = False
        user.save()

        self.send_verification_email(user)

        messages.success(request, 'Registration successful! Please check your email to verify your account.')
        return redirect('login')

    def send_verification_email(self, user):
        current_site = get_current_site(self.request)
        subject = "InkWave: Verify your account"
        message = render_to_string('account/mail/verify_account_email.txt', {
            'user': user,
            'user_name': user.username,
            'site_name': 'InkWave',
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'expiry_hours': 24,
        })
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(get_user_model(), pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None 
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been verified. You can log in now.')
            return redirect('login')
        else:
            messages.error(request, 'Activation link is invalid!.')
            return redirect('login')

class LoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        errors = []

        if not email:
            errors.append("Email is required.")
        if not password:
            errors.append("Password is required.")

        if not errors:
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                if not self.request.POST.get('remember'):
                    self.request.session.set_expiry(0)
                else:
                    self.request.session.set_expiry(1209600)
                return redirect('home')
            else:
                errors.append("Invalid email or password.")

        return render(request, self.template_name, {
            'errors': errors,
            'email': email
        })
    
def LogOutView(request):
    logout(request)
    return redirect('home')

class ForgotPasswordView(View):
    template_name = 'account/forgot_password.html'
    success_url = reverse_lazy('login')

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, self.template_name, {'email': email})
        try:
            user = User.objects.get(email=email)
            self.send_verification_email(user)
            messages.success(request, 'Check your email inbox or spam folder for password reset instructions.')
            return redirect(self.success_url)
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email.')
            return render(request, self.template_name, {'email': email})

    def send_verification_email(self, user):
        current_site = get_current_site(self.request)
        subject = "InkWave: Reset your password"
        message = render_to_string('account/mail/forgot_password_email.txt', {
            'user': user,
            'user_name': user.username,
            'site_name': 'InkWave',
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'expiry_hours': 24,
            'support_email': 'inkwaveteam@yahoo.com'
        })
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

class ForgotPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'account/reset_password.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your password has been reset successfully. You can log in now.')
        return redirect(reverse_lazy('login'))

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'account/change_password.html'

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your new password has been set.')
            return redirect(reverse_lazy('profile', kwargs={'username': request.user.username}))
        else:
            return self.render_to_response(self.get_context_data(errors=form.errors))

class ProfileView(DetailView):
    model = User
    template_name = "account/profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile_user = self.get_object()

        articles_qs = Article.objects.filter(writer=profile_user).order_by('-date_added')

        paginator = Paginator(articles_qs, 6)
        page = self.request.GET.get('page')
        articles = paginator.get_page(page)

        context["articles"] = articles
        context["is_owner"] = self.request.user == profile_user
        return context
    
class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "account/edit_profile.html"

    def get(self, request):
        user = request.user
        context = {
            "username": user.username,
            "email": user.email,
            "bio": getattr(user, "bio", ""),
            "profile_picture": getattr(user, "profile_picture", None),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        bio = request.POST.get("bio", "").strip()
        profile_pic = request.FILES.get("profilePic")

        errors = []

        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email address is required.")
        elif "@" not in email:
            errors.append("Invalid email address.")

        if errors:
            return render(request, self.template_name, {
                "username": username,
                "email": email,
                "bio": bio,
                "errors": errors,
                "profile_picture": getattr(request.user, "profile_picture", None),
            })

        user = request.user
        user.username = username
        user.email = email
        if hasattr(user, "bio"):
            user.bio = bio
        if profile_pic:
            user.profile_picture = profile_pic
        user.save()

        messages.success(request, "Your profile has been updated successfully.")
        return redirect(reverse("profile", kwargs={"username": user.username}))
