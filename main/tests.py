from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Skill


class PortfolioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser")

        cls.editor = User.objects.create_user(username="testeditor")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        cls.editor.groups.add(editor_group)

        cls.owner = User.objects.create_user(
            username="testowner",
            is_staff=True,
            is_superuser=True,
        )

        cls.experience = Experience.objects.create(
            title="Unique AJAX Experience",
            organization="Test Organization",
            description="Unique experience description",
            category="volunteer",
        )

        cls.skill = Skill.objects.create(
            name="Unique AJAX Skill",
            description="Unique skill description",
            level="Intermediate",
        )

    def setUp(self):
        self.create_cases = [
            (
                Experience,
                "main:create_experience_ajax",
                {
                    "title": "New Experience",
                    "organization": "New Organization",
                    "description": "New experience description",
                    "category": "volunteer",
                    "thumbnail": "",
                },
            ),
            (
                Skill,
                "main:create_skill_ajax",
                {
                    "name": "New Skill",
                    "description": "New skill description",
                    "level": "Advanced",
                },
            ),
        ]

    def test_home_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.experience.title)

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_models_and_experience_status(self):
        self.assertEqual(str(self.experience), self.experience.title)
        self.assertEqual(str(self.skill), self.skill.name)
        self.assertTrue(self.experience.is_ongoing)

        self.experience.ended_at = timezone.now()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

    def test_list_pages_render_shell_for_all_roles(self):
        pages = [
            (
                "main:show_experience",
                "experience.html",
                self.experience.title,
            ),
            (
                "main:show_skill",
                "skill.html",
                self.skill.name,
            ),
        ]

        for account in [None, self.user, self.editor, self.owner]:
            self.client.logout()

            if account is not None:
                self.client.force_login(account)

            for route, template, stored_title in pages:
                with self.subTest(account=account, route=route):
                    response = self.client.get(reverse(route))

                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, template)
                    self.assertContains(response, 'id="grid"')
                    self.assertNotContains(response, stored_title)

    def test_json_endpoints_are_public(self):
        cases = [
            ("main:get_experiences_json", self.experience),
            ("main:get_skills_json", self.skill),
        ]

        for route, item in cases:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))

                self.assertEqual(response.status_code, 200)

                data = response.json()
                self.assertEqual(len(data), 1)
                self.assertEqual(data[0]["pk"], str(item.pk))
                self.assertEqual(data[0]["fields"]["star_count"], 0)
                self.assertFalse(data[0]["fields"]["is_starred"])

    def test_empty_json_lists(self):
        Experience.objects.all().delete()
        Skill.objects.all().delete()

        for route in [
            "main:get_experiences_json",
            "main:get_skills_json",
        ]:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), [])

    def test_ajax_search_filters_both_models(self):
        Experience.objects.create(
            title="Other Experience",
            organization="Other Organization",
            description="Other description",
        )
        Skill.objects.create(
            name="Other Skill",
            description="Other description",
            level="Beginner",
        )

        cases = [
            (
                "main:get_experiences_json",
                "title",
                self.experience,
            ),
            (
                "main:get_skills_json",
                "name",
                self.skill,
            ),
        ]

        for route, field, item in cases:
            with self.subTest(route=route):
                response = self.client.get(
                    reverse(route),
                    {field: "uNIQue"},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    [entry["pk"] for entry in response.json()],
                    [str(item.pk)],
                )

                response = self.client.get(
                    reverse(route),
                    {field: "zzzzzz"},
                )
                self.assertEqual(response.json(), [])

    def test_json_star_status_depends_on_current_user(self):
        cases = [
            ("main:get_experiences_json", self.experience),
            ("main:get_skills_json", self.skill),
        ]

        for route, item in cases:
            with self.subTest(route=route):
                item.starred_by.add(self.user)

                self.client.logout()
                response = self.client.get(reverse(route))
                fields = response.json()[0]["fields"]

                self.assertEqual(fields["star_count"], 1)
                self.assertFalse(fields["is_starred"])

                self.client.force_login(self.user)
                response = self.client.get(reverse(route))
                fields = response.json()[0]["fields"]

                self.assertEqual(fields["star_count"], 1)
                self.assertTrue(fields["is_starred"])

    def test_superuser_can_create_with_ajax(self):
        self.client.force_login(self.owner)

        for model, route, payload in self.create_cases:
            with self.subTest(route=route):
                count_before = model.objects.count()
                response = self.client.post(reverse(route), payload)

                self.assertEqual(response.status_code, 201)
                self.assertEqual(
                    model.objects.count(),
                    count_before + 1,
                )
                self.assertTrue(
                    model.objects.filter(
                        pk=response.json()["pk"]
                    ).exists()
                )

    def test_empty_ajax_submission_returns_validation_errors(self):
        self.client.force_login(self.owner)

        for model, route, payload in self.create_cases:
            with self.subTest(route=route):
                count_before = model.objects.count()
                response = self.client.post(reverse(route), {})

                self.assertEqual(response.status_code, 400)
                self.assertTrue(response.json()["errors"])
                self.assertEqual(model.objects.count(), count_before)

    def test_unauthorized_roles_cannot_create_with_ajax(self):
        for account in [None, self.user, self.editor]:
            self.client.logout()

            if account is not None:
                self.client.force_login(account)

            for model, route, payload in self.create_cases:
                with self.subTest(account=account, route=route):
                    count_before = model.objects.count()
                    response = self.client.post(reverse(route), payload)

                    self.assertEqual(response.status_code, 403)
                    self.assertIn("message", response.json())
                    self.assertEqual(
                        model.objects.count(),
                        count_before,
                    )

    def test_ajax_create_rejects_get_requests(self):
        for model, route, payload in self.create_cases:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertEqual(response.status_code, 405)

    def test_required_fields_reject_html_only_input(self):
        self.client.force_login(self.owner)

        for model, route, payload in self.create_cases:
            text_fields = (
                ["title", "organization", "description"]
                if model is Experience
                else ["name", "description", "level"]
            )

            for field in text_fields:
                with self.subTest(route=route, field=field):
                    data = payload.copy()
                    data[field] = '<img src="x" onerror="alert(\'XSS!\')">'
                    count_before = model.objects.count()

                    response = self.client.post(reverse(route), data)

                    self.assertEqual(response.status_code, 400)
                    self.assertIn(field, response.json()["errors"])
                    self.assertEqual(
                        model.objects.count(),
                        count_before,
                    )

    def test_html_tags_are_removed_before_saving(self):
        self.client.force_login(self.owner)

        for model, route, payload in self.create_cases:
            with self.subTest(route=route):
                text_fields = (
                    ["title", "organization", "description"]
                    if model is Experience
                    else ["name", "description", "level"]
                )

                data = payload.copy()

                for field in text_fields:
                    data[field] = f"<b>{payload[field]}</b>"

                response = self.client.post(reverse(route), data)

                self.assertEqual(response.status_code, 201)

                saved_item = model.objects.get(
                    pk=response.json()["pk"]
                )

                for field in text_fields:
                    self.assertEqual(
                        getattr(saved_item, field),
                        payload[field],
                    )

    def test_ajax_create_requires_csrf_token(self):
        cases = [
            (self.create_cases[0], "main:show_experience"),
            (self.create_cases[1], "main:show_skill"),
        ]

        for case, page_route in cases:
            model, route, payload = case

            with self.subTest(route=route):
                csrf_client = Client(enforce_csrf_checks=True)
                csrf_client.force_login(self.owner)

                page = csrf_client.get(reverse(page_route))
                self.assertEqual(page.status_code, 200)

                token = csrf_client.cookies["csrftoken"].value
                count_before = model.objects.count()

                response = csrf_client.post(reverse(route), payload)

                self.assertEqual(response.status_code, 403)
                self.assertEqual(model.objects.count(), count_before)

                response = csrf_client.post(
                    reverse(route),
                    payload,
                    HTTP_X_CSRFTOKEN=token,
                )

                self.assertEqual(response.status_code, 201)
                self.assertEqual(
                    model.objects.count(),
                    count_before + 1,
                )

    def test_regular_user_cannot_edit_skill(self):
        self.client.force_login(self.user)

        url = reverse(
            "main:update_skill",
            args=[self.skill.pk],
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.client.post(
            url,
            {
                "name": "Unauthorized Change",
                "description": "Unauthorized description",
                "level": "Advanced",
            },
        )
        self.assertEqual(response.status_code, 403)

        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Unique AJAX Skill")

    def test_editor_and_superuser_can_edit_skill(self):
        url = reverse(
            "main:update_skill",
            args=[self.skill.pk],
        )

        for account in [self.editor, self.owner]:
            with self.subTest(account=account):
                self.client.force_login(account)

                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "skill_form.html")

                count_before = Skill.objects.count()

                response = self.client.post(
                    url,
                    {
                        "name": self.skill.name,
                        "description": self.skill.description,
                        "level": "Advanced",
                    },
                )

                self.assertRedirects(
                    response,
                    reverse("main:show_skill"),
                )

                self.skill.refresh_from_db()
                self.assertEqual(self.skill.level, "Advanced")
                self.assertEqual(Skill.objects.count(), count_before)

    def test_star_requires_login_and_can_be_toggled(self):
        cases = [
            ("main:toggle_star_experience", self.experience),
            ("main:toggle_star_skill", self.skill),
        ]

        for route, item in cases:
            with self.subTest(route=route):
                url = reverse(route, args=[item.pk])

                self.client.logout()
                response = self.client.post(url)

                self.assertEqual(response.status_code, 302)
                self.assertTrue(
                    response.url.startswith(reverse("main:login"))
                )
                self.assertEqual(item.starred_by.count(), 0)

                self.client.force_login(self.user)
                response = self.client.post(url)

                self.assertEqual(response.status_code, 302)
                self.assertEqual(item.starred_by.count(), 1)

                response = self.client.post(url)

                self.assertEqual(response.status_code, 302)
                self.assertEqual(item.starred_by.count(), 0)