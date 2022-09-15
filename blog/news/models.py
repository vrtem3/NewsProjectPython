from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    ratingAuthor = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating_author = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return str(self.authorUser)
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True, verbose_name='Название категории')
    subscribers = models.ManyToManyField(User, through='CategorySubscribers', blank=True, verbose_name='Подписчики')

    def __str__(self):
        return str(self.categoryName)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    authorConnect = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOISES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOISES, default=ARTICLE, verbose_name='Категория')

    dateCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, verbose_name='Название')
    text = models.TextField(verbose_name='Текст публикации')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
    

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.postThrough)


class CategorySubscribers(models.Model):
    subscriberThru = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,)
    categoryThru = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Публикация')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст комментария')
    dateCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'