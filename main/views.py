from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from main.models import Experience, Skill
from main.forms import ExperienceForm, SkillForm
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "last_login": last_login,
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


def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(experiences_json, content_type="application/json")


def get_skills_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    skills_json = serializers.serialize("json", skills, use_natural_foreign_keys=True)
    return HttpResponse(skills_json, content_type="application/json")


def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def show_skill(request):
    json_response = get_skills_json(request)

    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [skill.object for skill in skills]
    name_query = request.GET.get("name", "").strip()

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "skill_list": skills,
        "name_query": name_query,
    }
    return render(request, "skill.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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


@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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


@login_required(login_url="/login/")
def delete_experience(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def delete_skill(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    skill = get_object_or_404(Skill, pk=id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")

@login_required(login_url="/login/")
def update_experience(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "form": form,
        "is_edit": True,
    }

    return render(request, "experience_form.html", context)


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)
    return redirect("main:show_experience")

@login_required(login_url="/login/")
def toggle_star_skill(request, id):
    skill = get_object_or_404(Skill, pk=id)
    if request.method == "POST":
        if request.user in skill.starred_by.all():
            skill.starred_by.remove(request.user)
        else:
            skill.starred_by.add(request.user)
    return redirect("main:show_skill")
