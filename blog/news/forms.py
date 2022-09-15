from django import forms
from .models import Author, Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)  # Задаем минимальную длину текста публикации при создании новой публикации через форму

    class Meta:
        model = Post
        fields = ['authorConnect', 'title', 'text', 'postCategory',]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Текст публикации не должен быть идентичен названию."
            )

        return cleaned_data


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['authorUser']
#            'authorUser__username',
#            'authorUser__first_name',
#            'authorUser__last_name',
#            'authorUser__email'
#            ]
