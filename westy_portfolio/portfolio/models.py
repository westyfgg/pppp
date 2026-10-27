from django.db import models


class Project(models.Model):
    title = models.CharField("назва", max_length=120)
    description = models.TextField("опис")
    image = models.ImageField("зображення", upload_to="projects/", blank=True)
    url = models.URLField("посилання", blank=True)
    tech_stack = models.CharField("технології", max_length=240, blank=True)
    order = models.PositiveIntegerField("порядок", default=0)
    is_published = models.BooleanField("опубліковано", default=True)
    created_at = models.DateTimeField("додано", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "проєкт"
        verbose_name_plural = "проєкти"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField("ім'я", max_length=100)
    email = models.EmailField("email", blank=True)
    telegram = models.CharField("Telegram", max_length=100, blank=True)
    message = models.TextField("повідомлення", max_length=4000)
    created_at = models.DateTimeField("дата створення", auto_now_add=True)
    is_read = models.BooleanField("прочитано", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "повідомлення"
        verbose_name_plural = "повідомлення"

    def __str__(self):
        return f"{self.name} — {self.created_at:%d.%m.%Y %H:%M}"
