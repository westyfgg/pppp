from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "telegram", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"autocomplete": "name", "placeholder": "Як до вас звертатися"}
            ),
            "email": forms.EmailInput(
                attrs={"autocomplete": "email", "placeholder": "name@example.com"}
            ),
            "telegram": forms.TextInput(
                attrs={"autocomplete": "off", "placeholder": "@username"}
            ),
            "message": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Коротко опишіть вашу ідею"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("email") and not cleaned_data.get("telegram"):
            raise forms.ValidationError(
                "Вкажіть email або Telegram, щоб я міг зв'язатися з вами."
            )
        return cleaned_data
