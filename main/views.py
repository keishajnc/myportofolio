from django.shortcuts import render

from main.models import Experience, Skill


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
