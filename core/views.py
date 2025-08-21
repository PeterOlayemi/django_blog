from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

from .models import *

# Create your views here.

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ContactView(View):
    template_name = 'core/contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name', '').strip()
        email_address = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email_address and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email_address,
                subject=subject,
                message=message
            )
            self.send_message_confirmation_email(name, email_address)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill out all fields correctly.')
            return render(request, self.template_name)

    def send_message_confirmation_email(self, name, email_address):
        subject = "InkWave: We've received your message"
        text_message = render_to_string('core/mail/message_confirmation_email.txt', {
            'name': name,
            'date': timezone.now().date(),
        })
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email_address]
        )
        email.send()
 
class PrivacyView(TemplateView):
    template_name = 'core/privacy_policy.html'

class TermView(TemplateView):
    template_name = 'core/terms.html'
