# Create your views here.
from django.views.generic import ListView, TemplateView
from .models import *


class PostListView(ListView):
    model = Post
    paginate_by = 3
    template_name = 'mainapp/post-list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=1).order_by('creation_date')


class TopPostListView(ListView):
    model = Post
    paginate_by = 3
    template_name = 'mainapp/post-top.html'

    def get_queryset(self):
        qs = super().get_queryset().filter(status=1)

        return sorted(qs, key=lambda post: post.rating,reverse=True)[:10]


class PostContentView(TemplateView):
    model = Post
    template_name = 'mainapp/post-content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        post_id = kwargs['post_id']
        try:
            context['post'] = Post.objects.get(id=post_id)
            context['comments'] = Comment.objects.filter(post=context['post'])
        except Post.DoesNotExist:
            context['post_does_not_exist'] = "Sorry, but this post does not exist, check URL."

        return context

    def post(self, request, *args, **kwargs):
        print("HURRICANE")
        # print("ahhaa")
        # print(kwargs)
        # print("req")
        # print(request.POST.get('comment-text'))
        # post_id = kwargs['post_id']
        try:
            Comment.objects.create(user=request.user, text=request.POST.get('comment-text'),
                                   post=Post.objects.get(id=kwargs['post_id']))
        except Exception as e:
            print(e)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)



