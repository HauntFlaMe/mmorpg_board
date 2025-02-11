from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Post, Response
from .forms import PostForm, ResponseForm

# Главная страница со списком объявлений
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'board/post_list.html', {'posts': posts})

# Страница с деталями объявления
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'board/post_detail.html', {'post': post})

# Создание нового объявления
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'board/post_form.html', {'form': form})

# Редактирование объявления
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_list')  # Запрет редактирования чужих объявлений
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_form.html', {'form': form})

# Добавление отклика на объявление
@login_required
def add_response(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.post = post
            response.author = request.user
            response.save()

            # Отправка email автору объявления
            send_mail(
                'Новый отклик на ваше объявление',
                f'На ваше объявление "{post.title}" оставили отклик.',
                'from@example.com',
                [post.author.email],
                fail_silently=False,
            )

            return redirect('post_detail', pk=post.pk)
    else:
        form = ResponseForm()
    return render(request, 'board/add_response.html', {'form': form})

# Приватная страница с откликами на объявления пользователя
@login_required
def my_responses(request):
    responses = Response.objects.filter(post__author=request.user)
    return render(request, 'board/my_responses.html', {'responses': responses})

@login_required
def my_responses(request):
    query = request.GET.get('q')
    responses = Response.objects.filter(post__author=request.user)

    if query:
        responses = responses.filter(Q(post__title__icontains=query) | Q(text__icontains=query))

    return render(request, 'board/my_responses.html', {'responses': responses})
