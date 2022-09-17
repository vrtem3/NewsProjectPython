from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from datetime import datetime, timedelta
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import AuthorForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.core.mail import mail_admins  # импортируем функцию для массовой отправки писем админам
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.conf import settings
from django.utils import timezone
# from NewProject0622.settings import DAILY_POST_LIMIT
from .tasks import hello  # импорт задач приложения news
#  from django.http import HttpResponse


class PostList(ListView):
    model = Post
    ordering = '-dateCreate' # сортируем по дате объекты
    template_name = 'blog.html' # указываем шаблон, в котором выводим объекты
    context_object_name = 'postlist' # имя списка объектов, к которому обращаемся в html-шаблоне
    paginate_by = 5 # указываем, сколько выводить объектов на странице

    def get_queryset(self):
        queryset = super().get_queryset() # Получаем обычный запрос, используем наш класс фильтрации
        self.filterset = PostFilter(self.request.GET, queryset) # self.request.GET содержит объект QueryDict, сохраняем нашу фильтрацию в объекте класса
        # чтобы потом добавить в контекст и использовать в шаблоне.
        return self.filterset.qs # Возвращаем из функции отфильтрованный список товаров

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context
    
#  Запуск celery задачи в представлении
#    def get(self, request):
#        hello.delay()
#        return HttpResponse('Hello!')


class PostDetail(DetailView):
    model = Post
    ordering = 'title'
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем количество постов автора за текущие сутки
        limit = settings.DAILY_POST_LIMIT
#        limit = DAILY_POST_LIMIT
        context['limit'] = limit
        last_day = timezone.now() - timedelta(days=1)
#        last_day = datetime.utcnow() - timedelta(days=1)
        posts_day_count = Post.objects.filter(
            authorConnect__authorUser=self.request.user,
            dateCreate__gte=last_day,
        ).count()
        context['count'] = posts_day_count
        context['post_limit'] = posts_day_count < limit
        return context

    # для отображения подписки/отписки
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        id = self.kwargs.get('pk')
#        catPost = Category.objects.filter(pk=Post.objects.get(pk=id).post_category.all).values("subscribers__username")
#        context['is_not_subscribe'] = not catPost.filter(subscribers__username=self.request.user).exists()
#        context['is_subscribe'] = catPost.filter(subscribers__username=self.request.user).exists()
#        return context


#  Представление для создания нового объекта (CreateView)
#  PermissionRequiredMixin ограничение прав доступа к объектам модели (view, add, change, delete)
class PostCreateNews(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'
    permission_required = ('blog.add_post', 'blog.change_post', 'blog.delete_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = "NW"
        return super().form_valid(form)


class PostCreateArticles(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'
    permission_required = ('blog.add_post', 'blog.change_post', 'blog.delete_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = "AR"
        return super().form_valid(form)


# Представление для изменения объекта
class PostEdit(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'
    permission_required = ('blog.add_post', 'blog.change_post', 'blog.delete_post')


# Представление для удаления товара
class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('blog.add_post', 'blog.change_post', 'blog.delete_post')


# Представление в виде функции для редактирования объектов модели Автора
@login_required()  # login_url = "/home/" - адрес переадресации в случае неавторизации пользователя
def EditAuthor(request):
    form = AuthorForm()
    return render(request, 'author_edit.html', {"formAuthor": form})


#  Подписка на категорию
@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователю', request.user, 'добавлена категория в подписки:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/blog/')


#  Функция отписки от категории
@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'убрал из подписок категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/blog/')