# app/views.py
from .models import Project, ContactMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

def home(request):
    projects = Project.objects.all()
    return render(request, 'app/index.html', {'projects': projects})




def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Basic validation
        if not all([name, email, subject, message]):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        if '@' not in email:
            return JsonResponse({'error': 'Please enter a valid email address'}, status=400)

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact_submit')

    return redirect('home')