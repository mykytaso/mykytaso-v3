from django.views import generic

from posts.models import Post


class PostListView(generic.ListView):
    model = Post
    template_name = "index.html"
