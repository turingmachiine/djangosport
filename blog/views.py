from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from blog.forms import CommentForm, PostForm, SearchForm
from blog.models import Post, PostComment
from news.models import News
from user.models import User, Channel


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            post_list = Post.objects.filter(Q(name__icontains=query) |
                                           Q(post_text__icontains=query) |
                                           Q(author__name__icontains=query) |
                                           Q(author__description__icontains=query))
            news_list = News.objects.filter(Q(headline__icontains=query) |
                                            Q(news_text__icontains=query))
            print('abc')
            return render(request, "search_list.html", {'post_list': post_list,
                                                        'news_list': news_list })


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = PostComment.objects.filter(post=super().get_object())
        context['news'] = News.objects.all()[:20]
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                PostComment.objects.create(comment_text=comment_form.cleaned_data['comment_text'],
                                           post=super().get_object(),
                                           author=request.user)
            return super().get(self, request, *args, **kwargs)


class PostCreateView(TemplateView):
    template_name = "blog/post_create.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or len(Channel.objects.filter(owner=self.request.user)) == 0:
            return HttpResponseRedirect(reverse('login'))
        else:
            return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        else:
            post_form = PostForm(self.request.user, request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save()
                post.cover = post_form.cleaned_data['cover']
                post.save()
                return super().get(self, request, *args, **kwargs)
