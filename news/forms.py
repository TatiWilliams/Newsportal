from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from .models import Post


class NewsForm(forms.ModelForm):
    check_box = forms.BooleanField(label='Ало, Галочка!')

    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
            'author',
        ]


class BasicSignupForm(UserCreationForm):

    def save(self, commit=True):
        user = super(BasicSignupForm, self).save(commit=commit)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
