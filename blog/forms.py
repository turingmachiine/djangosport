from django import forms
from blog.models import PostComment, Post
from user.models import Channel


class CommentForm(forms.ModelForm):

    class Meta:
        model = PostComment

        fields = {"comment_text"}


class PostForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['author'] = forms.ModelChoiceField(queryset=Channel.objects.filter(owner=user))

    class Meta:
        model = Post

        fields = {"name", "description", "post_text", "cover", "author"}


class SearchForm(forms.Form):
    query = forms.CharField()
