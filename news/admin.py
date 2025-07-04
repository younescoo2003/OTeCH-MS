from django.contrib import admin
from news.models import ArticleImage, ArticleCategory, Article


class ArticleImageAdmin(admin.TabularInline):
    model = ArticleImage
    extra = 1

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_time')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_time', 'updated_time')
    inlines = [ArticleImageAdmin]
