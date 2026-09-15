from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.models import Experience, Skill
from main.forms import ExperienceForm, SkillForm


# Create your views here.
def show_main(request):
    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "npm": "2506551232",
        "study_program": "S1 Sistem Informasi",
        "bio": (
             "An Information Systems student at Universitas Indonesia "
    "interested in software development and education."
        ),
        "experience_list": Experience.objects.all(),
        "skill_list": Skill.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skill(request):
    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skill.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "form": form,
    }
    return render(request, "experience_form.html", context)


def create_skill(request):
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil ditambahkan!")
        return redirect("main:show_skill")

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "form": form,
    }
    return render(request, "skill_form.html", context)
