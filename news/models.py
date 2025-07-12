from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class ArticleCategory(models.Model):
    title = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Article Category')
        verbose_name_plural = _('Article Categories')

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('title'))
    text = models.TextField(null=False, blank=False, verbose_name=_('text'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=False, blank=False,
                               verbose_name=_('author'), related_name='articles')
    origin = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('origin'))
    reference = models.URLField(null=False, blank=False, verbose_name=_('reference'))
    image = models.ImageField(null=True, blank=True, verbose_name=_('image'), upload_to='articles/')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('created time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('updated time'))

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name=_('article'), related_name='images')
    image = models.ImageField(upload_to='articles/', null=False, blank=False, verbose_name=_('image'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('created time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('updated time'))

    class Meta:
        verbose_name = _('article image')
        verbose_name_plural = _('article images')

    def __str__(self):
        return self.article.title
