import json
from datetime import datetime, time, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView

from app_celery.celery import ping
from blog.models import Post
from news.forms import CommentForm, NewsCreationForm
from news.models import News, NewsComment
from user.models import Channel


class RootView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.filter(
                is_breaking=True, date_created__gt=datetime.combine(datetime.today(), time.min) - timedelta(days=1))[:5]
        context['posts'] = Post.objects.all()[:5]
        return context

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)


class NewsListView(ListView):
    model = News
    paginate_by = 20
    template_name = "news/news_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = NewsComment.objects.filter(news=super().get_object())
        context['all_news'] = News.objects.all()[:20]
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                NewsComment.objects.create(comment_text=comment_form.cleaned_data['comment_text'],
                                           news=super().get_object(),
                                           author=request.user)
            return super().get(self, request, *args, **kwargs)

class NewsCreateView(TemplateView):
    template_name = "news/news_create.html"
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('login'))
        else:
            return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('login'))
        else:
            news_form = NewsCreationForm(request.POST)
            if news_form.is_valid():
                news = news_form.save()
                return redirect(reverse('root'))
