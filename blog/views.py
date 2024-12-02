from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from .models import Post, Comment, Category
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')[:10]
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    post.views += 1
    post.save()
    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

@login_required
def new_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        image = request.FILES.get('image')
        tags = request.POST.get('tags')
        post = Post.objects.create(
            title=title, content=content, category=category,
            author=request.user, image=image, tags=tags, status='draft'
        )
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'blog/new_post.html', {'categories': categories})

@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk, status='published')
        content = request.POST.get('content')
        Comment.objects.create(post=post, user=request.user, content=content)
        return redirect('post_detail', pk=post.pk)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Foydalanuvchini ro'yxatdan o'tgandan keyin avtomatik kirish
            return redirect('home')  # Bosh sahifaga qaytaradi
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

# Logout funksiyasi
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})