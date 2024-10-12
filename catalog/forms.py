from typing import Any
from django.forms import BooleanField, ModelForm, ValidationError

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ("views_counter", "owner")



    def clean_name(self):
        name = self.cleaned_data["name"]
        self.validate_text(name, "name")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        self.validate_text(description, "description")
        return description

    def validate_text(self, text, field_name):
        forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
        for word in forbidden_words:
            if word in text.lower():
                raise ValidationError(f"Поле '{field_name}' содержит запрещенное слово '{word}'")


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.version_number = self.cleaned_data['version_number']
        instance.version_name = self.cleaned_data['version_name']
        if commit:
            instance.save()
        return instance
   