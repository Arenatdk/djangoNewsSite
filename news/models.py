from django.db import models
from django.urls import reverse




class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Изменено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Паблик?')
    category = models.ForeignKey('Category', on_delete=models.PROTECT,  verbose_name='Категория')
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title + ', id:' + str(self.id)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'pk': self.pk})


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})
