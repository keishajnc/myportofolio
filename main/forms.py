from django.forms import ModelForm, TextInput, Textarea, URLInput, Select
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Title tidak boleh hanya berisi tag HTML.")
        return title

    def clean_organization(self):
        organization = strip_tags(self.cleaned_data["organization"]).strip()
        if not organization:
            raise ValidationError(
                "Organization tidak boleh kosong atau hanya berisi tag HTML."
            )
        return organization

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError(
                "Description tidak boleh kosong atau hanya berisi tag HTML."
            )
        return description


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

    def clean_name(self):
        name = strip_tags(self.cleaned_data["name"]).strip()
        if not name:
            raise ValidationError("Nama skill tidak boleh hanya berisi tag HTML.")
        return name

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError(
                "Description tidak boleh kosong atau hanya berisi tag HTML."
            )
        return description

    def clean_level(self):
        level = strip_tags(self.cleaned_data["level"]).strip()
        if not level:
            raise ValidationError(
                "Level tidak boleh kosong atau hanya berisi tag HTML."
            )
        return level