from django import forms
from bbsnote.models import Board, Comment

# .form.
class BoardForm(forms.ModelForm):
    class Meta:
        # model(DB)은 Board를 참조
        model = Board
        #Board에서 입력받고자 하는 값
        fields = ['subject','content']
        # widgets = {
        #     'subject':forms.TextInput(attrs={'class':'form-control'}),
        #     'content':forms.Textarea(attrs={'class':'form-control','rows':10})
        # }
        # labels = {
        #     'subject':'제목',
        #     'content':'내용'
        # }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content':'댓글 내용'
        }