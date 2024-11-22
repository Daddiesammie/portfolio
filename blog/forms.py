from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none', 'placeholder': 'Enter your comment here...'}),
        }