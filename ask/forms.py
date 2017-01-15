from datetime import datetime
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


class QuestionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control input-lg', }
        ),
        min_length=3,
        max_length=100,
        label='Title',
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control input-lg', }
        ),
        label='Text',
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_title(self):
        try:
            question = Question.objects.get(title=self.cleaned_data['title'])
            raise forms.ValidationError('Title is already in use!!!')
        except Question.DoesNotExist:
            return self.cleaned_data['title']

    def save(self):
        question = Question()

        question.title = self.cleaned_data['title']
        question.text = self.cleaned_data['text']
        question.author = self.user
        question.date = datetime.now()
        question.likes = 0

        question.save()

        return question


class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control input-lg', }
        ),
        label='Text',
    )
    question_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_text(self):
        if not self.cleaned_data['text'] or not len(self.cleaned_data['text']):
            raise forms.ValidationError('This field is required!!!')

        return self.cleaned_data['text']

    def clean_question(self):
        if Question.objects.get(id=self.cleaned_data['question_id']):
            return self.cleaned_data['question_id']

        raise forms.ValidationError('Question does\'t exist!!!')

    def save(self):
        answer = Answer()

        answer.text = self.cleaned_data['text']
        answer.question_id = self.cleaned_data['question_id']
        answer.author = self.user
        answer.date = datetime.now()
        answer.likes = 0

        answer.save()