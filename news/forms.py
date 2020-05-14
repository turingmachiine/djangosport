from django import forms
from news.models import NewsComment, News


class CommentForm(forms.ModelForm):

    class Meta:
        model = NewsComment
        fields = {"comment_text"}


class NewsCreationForm(forms.ModelForm):
    class Meta:
        model = News
        fields = {'headline', 'news_text', 'source', 'is_breaking'}
