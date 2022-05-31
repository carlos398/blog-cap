from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post

class BlogIndexView(TemplateView):
    template_name = 'blog/blog_index.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'blog'
        context['posts'] = Post.postobjects.all()
        return context