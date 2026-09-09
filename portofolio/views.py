from django.shortcuts import render
from main.models import Skill

def landing_page(request):
    return render(request, "index.html")

def skill_page(request):
    skills = Skill.objects.all()

    return render(request, "skill.html", {
        "skills": skills
    })