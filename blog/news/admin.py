from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, CategorySubscribers


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'dateCreate', 'categoryType', 'rating') # выводим поля в админку
    list_filter = ('title', 'dateCreate', 'categoryType', 'rating') # добавляем фильтры в админку
    search_fields = ('title', 'dateCreate', 'categoryType', 'rating') # добавляем поиск по полям модели в админку


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')
    list_filter = ('authorUser', 'ratingAuthor')
    search_fields = ('authorUser', 'ratingAuthor')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(CategorySubscribers)
