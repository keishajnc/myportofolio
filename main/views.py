import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from main.forms import ExperienceForm, SkillForm
from main.models import Experience, Skill


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="Editor").exists()


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login",
        "Belum ada sesi login / Cookie tidak ditemukan",
    )

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
    experiences = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []

    for experience in experiences:
        starred_users = experience.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            user.username for user in starred_users
        )

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "organization": experience.organization,
                "description": experience.description,
                "category": experience.category,
                "thumbnail": experience.thumbnail,
                "is_ongoing": experience.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)


def get_skills_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.prefetch_related("starred_by").all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    data = []

    for skill in skills:
        starred_users = skill.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            user.username for user in starred_users
        )

        data.append({
            "pk": str(skill.id),
            "fields": {
                "name": skill.name,
                "description": skill.description,
                "level": skill.level,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "title_query": title_query,
        "is_editor": is_editor(request.user),
        "form": ExperienceForm(),
    }

    return render(request, "experience.html", context)


def show_skill(request):
    name_query = request.GET.get("name", "").strip()

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "name_query": name_query,
        "is_editor": is_editor(request.user),
        "form": SkillForm(),
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


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang dapat "
                    "menambahkan experience."
                ),
            },
            status=403,
        )

    form = ExperienceForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                "message": "Periksa kembali data experience yang dimasukkan.",
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )

    experience = form.save()

    return JsonResponse(
        {
            "message": "Experience berhasil ditambahkan.",
            "pk": str(experience.id),
        },
        status=201,
    )


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


@require_POST
def create_skill_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang dapat "
                    "menambahkan skill."
                ),
            },
            status=403,
        )

    form = SkillForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                "message": "Periksa kembali data skill yang dimasukkan.",
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )

    skill = form.save()

    return JsonResponse(
        {
            "message": "Skill berhasil ditambahkan.",
            "pk": str(skill.id),
        },
        status=201,
    )


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
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=id)

    form = ExperienceForm(
        request.POST or None,
        instance=experience,
    )

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

@login_required(login_url="/login/")
def update_skill(request, id):
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied

    skill = get_object_or_404(Skill, pk=id)

    form = SkillForm(
        request.POST if request.method == "POST" else None,
        instance=skill,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skill")

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "form": form,
        "is_edit": True,
    }

    return render(request, "skill_form.html", context)

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
    form = AuthenticationForm(
        request,
        data=request.POST or None,
    )

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())

        response = redirect("main:show_main")
        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        return response

    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "form": form,
    }

    return render(request, "login.html", context)


def logout_user(request):
    logout(request)

    response = redirect("main:show_main")
    response.delete_cookie("last_login")

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