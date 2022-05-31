from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogIndexView.as_view(), name='blog_index'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
]
