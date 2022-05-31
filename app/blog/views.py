from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import Post

class BlogIndexView(TemplateView):
    template_name = 'blog/blog_index.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'blog'
        context['posts'] = Post.postobjects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.filter(slug=self.kwargs.get('slug'))
        return context