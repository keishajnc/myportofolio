from django.forms import ModelForm, TextInput, Textarea, URLInput, Select
from main.models import Experience, Skill

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "organization", "description", "category", "thumbnail"]

        labels = {
            "title": "Title",
            "organization": "Organization",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail URL",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Software Engineering Intern",
                    "maxlength": 255,
                }
            ),
            "organization": TextInput(
                attrs={
                    "placeholder": "Google",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Developed new features for...",
                    "rows": 3,
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...",
                }
            ),
        }


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "description", "level"]

        labels = {
            "name": "Skill Name",
            "description": "Description",
            "level": "Proficiency Level",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Python",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Experienced in building web applications...",
                    "rows": 3,
                }
            ),
            "level": TextInput(
                attrs={
                    "placeholder": "Advanced",
                    "maxlength": 50,
                }
            ),
        }
