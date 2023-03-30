from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bbsnote.models import Board, Comment

class UserForm(UserCreationForm):
    # email 적는 field 추가
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username","email")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content':'댓글 내용'
        }