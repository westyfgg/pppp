from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactMessageForm
from .models import Project


def home(request):
    projects = Project.objects.filter(is_published=True)
    return render(request, "index.html", {"projects": projects})


def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Дякую! Повідомлення успішно надіслано.")
            return redirect("portfolio:contact_sent")
    else:
        form = ContactMessageForm()
    return render(request, "contact.html", {"form": form})


def contact_sent(request):
    return render(request, "contact_sent.html")
