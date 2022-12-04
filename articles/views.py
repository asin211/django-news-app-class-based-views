from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Article
from .forms import CommentForm

# Create your views here.
class HomePageView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "home.html"
    

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"
    


class CommentGet(DetailView):  # new
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

class CommentPost(SingleObjectMixin, PermissionRequiredMixin, FormView):  # new
    permission_required = "articles.add_comment"
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        form.instance.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):  # new
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, UpdateView):  # new
    # blog -- it is an app
    # photo -- it is model under blog
    # blog.add_photo - <app>.add_<model> (you can replace add with change, delete, view)
    permission_required = "articles.change_article"
    model = Article
    fields = (
        "title",
        "body",
    )
    template_name = "article_edit.html"

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, DeleteView):  # new
    permission_required = "articles.delete_article"
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user
    

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # new
    permission_required = "articles.add_article"
    model = Article
    template_name = "article_new.html"
    fields = ("title", "body")  # new

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)