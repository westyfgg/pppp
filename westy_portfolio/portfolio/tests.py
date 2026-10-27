from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import ContactMessage, Project


class PortfolioPageTests(TestCase):
    def test_homepage_lists_published_projects_and_escapes_user_content(self):
        project = Project.objects.create(
            title="<script>alert(1)</script>",
            description="Опис проєкту",
            is_published=True,
        )
        Project.objects.create(title="Чернетка", description="Не показувати", is_published=False)

        response = self.client.get(reverse("portfolio:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ідеї набувають сили")
        self.assertContains(response, "Андрій Бідник (Westy)")
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, project.description)
        self.assertNotContains(response, "Не показувати")
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertIn("Content-Security-Policy", response)
        self.assertIn("script-src 'self'", response["Content-Security-Policy"])
        self.assertNotIn("'unsafe-inline'", response["Content-Security-Policy"])

    def test_admin_has_its_own_csp_and_is_usable(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="secure-test-password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("admin:portfolio_project_changelist"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("'unsafe-inline'", response["Content-Security-Policy"])


class ContactFormTests(TestCase):
    def test_contact_form_requires_a_csrf_token(self):
        client = Client(enforce_csrf_checks=True)

        response = client.post(
            reverse("portfolio:contact"),
            {"name": "Андрій", "email": "test@example.com", "message": "Привіт"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_form_requires_email_or_telegram(self):
        response = self.client.post(
            reverse("portfolio:contact"),
            {"name": "Андрій", "email": "", "telegram": "", "message": "Привіт"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Вкажіть email або Telegram")
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_valid_contact_message_is_saved(self):
        client = Client(enforce_csrf_checks=True)
        client.get(reverse("portfolio:contact"))
        csrf_token = client.cookies["csrftoken"].value

        response = client.post(
            reverse("portfolio:contact"),
            {
                "name": "Андрій",
                "email": "test@example.com",
                "telegram": "",
                "message": "Потрібен сайт",
            },
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertRedirects(response, reverse("portfolio:contact_sent"))
        message = ContactMessage.objects.get()
        self.assertEqual(message.name, "Андрій")
        self.assertEqual(message.email, "test@example.com")
