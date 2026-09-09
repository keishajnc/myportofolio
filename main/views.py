from django.shortcuts import render

from main.models import Experience


# Create your views here.
def show_main(request):
    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "npm": "2506551232",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Keisha Janice Maulina Napitupulu",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
