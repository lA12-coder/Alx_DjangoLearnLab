from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.db.models import Q
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm, RegistrationForm

# Post list with optional search
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 10
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        tag = self.kwargs.get('tag')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)).distinct()
        if tag:
            qs = qs.filter(tags__name=tag)
        return qs

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        # custom save handles tags via save()
        response = super().form_valid(form)
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def form_valid(self, form):
        # remove existing tags if the user provided a new tags_field
        self.object.tags.clear()
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# Comments: create/edit/delete
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(post.get_absolute_url())

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()

# Registration view
class RegisterView(FormView):
    template_name = 'blog/auth/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

# Profile editing simple view (function-based)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/auth/profile.html', {'form': form})
