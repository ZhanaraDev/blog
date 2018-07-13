# Create your views here.
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, UpdateView, CreateView
from .models import *


class PostListView(ListView):
    model = Post
    paginate_by = 3
    template_name = 'mainapp/post-list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=1).order_by('creation_date')


class PostCreateView(CreateView):
    model = Post
    template_name = 'mainapp/post-create.html'
    success_url = reverse_lazy('mainapp:profile:view')
    fields = ('name', 'image', 'link', 'text', 'status', 'category', 'image', )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)
        post.save()
        return HttpResponseRedirect(self.success_url)


class TopPostListView(ListView):
    model = Post
    paginate_by = 3
    template_name = 'mainapp/post-top.html'

    def get_queryset(self):
        qs = super().get_queryset().filter(status=1)

        return sorted(qs, key=lambda post: post.rating, reverse=True)[:10]


class PostContentView(TemplateView):
    model = Post
    template_name = 'mainapp/post-content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        post_id = kwargs['post_id']

        try:
            context['post'] = Post.objects.get(id=post_id)
            context['user_rated_post'] = Review.objects.filter(
                post=context['post'], user=self.request.user).exists() if self.request.user.is_authenticated else False
            context['comments'] = Comment.objects.filter(post=context['post'])
        except Post.DoesNotExist:
            context['post_does_not_exist'] = "Sorry, but this post does not exist, check URL."

        return context

    def post(self, request, *args, **kwargs):
        try:
            Comment.objects.create(user=request.user, text=request.POST.get('comment-text'),
                                   post=Post.objects.get(id=kwargs['post_id']))
        except Exception as e:
            print(e)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


@csrf_exempt
def send_review(request):
    post_id = request.POST.get('post_id')
    rating = request.POST.get('rating')
    try:
        Review.objects.create(user=request.user, mark=rating, post=Post.objects.get(id=post_id))
    except Exception as e:
        print(e)
    return HttpResponseRedirect(reverse_lazy('mainapp:posts:read', args=(post_id,)))


class CategoryListView(ListView):
    model = Category
    template_name = 'mainapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        category_id = self.request.GET.get('category_id')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None

        context['posts'] = Post.objects.filter(category=category)
        return context


class ProfileView(TemplateView):
    model = User
    template_name = "mainapp/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['author'] = Author.objects.get(user=self.request.user)
        except Author.DoesNotExist:
            pass
        return context
