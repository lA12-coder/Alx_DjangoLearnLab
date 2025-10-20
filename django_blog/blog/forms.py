from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post, Comment, Tag

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PostForm(forms.ModelForm):
    tags_field = forms.CharField(required=False, help_text='Comma-separated tags')

    class Meta:
        model = Post
        fields = ['title', 'content']

    def save(self, commit=True, author=None):
        post = super().save(commit=False)
        if author:
            post.author = author
        if commit:
            post.save()
            tags_text = self.cleaned_data.get('tags_field', '')
            tag_names = [t.strip() for t in tags_text.split(',') if t.strip()]
            # attach tags: create or get
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                post.tags.add(tag)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }
