from django import forms
from django.contrib.auth import authenticate

from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your login...', }
        ),
        max_length=20,
        label='Login',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your password...', }
        ),
        min_length=8,
        label='Password',
    )

    def clean(self):
        user = authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password']
                            )

        if user is not None:

            if user.is_active:
                self.cleaned_data['user'] = user
            else:
                raise forms.ValidationError('This user is\'t active!!!')
        else:
            raise forms.ValidationError('Invalid login or password!!!')


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter login...'}
        ),
        max_length=20,
        label='Login',
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your first name...'}
        ),
        max_length=20,
        label='First name',
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your last name login...'}
        ),
        max_length=20,
        label='Last name',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter e-mail...'}
        ),
        max_length=30,
        label='E-mail',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter password...'}
        ),
        min_length=8,
        label='Password',
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Renter password...'}
        ),
        min_length=8,
        label='Repeat password',
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={'class': 'form-control input-lg', }
        ),
        label='Avatar'
    )

    def clean_username(self):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError('User already exists!!!')
        except User.DoesNotExist:
            return self.cleaned_data['username']

    def clean_repeat_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
            raise forms.ValidationError('Passwords don\'t match!!!')

    def clean_email(self):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError('E-mail already in use!!!')
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'],
                                        )

        return authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password'],
                            )


class SettingsForm(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control input-lg', }
        ),
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your first name...'}
        ),
        max_length=20,
        label='First name',
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your last name login...'}
        ),
        max_length=20,
        label='Last name',
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control input-lg', }
        ),
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={'class': 'form-control input-lg', }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        forms.Form.__init__(self, initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }, *args, **kwargs
                            )

    def clean_username(self):
        if self.cleaned_data['username'] == self.user.username:
            return self.cleaned_data['username']

        try:
            user = User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError('Username already in use!!!')
        except User.DoesNotExist:
            return self.cleaned_data['username']

    def clean_first_name(self):
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        return self.cleaned_data['last_name']

    def clean_email(self):
        if self.cleaned_data['email'] == self.user.email:
            return self.cleaned_data['email']

        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError('E-mail already in use!!!')
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def save(self):
        self.user.username = self.cleaned_data['username']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        self.user.avatar = self.cleaned_data['avatar']

        self.user.save()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags', ]

    def __init__(self, current_user, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['text'].widget.attrs.update({
            'class': 'form-control askme-textarea',
            'rows': 5,
        })
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control'
        })
        self.current_user = current_user

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        question.user = self.current_user

        if commit:
            question.save()

        return question.id


class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Enter question title...'
    }))
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Enter question context...',
        'rows': 20,
    }))

    def save(self, user_id):
        data = self.cleaned_data
        question = Question(title=data['title'], text=data['text'], author_id=user_id)
        question.save()
